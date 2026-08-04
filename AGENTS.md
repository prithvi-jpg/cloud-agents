# Cloud Agents

## Source of truth

- Direct maintainer instructions and reviewed pull-request changes take priority.
- Canonical project framing lives in `docs/agent/PROJECT.md`.
- Current working truth lives in `docs/agent/STATE.md`.
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
- Unit tests, project validation, and compilation pass.
- Public claims stay within the evidence recorded in the repository.
- Known limitations and one next action are recorded in `docs/agent/STATE.md`.
