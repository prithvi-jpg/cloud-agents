# Contributing

Cloud Agents is intentionally evidence-driven. A contribution should make the operating model easier to use, safer, more portable, or more falsifiable.

## Good contributions

- a reproducible failure case with the model, harness, environment, and observed outcome;
- a small adapter that keeps canonical project state harness-independent;
- a backward-compatible schema improvement with fixtures;
- a validation rule with both passing and failing tests;
- documentation that reduces ambiguity without adding ceremony.

## Before opening a pull request

1. Open an issue for changes that alter authority semantics, schema contracts, or the default project spine.
2. Keep private data, credentials, proprietary prompts, and real user records out of fixtures.
3. Add or update tests for observable behavior.
4. Run:

```bash
python3 -m unittest discover -s tests -v
python3 skill/adaptive-agent-operating-system/scripts/validate_project.py --root .
python3 -m compileall -q skill/adaptive-agent-operating-system/scripts tests
```

5. Describe the problem, evidence, compatibility impact, and rollback path in the pull request.

## Compatibility

The schemas follow semantic versioning after v1. Before v1, breaking changes may occur, but they must be called out in `CHANGELOG.md` and accompanied by a migration note.

## Review expectations

The maintainer will prioritize correctness, authority boundaries, privacy, recoverability, and evidence over feature volume. A green test run is necessary but may not be sufficient for changes that affect human or external-state boundaries.
