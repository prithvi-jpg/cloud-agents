# Cloud Agents

## Source of truth

- Direct maintainer instructions and reviewed pull-request changes take priority.
- For material decisions or a resumed task, read the relevant parts of `docs/agent/PROJECT.md` and `docs/agent/STATE.md`; focused edits need only the files they affect.
- Preserve evidence before interpretation and keep private fixtures out of the repository.

## Scope and authority

- Proceed with scoped, reversible local changes and deterministic checks.
- Preview and obtain explicit maintainer approval before publishing, releasing, changing repository access, or making other consequential external changes.

## Stable conventions

- Support Python 3.10+ without third-party runtime dependencies.
- Keep canonical project state harness-independent.
- Add passing and failing tests for behavior-affecting validation changes.
- Separate verified behavior, inference, proposal, and roadmap claim.

## Definition of done

- The relevant artifact exists and matches the acceptance criteria.
- Run checks relevant to the change. Before a public push, run unit tests, project validation, and Python compilation.
- Public claims stay within the evidence recorded in the repository.
- Known limitations and one next action are recorded in `docs/agent/STATE.md`.
