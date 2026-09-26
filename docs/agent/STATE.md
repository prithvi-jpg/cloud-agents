# State

## Objective and phase

Objective: maintain and evaluate the public Cloud Agents skill, including portable model routing.

Current phase: model-routing documentation awaiting cross-harness verification.

## Active plan and one next action

Next best action: validate the documented routing in a Codex task and a Claude-capable task using representative work.

## Verified evidence

- The source was copied from the maintainer's current installed skill into an isolated repository checkout.
- Personal labels and machine-local schema IDs were removed from the public candidate.
- Deterministic tests and tracked-source disclosure checks are part of the candidate verification path.
- Eight unit tests pass, including positive and negative controls for project and memory validation plus skill-package metadata checks.
- The official Skill Creator validator, repository project validation, Python compilation, whitespace checks, and a tracked-source secret/path scan pass locally.
- The maintainer explicitly approved public publication under MIT for this release.
- Public commit `117c45946bf886acfda276dc2800667f863835a8` contains the approved v0.1.0 scope.
- GitHub Actions run `30877600999` passed all checks on Python 3.10, 3.11, and 3.12.
- GitHub release `v0.1.0` is published and points to the verified commit.
- Public readback confirms MIT licensing, project metadata, topics, Discussions, and private vulnerability reporting.
- The model-routing note describes GPT-6 Sol/Astra in Codex and Claude Fable in a Claude-capable harness without adding model IDs to canonical project state. The public `main` branch contains the first routing note at `e06ac49`; GitHub Actions run `36269356537` passed all three Python matrix jobs.
- A local follow-up candidate shortens the root skill into a task-based router and makes repository guidance proportional to the task. It requires local checks and a separate review before publication.

## Decisions and rejected paths

- Selected the existing empty public `cloud-agents` repository instead of exposing a private application workspace.
- Rejected publishing the synthetic-user research workspace wholesale because it contains third-party checkouts and run artifacts.
- Rejected claiming stars, downloads, broad adoption, or production validation that do not exist.

## Assumptions, risks, and open questions

- The maintainer owns the original operating-skill text and licensed the public release under MIT.
- Early usefulness is supported by the artifact design and passing checks; external adoption remains unverified.
- Harness compatibility beyond the documented file format remains a roadmap item.
- Model access and supported effort levels vary by account and harness; this routing note requires checking the target environment rather than implying entitlement.

## Capability shortlist and rationale

- GitHub Issues and Discussions for public maintainer feedback.
- CI fixtures for falsifiable compatibility evidence.
- Release receipts and changelog entries for externally visible changes.

## Authority boundary

- Scoped, reversible local maintenance and verification may proceed.
- Future public pushes, releases, permission changes, and other consequential external actions require explicit approval.

## Verification status

v0.1.0 and the first routing update are public with passing CI. The simplification follow-up remains local until separately reviewed and pushed. Live cross-harness behavior and external adoption remain unverified.

## Handoff note

Start with this receipt, then use a real issue or compatibility fixture as the next evidence source. Do not convert repository existence into an adoption claim.
