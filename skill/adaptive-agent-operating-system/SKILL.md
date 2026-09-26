---
name: adaptive-agent-operating-system
description: Use Agent Systems Foundry for multi-session or consequential agent work that needs recoverable project state, bounded authority, work packets, or evidence-backed completion. Use when starting or resuming such work, or evaluating a durable skill or runtime change. Skip routine one-step edits.
---

# Agent Systems Foundry

Use the smallest process that gives the work a clear outcome, safe authority, and proof of completion. Read only the references that the current task needs.

## Orient

1. Follow the user's instructions and applicable `AGENTS.md`. Read `docs/agent/PROJECT.md` and `docs/agent/STATE.md` when they exist and matter to the task. Inspect the actual files, tools, and source evidence before treating a claim as current.
2. Separate user requirements, observed facts, inferences, assumptions, and proposals. Later user edits supersede earlier plans; preserve source provenance.
3. Match effort to the work. Act directly on focused, reversible tasks. Investigate uncertainty that could change a meaningful decision. Use checkpoints and budgets only for long or consequential work.

For a new project that needs durable state, keep the spine small: `AGENTS.md` for stable rules, `docs/agent/PROJECT.md` for the outcome and acceptance contract, and `docs/agent/STATE.md` for current truth and the next action. Read [project-and-context.md](references/project-and-context.md) before creating or restructuring it. The scripts in `scripts/` can initialize and validate this spine without overwriting existing files.

## Work within authority

- Define the result and a check capable of disproving completion. Choose the route while working; do not prescribe a reference trajectory when the result matters more than the steps.
- Explore and make scoped, reversible local changes autonomously. Prepare a concrete preview and obtain explicit scoped approval before external or consequential changes. A skill, memory policy, hook, or other durable behavior change needs a reviewed candidate, evaluation, version, and rollback.
- Delegate only independent, bounded work. Keep the main agent responsible for synthesis and verification.
- Keep canonical project state portable. Put Codex, Claude, model, tool, and provider details in adapters. Select skills and tools just in time instead of loading the full catalog.

For a task that must survive restarts or handoffs, record its state, attempts, evidence, approval wait, and recovery route. Add leases, event logs, or graph structure only when the horizon or concurrency requires them. See [work-packets-and-orchestration.md](references/work-packets-and-orchestration.md) and [long-horizon-runtime.md](references/long-horizon-runtime.md).

## Verify and close

- Inspect the artifact and run checks proportional to the change. Use a meaningful negative control for validation code whose false success would matter. Avoid repeating broad checks after the relevant gates pass.
- Treat a model result as evidence about the whole model, harness, context, tools, skill version, and verifier. Do not attribute a result to one model when those factors changed together.
- Update `STATE.md` after a material phase change, verified result, failure, or handoff. Close with the delivered result, evidence, material limits, and one next action.

## Read a reference when its trigger applies

| Trigger | Reference |
| --- | --- |
| Project setup, source hierarchy, checkpoints, or recovery of context | [project-and-context.md](references/project-and-context.md), [prompt-and-context.md](references/prompt-and-context.md) |
| Autonomy, effort, approvals, or capability choice | [autonomy-effort-and-routing.md](references/autonomy-effort-and-routing.md) |
| Choosing between GPT-6 Astra/Sol, Claude Fable, or harnesses | [model-and-harness-routing.md](references/model-and-harness-routing.md) |
| Deep reasoning, product judgment, or a high craft bar | [expert-reasoning-and-craft.md](references/expert-reasoning-and-craft.md) |
| Work packets, delegation, multi-session runtime, or recovery | [work-packets-and-orchestration.md](references/work-packets-and-orchestration.md), [long-horizon-runtime.md](references/long-horizon-runtime.md), [evaluation-and-recovery.md](references/evaluation-and-recovery.md) |
| Frontend or interactive artifact | [frontend-and-hci.md](references/frontend-and-hci.md) |
| Memory or skill learning | [memory-and-retrieval.md](references/memory-and-retrieval.md), [knowledge-and-learning.md](references/knowledge-and-learning.md) |
| Adapters, research basis, or the full system map | [runtime-and-adapters.md](references/runtime-and-adapters.md), [research-basis.md](references/research-basis.md), [foundry-system-map.md](references/foundry-system-map.md) |
