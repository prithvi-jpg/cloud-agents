# Evaluation, refutation, and recovery

## Contents

1. Completion contract
2. Evaluation stack
3. Universal evaluation envelope
4. Suite balance and validation discipline
5. Evidence-population integrity
6. Compound run manifest
7. Visible and held-out verification
8. Refuter loop
9. Failure classification and recovery
10. Checkpoint and completion receipt

## 1. Completion contract

Never claim completion without fresh evidence appropriate to the claim.

| Claim | Minimum evidence |
|---|---|
| code behavior | relevant tests, build, or reproducible real flow |
| research fact | directly supporting primary source and freshness |
| interface quality | rendered browser inspection, relevant interaction/accessibility checks |
| data result | source validation, transformation checks, reconciliation |
| multi-agent output | independent inspection of artifact and evidence |
| external action | explicit approval plus execution/readback receipt |
| procedural improvement | baseline comparison, representative and held-out cases, no authority regression |

Re-read acceptance criteria and inspect the actual artifact before saying done. State residual limitations.

## 2. Evaluation stack

Evaluate in order.

### Hard gates

- authority;
- privacy and credential handling;
- real artifact;
- build;
- runtime;
- core correctness.

A hard failure blocks completion and cannot be averaged away.

### Deterministic checks

- structure;
- behavior;
- state transitions;
- schemas;
- accessibility mechanics;
- performance;
- reproducibility.

### Artifact judgment

- source/code quality;
- feature completeness;
- factual fidelity;
- visual craft;
- interaction experience;
- task-specific rubric.

### Process judgment

- tool discipline;
- efficiency;
- context economy;
- recovery quality;
- communication and steering;
- source provenance;
- authority behavior.

### Held-out verification

- unseen scenarios;
- evaluator isolation;
- limited submissions;
- regression suite;
- adversarial or edge cases.

## 3. Universal evaluation envelope

Unify evaluator outputs through one interface, not one opaque reward number:

```yaml
hard_gates:
  authority: pass | fail
  privacy: pass | fail
  real_artifact: pass | fail
  build_runtime: pass | fail | not_applicable
metrics:
  outcome_fidelity: 0..1
  correctness: 0..1
  craft: 0..1
  interaction: 0..1
  efficiency: 0..1
  recovery: 0..1
  provenance: 0..1
task_rubric: []
evidence_refs: []
uncertainty: []
```

Deterministic execution checks, rendered visual review, rubric-conditioned judgment, agentic inspection, and human review may all emit this envelope. Each evaluator still needs a task-appropriate rubric and evidence contract.

Hard-gate failure blocks completion or promotion. Metric weights are suite-specific and versioned. A scalar may rank candidates only after the full metric vector, gate status, uncertainty, and failure distribution remain visible.

## 4. Suite balance and validation discipline

Stratify evaluation cases across:

- task and product domain;
- difficulty and horizon;
- workspace size/shape;
- harness, model, tool, and skill configuration;
- deterministic versus stochastic behavior;
- known failure class and unseen edge cases.

Balance evaluation batches when one category would dominate conclusions, but preserve the natural-distribution view separately. Training-style online data balancing is not needed for ordinary project execution.

For stochastic procedures:

- run repeated trials or seeds;
- retain every compound manifest;
- compare mean, variance, tail failures, and failure clusters;
- use multi-seed union coverage when different seeds expose different valid failure modes;
- never promote from one lucky trajectory.

If design-period metrics improve while validation-period metrics regress, treat it as overfitting. Audit metric leakage, correlated/redundant factors, evaluator gaming, and path dependence. Prune or simplify factors round by round, then rerun baseline and held-out validation. Do not lower thresholds to conceal failure.

## 5. Evidence-population integrity

A successful command is not proof that the intended evidence population ran. For material suites record and check:

1. **Population:** expected tests, fixtures, scenarios, rendered states, or review targets.
2. **Membership:** exact expected versus executed identities; qualify names when collisions are possible.
3. **Reachability:** the production command/recipe/CI path actually invokes the intended checks.
4. **Skip policy:** unexpected skips, zero discovered tests, or missing evidence artifacts fail closed.
5. **Sensitivity:** a canary, mutation, or red-arm proves the guard fails when the protected condition is broken.

Run build/compile checks on the committed/source tree before a generator or formatting step can repair it invisibly. Protect critical authority, security, and completion tests from deletion through manifest membership rather than trusting naming convention alone.

## 6. Compound run manifest

Record every factor that could materially explain a score:

```yaml
run:
  id:
  task_id:
  dataset_version:
  model:
  model_version:
  harness:
  harness_version:
  stable_kernel_version:
  phase_packet_version:
  capability_set: []
  effort_class:
  sampling:
  context_strategy:
  environment:
  visible_verifier:
  held_out_verifier:
  evaluator:
  attempts:
  cost:
  latency:
  artifact_receipt:
  evidence_population_manifest:
  executed_evidence_membership:
  negative_control:
  hard_gate_failures: []
  outcome:
  human_corrections: []
```

Use `assets/schemas/compound-run.schema.json` for required fields.

Describe a cross-harness leaderboard result as product-system evidence. Draw model-only conclusions only from controlled comparisons.

## 7. Visible and held-out verification

Visible diagnostics help the worker learn:

- build errors;
- test failures;
- validator messages;
- rubric categories;
- intermediate observations.

Held-out checks protect integrity:

- unseen examples;
- evaluator-owned criteria;
- hidden or private fixtures;
- independent readback;
- limited attempts.

Use held-out checks when:

- the worker can overfit a visible validator;
- reward hacking is plausible;
- a reusable skill is being promoted;
- safety/authority behavior must generalize;
- nondeterminism makes a single pass unreliable.

Do not leak held-out answers or reference trajectories into the worker packet.

## 8. Refuter loop

1. Define outcome, non-goals, criteria, and evidence.
2. Build the smallest real artifact that can be judged.
3. Run hard gates and deterministic checks.
4. Give a fresh verifier the artifact, rubric, and sources.
5. Return:
   - **accept** with claim-to-evidence links;
   - **correct** with a specific failed criterion;
   - **escalate** when a real tradeoff or authority choice belongs to the user.
6. Rerun affected checks after correction.

Use a separate verifier or fresh-context review when stakes, novelty, or irreversibility makes correlated error likely. Do not manufacture a verifier for trivial work.

For stochastic behavior:

- repeat representative trials;
- preserve each run manifest;
- report variance and failure distribution;
- do not promote from one lucky result.

## 9. Failure classification and recovery

When a check fails:

1. contain impact and preserve the trace;
2. classify:
   - misunderstood objective;
   - missing or stale context;
   - wrong framing/architecture;
   - tool/environment fault;
   - implementation defect;
   - quality/craft gap;
   - evaluator or test defect;
   - reward/validator gaming;
   - changed requirement;
3. return to source evidence;
4. form one corrective hypothesis;
5. test it;
6. update state with result and next action.

Do not stack random fixes. If repeated attempts fail, question the framing or architecture rather than adding complexity by inertia.

Common long-horizon failure patterns:

- incomplete final step;
- correct local action but wrong overall strategy;
- prolonged unproductive debugging loop;
- missing final verification;
- context drift after compaction;
- declaring success from self-report;
- overfitting to one harness or validator.

Turn repeated observed failures into eval cases before changing durable procedure.

## 10. Checkpoint and completion receipt

Checkpoint:

```md
## Objective and phase
## Confirmed evidence
## Decisions and rejected paths
## Assumptions, risks, and open questions
## Authority and approval state
## Budget / attempts consumed
## Verification state
## One next action or hypothesis
```

Completion receipt:

```md
# Result

## Delivered artifacts
## Claim-to-evidence matrix
## Verification performed
## Expected and executed evidence population
## Negative-control / guard sensitivity
## Hard gates
## Human approvals / external receipts
## Delivery / readback receipt
## Known limitations
## State and one next action
```

The next agent must be able to resume without rereading the transcript or repeating verified work.
