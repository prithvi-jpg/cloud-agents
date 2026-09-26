---
name: delegation-timeout-salvage
description: Salvage subagent disk output when delegate_task times out
---

# Delegation Timeout Salvage

## When to use this
You dispatched one or more `delegate_task` (or `delegate_task` batch) subagents, they ran
for their full budget, and came back as `status=timeout` with **no summary and no returned
file** — yet the task told them to *write incrementally to a disk file as they went*. The
data is almost certainly still on disk. Salvage it instead of re-dispatching.

This is confirmed working: in one session three research agents each timed out at ~600s but
had written 889 / 414 / 562 lines of real, sourced content to `/tmp/res_*.md` before dying.
Grepping those files gave everything needed; the rebuilt output was correct and verified.

## The core principle
A subagent's *final summary* is fragile (it's the last thing written, and the thing that
gets cut when the budget expires). Its *side effects on disk* are durable. Design every
long delegation so the valuable output lands in a file as it is produced, never only in the
final message.

## How to brief the child (the part that makes salvage possible)
Embed these instructions verbatim in the `goal` / `context`:
- "Write findings **incrementally** to `<explicit file path>` as you go. Append sections;
  do NOT save everything at the end."
- "Use real verified URLs for every claim — NO invented links."
- Give a specific, existing file path (e.g. `/tmp/res_fluidstack.md`), not a vague one.

Children that gather for the whole budget and emit their report only at the end return
`timeout` with nothing usable. Children that append to disk leave a recoverable artefact
even on timeout.

## On timeout: the salvage sequence
1. Do NOT re-dispatch immediately — the work is probably already done on disk.
2. Check the output files exist and have real content:
   `for f in /tmp/res_*.md; do wc -l "$f"; done`
3. Grep the file for URLs to confirm they are real (not placeholders):
   `grep -oE 'https?://[^ )]+' "$f" | head`
4. The complete tool/assistant trace also lives at the live transcript path returned in the
   dispatch result, e.g.
   `/home/prithvi/.hermes/cache/delegation/live/<deleg_id>/task-<n>.log`
   — use it only if the disk file is missing.
5. Treat salvaged content as a *draft source*, then cross-check its specific figures against
   whatever consumes them (e.g. reconcile research numbers with an app before trusting them).
   See `references/salvage-recipe.md` for the exact reconciliation pattern used.

## Pitfalls
- **Don't assume timeout == no work done.** It usually means "did the work, failed to report."
  Re-dispatching wastes the budget and can produce conflicting drafts.
- **Don't trust a salvaged number blindly.** A child can surface a figure that contradicts
  your existing artefact. Diff the research against the consumer (app / doc) and patch
  discrepancies. (In the validating session, this caught a backstop total that was
  $4.9B in the app vs $4.6B in the research — the research was right.)
- **Split goals with >4 deliverables into separate narrow tasks** so each child is more
  likely to finish within budget and to a coherent file.
- **Front-load durable side effects** (writes to disk, `git clone --depth 1`) — those
  survive even a hard kill; in-session reasoning does not.

## Overlap note
`software-development/subagent-driven-development` covers the *happy path* of using
subagents. It is user-owned / non-curator-managed and off-limits to autonomous patch, so the
timeout-and-salvage recovery procedure lives here instead. The background curator can
consolidate if desired.

See `references/salvage-recipe.md` for the copy-paste verification recipe.
