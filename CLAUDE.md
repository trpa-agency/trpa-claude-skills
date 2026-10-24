# trpa-claude-skills

The Claude plugin marketplace TRPA staff install skills from. One plugin per folder under `skills/`.

## How we work in this repo

Read the handoff and context below before changing anything. They are imported here, so they are already in your context at launch; if you do not see them, read `docs/HANDOFF.md` and `docs/CONTEXT.md` now.

Before changing an approach, read `docs/DECISIONS.md`. If a decision there covers your change, follow it or add a new dated entry explaining why it changed.

Before ending a session that changed a skill, the marketplace file, or the README, rewrite `docs/HANDOFF.md` (state, next steps, open questions, blockers), add any decisions to `docs/DECISIONS.md`, run `python skills/trpa-repo-handoff/scripts/handoff_check.py .`, commit as `docs: handoff YYYY-MM-DD`, and push. Use the `trpa-repo-handoff` skill if it is installed; it has the checks and the handoff note.

## Skills for this repo

skill-creator to build or revise a skill, trpa-brand for the writing rules every SKILL.md follows, trpa-repo-handoff

## Repo-specific rules

- A new skill is a new folder under `skills/`, a new entry in `.claude-plugin/marketplace.json`, and a new row in the README table. The `name` in SKILL.md must match the marketplace entry.
- Run `claude plugin validate .` before every commit that touches a skill or the marketplace file.
- No em dashes, Oxford commas, no symbols in body text, in every SKILL.md and doc.

@docs/HANDOFF.md
@docs/CONTEXT.md
