"""
Pre-flight check for a TRPA repo handoff.

Usage:
    python handoff_check.py [repo_path]

Checks that the handoff docs exist and are wired into CLAUDE.md, that the
handoff is dated and current, that nothing is uncommitted or unpushed, and
that the docs hold no secrets, machine-specific paths, leftover placeholders,
or em dashes.

Standard library only. Runs under arcgispro-py3 or any Python 3.9 or later.
Exit code 1 when any check fails.
"""
import re
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path

REQUIRED = ["CLAUDE.md", "docs/CONTEXT.md", "docs/HANDOFF.md", "docs/DECISIONS.md"]
IMPORTS = ["@docs/HANDOFF.md", "@docs/CONTEXT.md"]

# Line budgets. CLAUDE.md and its imports load every session, so size is context cost.
CLAUDE_MD_WARN_LINES = 40
CLAUDE_MD_FAIL_LINES = 200
HANDOFF_WARN_LINES = 60
CONTEXT_WARN_LINES = 120

SECRET_PATTERNS = {
    "password or token assignment": r"(?i)(password|passwd|pwd|secret|token|api[_-]?key|access[_-]?key)\s*[:=]\s*['\"]?[A-Za-z0-9+/_\-\.]{8,}",
    "AWS access key": r"\bAKIA[0-9A-Z]{16}\b",
    "connection string with password": r"(?i)(pwd|password)=[^;\s]{4,}",
    "GitHub token": r"\bgh[pousr]_[A-Za-z0-9]{20,}\b",
    "ArcGIS or generic bearer token": r"(?i)\b(bearer|token)\s+[A-Za-z0-9\-_\.]{40,}",
    "private key block": r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
}

MACHINE_PATH_PATTERNS = {
    "Windows user profile path": r"[A-Za-z]:\\Users\\[^\\\s]+",
    "macOS user path": r"(?<![\w/])/Users/[^/\s]+",
    "Linux home path": r"(?<![\w/])/home/[^/\s]+",
}

PLACEHOLDER_PATTERN = r"<[A-Za-z][^<>\n]{2,240}>"
PLACEHOLDER_WORDS = r"\b(TODO|TBD|fill in|FILL IN|lorem ipsum)\b"

results = []


def record(level, area, message):
    results.append((level, area, message))


def read(path):
    return path.read_text(encoding="utf-8", errors="replace")


def strip_code(text):
    """Drop fenced blocks and inline code so patterns only hit prose."""
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    text = re.sub(r"`[^`\n]*`", "", text)
    return text


def git(repo, *args):
    try:
        out = subprocess.run(
            ["git", "-C", str(repo), *args],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=30,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None
    if out.returncode != 0:
        return None
    # Only trailing newlines are stripped; porcelain output has a meaningful leading space.
    return out.stdout.rstrip("\n")


def check_files(repo):
    missing = [f for f in REQUIRED if not (repo / f).exists()]
    if missing:
        record("FAIL", "files", "missing: " + ", ".join(missing) + ". Run Init from the trpa-repo-handoff skill.")
    else:
        record("PASS", "files", "CLAUDE.md and the three docs are present")
    return not missing


def check_claude_md(repo):
    path = repo / "CLAUDE.md"
    text = read(path)
    prose = strip_code(text)
    missing = [imp for imp in IMPORTS if imp not in prose]
    if missing:
        record("FAIL", "CLAUDE.md", "missing import lines: " + ", ".join(missing) + ". Add them on their own lines, outside backticks.")
    else:
        record("PASS", "CLAUDE.md", "imports HANDOFF.md and CONTEXT.md")

    lines = text.count("\n") + 1
    if lines > CLAUDE_MD_FAIL_LINES:
        record("FAIL", "CLAUDE.md", f"{lines} lines; Claude Code adherence drops past {CLAUDE_MD_FAIL_LINES}. Move facts to docs/CONTEXT.md.")
    elif lines > CLAUDE_MD_WARN_LINES:
        record("WARN", "CLAUDE.md", f"{lines} lines; target is under {CLAUDE_MD_WARN_LINES}. Move facts to docs/CONTEXT.md.")


def parse_handoff_date(text):
    m = re.search(r"\*\*Last updated:\*\*\s*(\d{4}-\d{2}-\d{2})", text)
    if not m:
        return None
    try:
        return datetime.strptime(m.group(1), "%Y-%m-%d").date()
    except ValueError:
        return None


def check_handoff_date(repo):
    text = read(repo / "docs/HANDOFF.md")
    updated = parse_handoff_date(text)
    if updated is None:
        record("FAIL", "HANDOFF.md", "no '**Last updated:** YYYY-MM-DD' line found")
        return
    if updated > date.today():
        record("WARN", "HANDOFF.md", f"last updated {updated} is in the future")

    # Latest commit that touched something other than docs/ and CLAUDE.md.
    last_code = (git(repo, "log", "-1", "--format=%cs", "--", ".", ":(exclude)docs", ":(exclude)CLAUDE.md") or "").strip()
    if last_code:
        try:
            last_code_date = datetime.strptime(last_code, "%Y-%m-%d").date()
        except ValueError:
            last_code_date = None
        if last_code_date and last_code_date > updated:
            record("FAIL", "HANDOFF.md", f"last updated {updated} but code changed in a commit on {last_code_date}. Rewrite the handoff.")
            return
    record("PASS", "HANDOFF.md", f"dated {updated}, no code commits after it")


def check_git(repo):
    if not (repo / ".git").exists():
        record("WARN", "git", "not a git repo; a handoff without a remote is a folder copy. Say so in the note.")
        return
    if git(repo, "rev-parse", "--is-inside-work-tree") is None:
        record("WARN", "git", "git not available on this machine; could not check branch, uncommitted, or unpushed state")
        return

    branch = (git(repo, "branch", "--show-current") or "").strip() or "(detached)"
    porcelain = git(repo, "status", "--porcelain")
    if porcelain and porcelain.strip():
        files = [line[3:] for line in porcelain.splitlines() if len(line) > 3]
        shown = ", ".join(files[:6]) + (" ..." if len(files) > 6 else "")
        record("FAIL", "git", f"{len(files)} uncommitted change(s) on {branch}: {shown}")
    else:
        record("PASS", "git", f"working tree clean on {branch}")

    upstream = git(repo, "rev-parse", "--abbrev-ref", "@{u}")
    if upstream is None:
        record("WARN", "git", f"branch {branch} has no upstream; push with -u so the coworker can pull it")
    else:
        upstream = upstream.strip()
        ahead = (git(repo, "rev-list", "--count", "@{u}..HEAD") or "").strip()
        behind = (git(repo, "rev-list", "--count", "HEAD..@{u}") or "").strip()
        if ahead and ahead != "0":
            record("FAIL", "git", f"{ahead} commit(s) not pushed to {upstream}")
        else:
            record("PASS", "git", f"nothing unpushed relative to {upstream}")
        if behind and behind != "0":
            record("WARN", "git", f"{behind} commit(s) on {upstream} not pulled here; pull before handing off")

    handoff = read(repo / "docs/HANDOFF.md")
    m = re.search(r"\*\*Branch:\*\*\s*`?([^`,\s]+)", handoff)
    if m and m.group(1) != branch and not m.group(1).startswith("<"):
        record("WARN", "git", f"HANDOFF.md says branch {m.group(1)} but checkout is {branch}")


def check_doc_content(repo):
    docs = [repo / "CLAUDE.md"] + sorted((repo / "docs").glob("*.md"))
    for path in docs:
        rel = path.relative_to(repo).as_posix()
        text = read(path)
        prose = strip_code(text)

        for name, pat in SECRET_PATTERNS.items():
            for m in re.finditer(pat, text):
                line = text[: m.start()].count("\n") + 1
                record("FAIL", "secrets", f"{rel}:{line} looks like a {name}. Name the variable, never the value.")

        for name, pat in MACHINE_PATH_PATTERNS.items():
            for m in re.finditer(pat, text):
                line = text[: m.start()].count("\n") + 1
                record("FAIL", "paths", f"{rel}:{line} {name}: {m.group(0)!r}. Use a repo-relative or shared path.")

        for m in re.finditer("—|–", prose):
            line = prose[: m.start()].count("\n") + 1
            kind = "em dash" if m.group(0) == "—" else "en dash"
            record("FAIL", "style", f"{rel}:{line} {kind}. TRPA docs use commas, periods, or 'to'.")

        for m in re.finditer(r"\d%|(?<=\s)[&+=]|[&+=](?=\s)", prose):
            line = prose[: m.start()].count("\n") + 1
            record("WARN", "style", f"{rel}:{line} symbol in body text: {prose[max(0, m.start() - 20): m.end() + 20]!r}")

        placeholder_level = "FAIL" if rel == "docs/HANDOFF.md" else "WARN"
        hits = list(re.finditer(PLACEHOLDER_PATTERN, prose)) + list(re.finditer(PLACEHOLDER_WORDS, prose))
        # Allow genuine HTML or markdown angle brackets only when they look like tags.
        hits = [h for h in hits if not re.fullmatch(r"</?[a-z][a-z0-9]*( [^>]*)?>", h.group(0))]
        if hits:
            first = hits[0]
            line = prose[: first.start()].count("\n") + 1
            record(placeholder_level, "placeholders", f"{rel}: {len(hits)} placeholder(s) left, first at line {line}: {first.group(0)!r}")

    for rel, limit in (("docs/HANDOFF.md", HANDOFF_WARN_LINES), ("docs/CONTEXT.md", CONTEXT_WARN_LINES)):
        lines = read(repo / rel).count("\n") + 1
        if lines > limit:
            record("WARN", "size", f"{rel} is {lines} lines; it loads every session, so keep it under {limit}")


def main():
    repo = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    if not repo.is_dir():
        print(f"Not a directory: {repo}")
        return 2

    print(f"Handoff check: {repo}")
    if check_files(repo):
        check_claude_md(repo)
        check_handoff_date(repo)
        check_git(repo)
        check_doc_content(repo)
    else:
        check_git(repo)

    order = {"FAIL": 0, "WARN": 1, "PASS": 2}
    for level, area, message in sorted(results, key=lambda r: order[r[0]]):
        print(f"[{level}] {area}: {message}")

    fails = sum(1 for r in results if r[0] == "FAIL")
    warns = sum(1 for r in results if r[0] == "WARN")
    print(f"Result: {fails} FAIL, {warns} WARN")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
