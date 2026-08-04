# Cloud Agents

Cloud Agents is an open-source operating layer for long-running AI-agent work. It adds portable project truth, bounded authority, typed work packets, recoverable task state, durable memory records, and evidence-backed completion to agent workflows.

This repository packages the **Agent Systems Foundry OS** as a reusable agent skill plus dependency-free Python utilities and JSON Schemas.

> **Project status:** v0.1.0 initial public release. This is a new project. It does not claim established adoption or production-wide validation yet.

## Why this exists

Agent frameworks are good at invoking models and tools. Real project work also needs an operating contract:

- What is the current source of truth?
- What may the agent do without approval?
- How does work survive a restart or handoff?
- How are retries, budgets, and approvals represented?
- What evidence is required before completion is claimed?

Cloud Agents makes those concerns explicit and inspectable instead of leaving them implicit in a chat transcript.

## What is included

| Component | Purpose |
| --- | --- |
| [`skill/adaptive-agent-operating-system/SKILL.md`](skill/adaptive-agent-operating-system/SKILL.md) | The portable operating skill and routing map |
| [`scripts/init_project.py`](skill/adaptive-agent-operating-system/scripts/init_project.py) | Creates a minimal `AGENTS.md` + project/state spine without overwriting files |
| [`scripts/validate_project.py`](skill/adaptive-agent-operating-system/scripts/validate_project.py) | Validates the project spine and its required sections |
| [`scripts/validate_memory_bundle.py`](skill/adaptive-agent-operating-system/scripts/validate_memory_bundle.py) | Validates provenance-aware Markdown memory records |
| [`assets/schemas`](skill/adaptive-agent-operating-system/assets/schemas) | JSON Schemas for work packets, task state, run events, compound runs, and memory records |
| [`references`](skill/adaptive-agent-operating-system/references) | Detailed guidance for authority, context, orchestration, evaluation, recovery, HCI, and memory |

## Quick start

The utilities require Python 3.10+ and have no third-party dependencies.

```bash
git clone https://github.com/prithvi-jpg/cloud-agents.git
cd cloud-agents

mkdir -p /tmp/cloud-agents-demo
python3 skill/adaptive-agent-operating-system/scripts/init_project.py \
  --root /tmp/cloud-agents-demo \
  --name "Cloud Agents Demo" \
  --outcome "Ship a small, verifiable agent workflow."

python3 skill/adaptive-agent-operating-system/scripts/validate_project.py --root /tmp/cloud-agents-demo
```

The initializer is idempotent: existing project files are reported and preserved.

To install the skill in Codex, copy the isolated package directory into your Codex skills directory:

```bash
cp -R skill/adaptive-agent-operating-system "${CODEX_HOME:-$HOME/.codex}/skills/"
```

The package keeps its `SKILL.md`, agent metadata, scripts, references, and assets together; repository-only files remain outside the installed skill.

## Operating model

The system separates four kinds of autonomy:

1. **Think and explore:** wide freedom, with uncertainty labeled.
2. **Create locally:** high autonomy inside a clear, reversible scope.
3. **Change consequential state:** exact preview and explicit approval.
4. **Change durable behavior:** evaluated candidate, reviewable diff, approval, version, and rollback.

A default project uses three small files:

```text
AGENTS.md                  stable repository map and authority boundary
docs/agent/PROJECT.md      durable outcome and acceptance contract
docs/agent/STATE.md        compact current truth and one next action
```

Long-horizon projects can add typed task state, work packets, append-only run events, memory records, leases, budgets, and resumable approval states only when the added machinery is justified.

## Validation

Run the repository checks:

```bash
python3 -m unittest discover -s tests -v
python3 skill/adaptive-agent-operating-system/scripts/validate_project.py --root .
python3 -m compileall -q skill/adaptive-agent-operating-system/scripts tests
```

Continuous integration runs the same checks on Python 3.10, 3.11, and 3.12.

## Maturity and proof boundary

The current release verifies:

- project-spine initialization and idempotency;
- required project/state structure;
- memory-record parsing and validation;
- JSON Schema syntax and stable canonical IDs;
- secret-pattern and absolute-path checks in the tracked source.

It does **not** yet prove broad ecosystem adoption, human-outcome improvement, or compatibility with every agent harness. Those are roadmap items and should be evaluated with real projects and disclosed evidence.

## Contributing

Issues, small reproducible examples, schema proposals, and harness adapters are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md), [SECURITY.md](SECURITY.md), and the [roadmap](ROADMAP.md) first.

Primary maintainer: [Prithvi Rey](https://github.com/prithvi-jpg).

## License

[MIT](LICENSE). External projects and publications referenced in the research notes remain under their own licenses and terms.
