# Project

## Outcome and users

Maintain a small, portable operating layer that helps agent builders and open-source maintainers run recoverable, bounded, and evidence-backed AI-agent workflows.

## Baseline and causal problem

Agent frameworks expose models and tools, but project truth, authority, recovery, and completion proof often remain implicit in transcripts. This makes long-running work difficult to inspect, resume, review, and trust.

## Constraints and non-goals

- No model or harness dependency in canonical state.
- No credential storage or raw-secret handling.
- No claim that synthetic or automated evaluation proves human outcomes.
- No long-horizon machinery for projects that do not need it.

## Quality bar and references

- Dependency-free core utilities with deterministic tests.
- Typed, documented schemas with explicit compatibility changes.
- Human-readable canonical records and rebuildable derived indexes.
- External research remains comparative evidence, not project authority.

## Authority and approval boundary

- Scoped local implementation and verification may proceed after alignment.
- Public pushes, releases, permission changes, and other consequential external actions require exact preview and explicit maintainer approval.

## Canonical sources and evidence standard

- Maintainer instructions and reviewed repository files are primary.
- Tests demonstrate bounded code behavior, not broad user outcomes.
- Adoption, compatibility, and impact claims require current public evidence.

## Human steering points

- Authority semantics, schema-breaking changes, project-spine changes, releases, and public claims require maintainer review.

## Acceptance criteria and completion proof

- The isolated skill package, reference docs, scripts, and schemas are present and internally linked.
- Unit tests pass on Python 3.10, 3.11, and 3.12 in CI.
- The repository validates its own project spine.
- Tracked source contains no credentials, personal fixtures, or machine-specific absolute paths.
- Release claims disclose the project's actual maturity and limitations.
