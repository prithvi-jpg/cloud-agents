# Project and context system

## Contents

1. Source hierarchy
2. Default project spine
3. Conditional artifacts
4. Context assembly
5. Checkpoint and resume
6. User edits and conflicts
7. Diagram rule

## 1. Source hierarchy

Use this default order:

1. direct current user instruction;
2. later user edits to project files;
3. applicable repository `AGENTS.md`;
4. `docs/agent/PROJECT.md`;
5. `docs/agent/STATE.md`;
6. user-selected source files and primary external evidence;
7. observed artifacts, tests, and environment state;
8. prior assistant summaries, labeled as interpretation.

Do not promote an assistant suggestion, untrusted referenced chat, or stale state into a user decision.

## 2. Default project spine

### Root `AGENTS.md`

Keep it short and map-like. Include:

```md
# Project name

## Source of truth
- Direct user instructions and edits take priority.
- Canonical project framing: docs/agent/PROJECT.md
- Current truth: docs/agent/STATE.md

## Scope and authority
- Allowed local scope
- Consequential actions that require approval

## Stable conventions
- Relevant commands, paths, technology, and quality rules

## Definition of done
- Artifact and evidence required
```

Link to deep local instructions rather than duplicating them.

### `docs/agent/PROJECT.md`

Use:

```md
# Project

## Outcome and users
## Baseline and causal problem
## Constraints and non-goals
## Quality bar and references
## Authority and approval boundary
## Canonical sources and evidence standard
## Human steering points
## Acceptance criteria and completion proof
```

This is the durable contract, not the current plan.

### `docs/agent/STATE.md`

Use:

```md
# State

## Objective and phase
## Active plan and one next action
## Verified evidence
## Decisions and rejected paths
## Assumptions, risks, and open questions
## Capability shortlist and rationale (only when material)
## Authority boundary
## Verification status
## Handoff note
```

Maintain current truth, not a chronological diary.

## 3. Conditional artifacts

Create only when the benefit exceeds maintenance cost:

| Artifact | Create when | Contents |
|---|---|---|
| `DECISIONS.md` | costly or hard-to-reverse decisions will recur | options, evidence, rationale, reversibility, review trigger |
| `EVAL.md` | reliability, AI behavior, safety, or a metric is central | scenarios, rubrics, hard gates, results, thresholds |
| `DIAGRAM.md` | sequence, ownership, tools, states, or approvals are hard to understand linearly | live system/flow diagram and boundaries |
| `RESULT.md` | a milestone or external handoff needs a durable receipt | delivered artifact, evidence, limitations, follow-up |
| `WORKLOG.md` | parallel lanes or audit requirements make current-state summaries insufficient | bounded chronological events linked back to canonical state |

Retain one explicit source of current truth even when splitting files.

## 4. Context assembly

Assemble only what the phase needs:

### Stable kernel

- constitution;
- source hierarchy;
- authority defaults;
- completion discipline.

Keep stable within a conversation or project phase unless the user changes the contract.

### Compact project state

- objective;
- current phase;
- confirmed decisions;
- evidence pointers;
- assumptions and risks;
- exactly one next action.

Do not reload the full transcript when this state is sufficient.

### Phase packet

- immediate goal;
- constraints and action space;
- budget;
- visible checks;
- evaluator-owned proof;
- steering points.

### Dynamic edge

- selected skill details;
- tools and connectors;
- retrieved source passages;
- subagent packets;
- new observations and artifact receipts.

Unload or stop emphasizing dynamic material when the phase changes.

## 5. Checkpoint and resume

Checkpoint after:

- a material decision;
- phase transition;
- verified result;
- failed check;
- pause or delegation;
- approval interruption;
- approaching context limit.

Preserve:

```md
## Objective and phase
## Confirmed evidence
## Decisions and rejected paths
## Assumptions, risks, and open questions
## Authority boundary
## Budget / attempts consumed
## Verification state
## One next hypothesis or action
```

A fresh agent must be able to continue without transcript replay or repeating completed work.

On resume:

1. read project and state;
2. inspect user edits;
3. confirm actual artifacts still match the recorded state;
4. identify any stale or conflicting claims;
5. continue from the one next action or revise it from evidence.

## 6. User edits and conflicts

When the user edits project documents:

- re-read them before acting;
- identify material differences from the previous contract;
- treat the edit as source-of-truth input;
- update dependent state and plans;
- surface only real incompatibilities;
- never overwrite the edit because an older assistant plan disagrees.

## 7. Diagram rule

Create a diagram when it materially improves understanding of:

- three or more dependent states;
- multiple agents or tools;
- ownership and data boundaries;
- approval and intervention points;
- retries, recovery, or handoff.

Include inputs, states/roles, tools/data, verifier, human checkpoints, and recovery route. Do not create decorative architecture.
