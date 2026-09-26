# Tester packet

## Inputs

- Run manifest: `<run-dir>/manifest.json`
- Assigned profile: `<run-dir>/profiles/<agent-id>.json`
- Result destination: `<run-dir>/results/<agent-id>.json`
- Trace directory: `<run-dir>/traces/<agent-id>/`
- Screenshot directory: `<run-dir>/screenshots/<agent-id>/`
- Browser session: `<run-id>-<agent-id>`

## Objective

Attempt the manifest mission from the assigned profile’s declared starting knowledge and constraints. Produce observable evidence about the interface, not a story about the character.

## Rules

1. Read the target’s `AGENTS.md` and current project state when the manifest permits source access.
2. Operate only the declared URL, fixture, authority mode, time budget, and action budget.
3. Capture an initial snapshot before interaction.
4. Refresh element references after DOM or navigation changes.
5. Preserve decisive screenshots, snapshots, URLs, and visible error states.
6. Stop before any forbidden or consequential action.
7. Do not inspect another tester’s result.
8. Do not infer feelings, prevalence, adoption, disability experience, or human preference.
9. Use `unknown` when the evidence is insufficient.
10. Write valid JSON matching `result-contract.md` and close the session.

## Finding test

For every finding ask:

- What exactly was visible or operable?
- Which trace or screenshot proves it?
- Is this observed, interpreted, specified, simulated, or unknown?
- What user job could it affect?
- Is the consequence deterministic or a hypothesis?
- Does it require a human participant or qualified reviewer?

## Completion

A tester is complete only when its result JSON exists, includes an authority receipt, and references the captured evidence. A browser summary in chat is not the artifact.
