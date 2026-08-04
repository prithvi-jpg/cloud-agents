# Work packets and orchestration

## Contents

1. Final-state contract
2. Packet template
3. Coordinator, builder, and verifier
4. Decomposition and parallelism
5. Typed trace
6. Long-horizon execution
7. Portability

## 1. Final-state contract

Use the Autonomous Execution Task principle:

- define a legible initial state;
- fix a constrained outcome;
- constrain the available action space;
- set an effort, time, attempt, or cost budget;
- provide visible diagnostic checks;
- keep final or held-out verification evaluator-owned;
- expose human steering and approval points;
- judge the real final state.

Do not give the worker a reference trajectory unless the procedure itself is being evaluated. More autonomy comes from a clearer environment contract, not a vaguer request.

## 2. Packet template

```yaml
task:
  id: stable-id
  title: human-readable title
  initial_state:
    canonical_sources: []
    artifacts: []
    verified_facts: []
  objective:
    final_state: observable change
    people_served: []
  constraints:
    in_scope: []
    non_goals: []
    quality_bar: []
    authority: []
  action_space:
    read: []
    write: []
    tools: []
    forbidden: []
  budget:
    effort: focused | investigative | frontier
    max_attempts:
    time_or_cost:
    checkpoint_triggers: []
  diagnostics:
    visible_checks: []
    feedback_policy:
  verification:
    acceptance: []
    held_out_owner:
    hard_gates: []
  steering:
    preview_points: []
    approval_points: []
    escalation_conditions: []
  receipt:
    artifacts: []
    evidence: []
    limitations: []
    next_state:
```

Use `assets/schemas/work-packet.schema.json` for the machine-readable required fields.

## 3. Coordinator, builder, and verifier

Use separate roles only when complexity or stakes earns them.

### Coordinator

- preserve the project objective and authority;
- create bounded packets;
- sequence dependencies;
- select capabilities;
- merge evidence;
- accept, correct, or escalate.

The coordinator does not accept another agent's success statement without inspecting the artifact and verifier evidence.

### Builder

- work only inside the packet;
- choose the implementation route unless procedure is constrained;
- create real artifacts;
- use visible diagnostics;
- record failures and observations;
- stop at approval gates or budget exhaustion.

### Verifier / refuter

- receive the artifact, criteria, and relevant source evidence;
- avoid the builder's persuasive rationale when possible;
- run claim-specific checks;
- attempt to falsify;
- return accept, correct, or escalate with evidence.

Do not use the same vague model prompt—“Did you do a good job?”—as verification.

## 4. Decomposition and parallelism

Treat decomposition as a proposal compiler, not an automatic task factory. Before creating work items:

1. inspect canonical project state and the real artifact/codebase;
2. identify work already complete, stale, duplicated, superseded, or incompatible;
3. choose the smallest coherent packet set—never force a numeric quota;
4. build the full proposed DAG and packet contracts in memory;
5. validate dependency semantics, cycles, acceptance criteria, authority, verification reachability, and mutable write-set conflicts;
6. preview when direction, cost, or human taste materially benefits;
7. materialize atomically or idempotently, with a recoverable partial-write strategy;
8. let the coordinator assign packets from authoritative state.

Do not recursively fan out before the parent direction is sufficiently proven. Use compact source pointers and state summaries instead of copying an ever-growing ancestor transcript into every child.

Decompose by:

- independent evidence domains;
- distinct artifacts;
- interfaces with explicit contracts;
- tests separable from implementation;
- parallel sources whose results can be merged objectively.

Do not parallelize:

- tightly coupled design choices before a direction exists;
- tasks sharing the same mutable files without coordination;
- trivial work;
- work where agents would duplicate context and create merge overhead.

Every delegated packet needs:

- outcome;
- exact scope;
- non-goals;
- source inputs;
- action boundary;
- definition of done;
- expected evidence;
- handoff format.

A task description is a brief, not merely a title. For consequential work include the observed problem or root cause, canonical evidence, expected files/surfaces, constraints, definition of done, verification command or method, and required delivery receipt.

Use a diagram when ownership, tools, state, approvals, retries, and handoffs would otherwise be difficult to understand.

## 5. Typed trace

Record observable events, not hidden reasoning:

```json
{
  "timestamp": "ISO-8601",
  "run_id": "stable id",
  "task_id": "stable id",
  "attempt_id": "stable id or null",
  "phase": "build",
  "actor": "builder",
  "event": "tool_call | observation | decision | artifact | check | approval | failure",
  "input_refs": [],
  "action": {},
  "result": {},
  "evidence_refs": [],
  "authority": "local_reversible",
  "idempotency_key": "required for effectful commands or null",
  "status": "ok | failed | blocked | needs_approval"
}
```

Preserve enough to reproduce and diagnose:

- exact inputs and versions;
- tool/action and effect class;
- observations;
- artifacts and hashes where useful;
- checks and results;
- approval receipts;
- attempt/budget state.

Do not expose or evaluate private hidden chain-of-thought.

## 6. Long-horizon execution

For long work:

- move tasks through validated states rather than free-form status prose;
- keep the work graph, task lifecycle, and worker-attempt lifecycle separate;
- keep task outcome separate from individual worker attempts;
- use one authoritative dispatcher or transactional command path;
- claim mutable work with a lease, owner, expiry, and heartbeat;
- append events so materialized state can be rebuilt;
- reconcile database, tracker, process, files, and lease before dispatch/resume;
- make approval a durable interruption with exact action, target, scope, and expiry;
- checkpoint at phase and failure boundaries;
- externalize current state rather than retaining the full conversation;
- preserve budget and attempt counts;
- support pause/resume;
- isolate risky or conflicting work;
- avoid allowing one long job to starve short work;
- use watchdogs to detect expired leases, silence, and repeated no-progress loops;
- stop repeated unproductive loops and reconsider framing or architecture.

A task dependency is satisfied by the declared successful outcome, not merely by any terminal/closed state. Model failed and canceled prerequisites explicitly. Keep retry, approval, recovery, and iteration loops in the runtime state machine/event log rather than creating circular task dependencies.

On resume, verify the environment has not drifted before continuing.

Use simulation or pre-mortem before irreversible or high-leverage choices:

1. predict direct result;
2. identify second-order effects and lock-in;
3. imagine failure and likely cause;
4. compare plausible paths;
5. add mitigation, checkpoint, or rollback.

Do not claim certainty from narrative simulation.

Read [long-horizon-runtime.md](long-horizon-runtime.md) before implementing a queue, dispatcher, watchdog, issue workflow, resumable worker, or multi-day runtime. Do not force those mechanisms into a one-session task.

## 7. Portability

Separate:

- portable task semantics;
- runtime adapter;
- tool schemas;
- context strategy;
- evaluator.

Record a run as a compound system. If the procedure should generalize, test the same packet under at least two relevant harness configurations.

Do not infer a model-only causal conclusion when harness, tools, effort, context management, or judge also changed.
