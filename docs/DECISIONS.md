# Decisions

Newest first. One entry per decision someone could reasonably re-litigate. Record the why, not the what; the what is in git.

## 2026-10-23: Pod engagement docs live in the tools repo, the process lives here as trpa-pod

**Why:** Department engagement folders, the intake template, and the beta app scaffold sit in `trpa-agency/tools` next to the betas they produce, so an engagement and its output share one repo and one commit history. The process itself is a skill here so every machine and staff member runs an engagement the same way. The tools repo is public, so engagement notes are role-level only, and the skill repeats that rule.
**Alternatives considered:** Everything in the skills repo (separates engagements from their outputs); everything in the tools repo (process does not reach other machines as a skill).
**Revisit if:** engagements start producing mostly non-app outputs and the tools repo stops being the natural home.

## 2026-10-23: Keep one plugin per skill in the marketplace

**Why:** Staff already install skills individually and the README documents that flow. One bundled plugin would be one install and one update, but it would break every existing install and force a reinstall.
**Alternatives considered:** One `trpa-skills` plugin holding every skill under `skills/`.
**Revisit if:** the skill count grows past twenty and staff complain about the install line, or a managed settings rollout requires every machine to carry the full set.

## 2026-10-23: Repo memory lives in tracked docs, not in Claude Code auto memory

**Why:** Auto memory sits in `~/.claude/projects/<repo>/memory/` on one machine and never reaches a coworker. The `autoMemoryDirectory` setting needs an absolute path, so it cannot point into a clone. The only memory that travels is what is committed, so `CLAUDE.md` imports `docs/HANDOFF.md` and `docs/CONTEXT.md` at launch and `docs/DECISIONS.md` is read on demand.
**Alternatives considered:** Pointing auto memory at the repo (impossible with a relative path); relying on session transcripts (machine local); writing everything into `CLAUDE.md` (grows past the 200 line adherence limit).
**Revisit if:** Claude Code ships shared or repo-scoped auto memory.

## 2026-10-23: Claude sessions need the GitHub App to push here

**Why:** A Claude session attached this repo and could clone and fetch but not push; the org has not installed the Claude GitHub App. Until it is installed, Claude work arrives as a patch or a local branch and Mason pushes.
**Alternatives considered:** Pushing with a personal token from a session (not allowed; secrets stay out of sessions).
**Revisit if:** an org admin installs the app at https://github.com/apps/claude/installations/select_target or reconnects GitHub from claude.ai settings.

## 2026-10-09: Evals and iteration output are gitignored

**Why:** Skills are the deliverable. Eval runs and workspaces are large, machine specific, and change every iteration.
**Alternatives considered:** Committing `evals/` prompts without results.
**Revisit if:** the team wants `claude plugin eval` in CI, which needs the case folders tracked.
