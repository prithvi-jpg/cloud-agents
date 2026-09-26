# Codex inline delivery

Use this checklist after following the current `visualize` skill.

## Fragment contract

- The file is an HTML fragment, not a full document.
- CSS is scoped under one unique root ID.
- The first view is useful without interaction.
- The width works around 736 CSS pixels and narrows gracefully.
- Light and dark host themes remain legible.
- Data, styles, scripts, and small assets are self-contained.
- No runtime fetch is required.
- Buttons either change local state or call `window.openai.sendFollowUpMessage({ prompt })`.
- The fragment stays below the renderer size limit.
- A surrounding response supplies the title, description, and any necessary citations.

## Mixed Windows and WSL delivery

Codex Desktop can resolve the inline directive through a WSL visualization path even when the working artifact was written to the Windows-backed path. Markdown media and inline HTML can also use different path bridges.

When both resolvers have appeared in the task:

1. Write the canonical fragment to the thread-scoped Windows-backed visualization directory.
2. Mirror the byte-identical file to the thread-scoped WSL visualization directory.
3. Compare hashes.
4. Render the canonical fragment with the bundled renderer.
5. Exercise the first interaction and inspect browser errors.
6. Run `scripts/verify-codex-inline.sh <YYYY/MM/DD> <thread-id> <basename.html>`.
7. Emit only the basename in `::codex-inline-vis{file="..."}`.

Do not use a WSL-only local media reference inside the fragment. Embed small media as data URIs when inline playback is required and the total remains below the size limit.

## Resolver precedence

Choose the resolver from the active host before emitting the response:

1. If Codex Desktop app context provides a thread-scoped visualization root or documents `::codex-inline-vis`, use the basename-only directive.
2. If another active host explicitly requires an absolute-path visualization content reference and provides no basename protocol, use that host's required reference.
3. Never emit both formats in one response to guess which resolver will work.

In mixed Windows/WSL Codex Desktop tasks, the final form is:

```text
::codex-inline-vis{file="example.html"}
```

The basename must exist with identical bytes in both current thread roots. Do not place an absolute `/mnt/c/...` or `/home/...` path inside this directive.

## Failure triage

| Symptom | Failed layer | Correct response |
|---|---|---|
| `Invalid visualization read request` | Resolver schema | Keep the validated fragment, stop using the absolute-path request, and retry once with the basename-only Codex Desktop directive. |
| `ENOENT` or file not found | Mirror/path | Verify date, thread ID and basename; create the missing WSL thread mirror; compare hashes. |
| Inline surface loads but is blank, clipped or inert | Fragment/renderer | Inspect literal markup, viewport behavior, queried elements, CSP and console errors. |
| A local file opens externally | Delivery surface | Use the inline directive; keep a file link only as an explicit fallback. |

Do not change visual content until the failing layer has been identified. File validity, file reachability, resolver validity and renderer validity are separate proofs.

## Receipt

Record:

- canonical path
- mirror path
- byte size
- matching hash
- selected resolver protocol
- exact basename directive
- target viewport
- interactions exercised
- console error count
- successful inline resolver result when the host can report it
- media readiness when applicable

File creation is not delivery. The renderer must load and the interaction must work.
