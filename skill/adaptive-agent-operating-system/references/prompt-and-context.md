# Prompt and context engineering

## Contents

1. Prompt assembly
2. Stable versus dynamic information
3. Phase-packet synthesis
4. Tool and observation representation
5. Context economy and compaction
6. Harness variation and portability
7. Anti-patterns

## 1. Prompt assembly

Assemble a meaningful task from four layers:

```text
Stable kernel
  → compact project state
    → current phase packet
      → selected dynamic capabilities and observations
```

Do not solve missing project state by growing the stable system prompt.

### Stable kernel

Include only cross-project behavioral invariants:

- source hierarchy;
- professional-intelligence charter;
- autonomy and authority semantics;
- context discipline;
- verification and completion behavior.

### Compact project state

Include only current truth:

- objective;
- phase;
- confirmed decisions;
- relevant evidence pointers;
- risks and assumptions;
- one next action.

### Phase packet

Include:

- immediate final-state goal;
- relevant source inputs;
- constraints and non-goals;
- allowed action space;
- effort and attempt budget;
- visible checks;
- held-out/evaluator-owned proof;
- human steering and approval points.

### Dynamic edge

Include:

- selected skill instructions;
- tools and schemas;
- retrieved passages;
- current observations;
- subagent results;
- artifact/test receipts.

Remove or stop prioritizing dynamic information that no longer serves the phase.

## 2. Stable versus dynamic information

Keep stable instructions stable within a run to reduce conflict and context churn. Place task-specific or one-shot options late, after durable history/state. Announce new tools or capabilities only when they become relevant.

Do not rebuild the entire system prompt when:

- a tool becomes available;
- one phase ends;
- a new source is retrieved;
- a subagent returns;
- a test fails.

Update the phase packet or dynamic observations instead.

When the user changes a durable rule, record the change explicitly and update the correct project/skill layer rather than silently mixing old and new instructions.

## 3. Phase-packet synthesis

Convert a vague request into a packet by asking internally:

1. What observable state should change?
2. Which source facts are canonical?
3. Which constraints and non-goals matter now?
4. What is the allowed action space?
5. How much effort is justified?
6. Which uncertainty should be tested?
7. What evidence can reject completion?
8. Where can the human steer or must the human approve?

Do not add process steps that do not help answer one of these questions.

For explore mode:

- request structurally distinct options;
- specify comparison dimensions;
- require evidence or deciding experiments;
- set a convergence condition.

For commit/build mode:

- name the selected direction;
- freeze rejected paths unless new evidence appears;
- define the real artifact and completion proof;
- permit autonomous local iteration.

## 4. Tool and observation representation

Represent actions and results explicitly:

```json
{
  "call_id": "stable-index",
  "capability": "tool-or-skill",
  "purpose": "decision or state change unlocked",
  "effect": "read | local_write | external_write | destructive",
  "arguments": {},
  "result": {},
  "evidence_refs": [],
  "status": "ok | failed | approval_required"
}
```

Use typed arguments where the harness supports them. Keep response text, tool calls, and tool results distinct. Parallel calls need stable IDs so results cannot be confused.

Use tools to create observations:

- inspect real state;
- retrieve evidence;
- execute code;
- render output;
- measure behavior;
- read back external results after approved action.

Do not call tools for performance theater.

## 5. Context economy and compaction

Treat context as scarce.

Before loading:

- prefer metadata and search over full files;
- load one-to-three relevant detailed procedures;
- read the exact source needed for a claim;
- avoid duplicated summaries.

Before compaction:

- update STATE;
- preserve exact evidence references;
- record decisions and rejected paths;
- record budget/attempt state;
- name one next hypothesis/action.

After compaction or resume:

- reconstruct from canonical state;
- validate artifact/environment drift;
- do not treat compressed prose as stronger than original source;
- do not rerun verified work without cause.

Long context is not permission to retain noise. Context management can outperform using a maximum window without organization.

## 6. Harness variation and portability

A reusable procedure should not depend accidentally on:

- one tool name;
- one system-prompt phrase;
- one memory convention;
- one compaction mechanism;
- one subagent protocol;
- one response/tool-call syntax.

Keep portable:

- objective;
- state;
- constraints;
- authority;
- work packet;
- evidence;
- evaluator contract.

Keep adapter-specific:

- tool schemas;
- prompt syntax;
- channel conventions;
- host permissions;
- context APIs;
- sandbox lifecycle.

When portability matters, run the same packet through more than one harness and record the full compound configuration.

## 7. Anti-patterns

Avoid:

- one mega-prompt containing every skill;
- “act as the world's best expert” without expert practice or evidence;
- vague “work hard” instructions without effort routing and proof;
- repeating the entire constitution in every task;
- forcing a full interview when the project already answers the questions;
- leaking the reference solution into autonomous tasks;
- treating model self-report as completion;
- using long context as a substitute for state;
- mixing secrets into prompts;
- hiding authority or tool effects inside prose;
- preserving abandoned ideas as active requirements.
