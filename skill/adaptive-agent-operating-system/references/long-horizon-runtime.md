# Long-horizon runtime, dispatch, and recovery

## Contents

1. Boundary
2. Task and attempt state machines
3. Dispatcher and lease invariants
4. Events, checkpoints, and replay
5. Monitoring, watchdog, and recovery
6. Self-testing and verification routing
7. Human interruption and authority
8. Multi-source evolution
9. Scaling and interoperability

## 1. Boundary

The portable skill defines runtime invariants. A separate runtime implements queues, transactions, workers, issue adapters, browser sessions, and dashboards.

Use the runtime for multi-hour, multi-session, multi-task, crash-recoverable, scheduled, or externally integrated work. A normal scoped task does not need a dispatcher or database.

## 2. Task and attempt state machines

Model three different structures explicitly:

- **work graph:** prerequisites, hierarchy, related/duplicate links, artifacts, and evidence;
- **task lifecycle:** whether a work item is draft, eligible, claimed, verified, or terminal;
- **attempt lifecycle:** what one worker execution is doing and why it stopped.

Do not encode retries, approval waits, or self-improvement loops as circular dependency edges. A terminal failure/cancellation does not satisfy a prerequisite unless the work contract explicitly defines that outcome as sufficient.

Recommended task states:

```text
draft
ready
leased
active
waiting_approval
verifying
retry_wait
stalled
succeeded
failed
canceled
released
```

Recommended attempt states:

```text
preparing_workspace
building_packet
launching_worker
initializing_session
streaming
finishing
succeeded
failed
timed_out
stalled
canceled_by_reconciliation
```

Define an explicit transition table. Reject invalid transitions. Keep task outcome separate from one worker attempt so failed attempts can be diagnosed and retried without corrupting task truth.

Separate coarse computed outcome, asserted workflow stage, and adapter-native status when integrating external trackers. Preserve native values losslessly instead of forcing all three meanings into one status field.

## 3. Dispatcher and lease invariants

- One dispatcher or transactional command path owns scheduling mutations.
- A task has at most one valid execution lease per mutable workspace.
- Every lease records owner, scope, acquired time, expiry, and heartbeat.
- Reconcile tracker, database, process, and workspace state before dispatch.
- Recheck eligibility inside the transaction that claims the task.
- Derive eligibility from canonical stage/outcome, dependency success, holds, schedule, authority, budget, and required inputs; never trust a stale `ready` label alone.
- Use compare-and-swap/version checks for the ownership mutation, then attach a distinct expiring execution lease with heartbeat and attempt identity.
- Use idempotency keys for effectful commands and external writes.
- Prevent one long task from starving short or urgent work.
- Carry attempt, time, cost, tool-call, and context budgets.
- Separate readiness from permission: a ready task may still wait at an approval gate.

Issue trackers may be an intake/visibility adapter. They are not automatically the authoritative run database.

Prefer a progressive deployment ladder: prove the normalized contract in an embedded local store first, then preserve that client/domain contract when moving to a remote authenticated service. External adapters should carry source identity/version, representability limits, and a lossless native payload for readback and round-trip fidelity.

Use `assets/schemas/task-state.schema.json` for a normalized task snapshot and `assets/schemas/run-event.schema.json` for events.

## 4. Events, checkpoints, and replay

Append observable events such as:

```text
task_created
task_claimed
lease_renewed
attempt_started
tool_called
artifact_written
check_failed
approval_requested
approval_resolved
attempt_stalled
retry_scheduled
verification_passed
task_completed
```

Each event needs a stable ID, task/run/attempt IDs, timestamp, actor, state transition, effect class, evidence pointers, idempotency key when applicable, and result.

Materialized current state must be rebuildable from the event stream plus canonical project files. Checkpoint at phase changes, verification outcomes, approval interruptions, budget boundaries, and context/sandbox handoffs.

Keep a best-effort live UI stream separate from the durable event log. A stream may drop, reconnect, or restart its sequence; the client must detect gaps and repair from an authoritative snapshot. Time- or dependency-derived readiness may require reconciliation/polling even when no mutation event fires.

On resume:

1. reload canonical `PROJECT.md` and `STATE.md`;
2. replay or read the latest materialized task state;
3. reconcile environment and files against the checkpoint;
4. invalidate expired leases;
5. revalidate external facts or approvals that may have changed;
6. continue from one explicit next hypothesis/action without repeating verified work.

## 5. Monitoring, watchdog, and recovery

Monitor:

- heartbeat age;
- lease expiry;
- time since last meaningful observation or artifact change;
- repeated identical tool/error sequences;
- budget consumption;
- queue starvation;
- failed checks and regressions;
- approval wait duration;
- environment drift.

The watchdog may stop, release, or schedule a classified retry. It must not independently invent broad new authority.

Recovery sequence:

1. contain effects and preserve the trace;
2. classify objective, context, framing, tool, environment, implementation, craft, evaluator, or authority failure;
3. reconcile actual state;
4. form one corrective hypothesis;
5. retry within budget and with backoff;
6. escalate or fail visibly when the budget or authority boundary is reached.

After repeated no-progress attempts, question the framing or architecture instead of extending the loop.

## 6. Self-testing and verification routing

Route checks from changed surfaces:

```text
format/type/static
  → unit
  → build/package
  → integration/E2E
  → browser/desktop lifecycle
  → rendered HCI/craft review
  → independent completion receipt
```

Before accepting a green suite, verify expected test/evidence population, executed membership, command-path reachability, and negative-control sensitivity where omission could produce a false pass. Compile/build the committed artifact before any generator or formatter can silently repair missing output.

Not every change runs every test. The router must explain applicability and never skip a required hard gate for cost alone.

When a test fails, route the artifact, failed criterion, environment, trace, and next hypothesis back to the owning task. A repair is not complete until affected and regression checks rerun.

Transition to `succeeded` only when both product/artifact verification and the required delivery/readback evidence exist. A local file, commit, PR, deployment, message, or external record has different receipt semantics; “worker says done” is never the receipt.

## 7. Human interruption and authority

`waiting_approval` is a durable state containing:

- exact proposed action;
- target and effect;
- reason;
- preview/diff;
- risk and reversibility;
- requested scope and expiry;
- what the runtime may continue doing while waiting.

Approval applies only to that declared scope. Resume must verify the action is still current and has not already executed. Rejection or correction becomes an event and updated packet, not an error to work around.

## 8. Multi-source evolution

Convert user corrections, developer feedback, telemetry, support issues, and community reports through the same intake funnel:

```text
signal
  → source-preserving record
  → deduplicate / cluster
  → reproduce
  → classify product, harness, skill, or environment failure
  → work packet
  → implementation
  → regression case
  → verified release
```

Do not treat volume as truth. Weight signals by source, reproducibility, impact, recency, and affected users. Keep product demand separate from model/harness capability failure.

## 9. Scaling and interoperability

Scale independent axes deliberately:

- task: single step to multi-day portfolios;
- workspace: one file to heterogeneous repositories;
- harness: model, tools, skills, context policy, and version;
- verifier: deterministic, rendered, rubric, human, and held-out;
- environment: local, sandbox, browser, desktop, or remote service.

Record the cross-product in the compound run manifest so improvements are not misattributed.

Use A2A only when independently deployed agents need capability discovery, async task IDs, artifacts, streaming/polling, and durable status. Use host-native local delegation for workers inside one runtime. Use MCP for agent-to-tool/data access. These boundaries may coexist but should not be collapsed.
