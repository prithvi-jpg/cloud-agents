# Changelog

All notable changes to Cloud Agents will be documented here.

## Unreleased

### Added

- A portable model and harness routing reference for Codex GPT-6 Sol/Astra and Claude Fable, including effort, entitlement, and evaluation boundaries.

### Changed

- Shortened the adaptive skill description and root instructions into a task-based router; detailed procedures remain in references.
- Made repository guidance and required checks proportional to the task while preserving the full pre-push gate.
- Added a minimal `CLAUDE.md` import so Claude Code reads the repository's shared `AGENTS.md` instructions without duplicating them.
- Added a pinned, rollback-capable portable installer for 189 skill names, a source manifest, 21 bundled local skills, and an equivalent ZIP download. Managed Codex plugins remain inventory entries.

## [0.1.0] - 2026-08-03

### Added

- Initial release of the Agent Systems Foundry operating skill.
- Dependency-free project initialization and validation utilities.
- Markdown memory-bundle validator.
- JSON Schemas for work packets, task state, run events, compound runs, and memory records.
- Tests, CI, contribution guidance, security policy, and explicit proof boundaries.
