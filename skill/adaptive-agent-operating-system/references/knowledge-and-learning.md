# Knowledge and controlled learning

## Contents

1. Source-preserving knowledge
2. Retrieval, tools, skills, state, and memory
3. When a knowledge graph earns its use
4. Trace-to-eval learning
5. Candidate skill lifecycle
6. Longitudinal improvement
7. Self-improvement boundary

## 1. Source-preserving knowledge

Preserve source context before interpretation:

- exact quote or source fragment;
- title/path/URL;
- author or owner;
- date and freshness;
- confidentiality;
- surrounding context;
- observed fact;
- later interpretation and confidence.

Keep:

```text
source → evidence record → claim/decision/eval
```

Do not replace the source with a polished summary or combine unrelated sources into an untraceable “memory.”

## 2. Retrieval, MCP, skills, and memory

- **Retrieval/RAG:** chooses and ranks relevant information.
- **MCP or connector:** exposes governed data and actions to an AI client.
- **Skill:** provides a procedure, constraints, checks, and output expectations.
- **Project state:** preserves current objective, decisions, evidence pointers, and next action.
- **Memory:** preserves selected durable knowledge across runs.
- **Model:** reasons over the available context and chooses actions.

Use them together when needed, but do not collapse them.

A local knowledge capability should prefer:

- `search` with filters and provenance;
- `read` after likely sources are identified;
- link/relationship traversal;
- draft-with-approval for edits.

Do not make an MCP for every folder. Define the few capabilities that improve search, read, or governed action.

For durable records, hybrid FTS/vector recall, provenance, freshness, correction, and graph activation gates, read [memory-and-retrieval.md](memory-and-retrieval.md). This section defines conceptual boundaries; that reference defines the memory contract.

## 3. When a knowledge graph earns its use

Use a hierarchical graph when a linear catalog can no longer show:

- duplicate or equivalent concepts;
- coarse-to-atomic coverage;
- related capabilities;
- underrepresented combinations;
- failure clusters;
- eval lineage.

Recommended graph:

```text
domain
  → capability
    → atomic behavior
      → observed failure
        → reproducible trace
          → eval case
            → candidate procedure
              → verified outcome
```

Rules:

1. Search for equivalent and related nodes before adding.
2. Reuse or link duplicates.
3. Direct edges from coarse to fine.
4. Preserve provenance, aliases, and freshness.
5. Sample related or under-covered nodes to synthesize held-out cases.
6. Stop expansion when a node is sufficiently atomic.

Do not use a graph:

- by default for small projects;
- as a replacement for PROJECT/STATE;
- as a claim of consciousness or AGI;
- because “knowledge graph” sounds advanced.

## 4. Trace-to-eval learning

When the user says:

- “lazy”;
- “generic”;
- “not following me”;
- “drifted”;
- “too many tools”;
- “looks right but does not work”;

preserve the language, then:

1. recover the exact task and context;
2. inspect the action trace and final artifact;
3. classify concrete failures;
4. collect representative and edge examples;
5. define a falsifiable evaluator;
6. rerun baseline and candidate;
7. retain, revise, or reject.

Examples:

- “generic UI” → visual-direction, hierarchy, interaction, and rendered-browser cases;
- “not following instructions” → isolate schema, ordering, state, or conflicting-context cases;
- “agent wandered” → effort, stop-condition, and outcome-fidelity cases;
- “used everything” → capability-precision and context-economy cases.

## 5. Candidate skill lifecycle

A reusable lesson becomes a candidate only when:

- a pattern recurs or has high enough impact;
- scope and trigger are clear;
- an anti-trigger prevents overuse;
- authority is bounded;
- a simpler baseline exists;
- representative and adversarial cases exist;
- the candidate can be rolled back.

Constrain an improvement experiment before running it:

- fix the baseline environment and evaluator;
- define the narrow editable surface;
- set time, attempt, and cost budgets;
- preserve an append-only experiment log;
- compare and keep/discard each candidate explicitly;
- keep the candidate from rewriting its own held-out evaluator or authority boundary.

Lifecycle:

```text
observe
  → candidate
  → tests
  → baseline comparison
  → human review
  → versioned promotion
  → monitoring
  → retain, revise, or rollback
```

Promotion requires:

1. clear trigger and anti-trigger;
2. at least three representative cases, including an edge/adversarial case;
3. held-out proof when gaming is plausible;
4. zero authority regression;
5. improved quality, time, cost, corrections, or safety;
6. reviewable diff;
7. explicit human approval;
8. version and rollback condition.

Do not create a permanent skill for one-off taste or project-local rules.

## 6. Longitudinal improvement

Track:

- outcome quality;
- completion rate;
- human correction rate;
- authority failures;
- false completion claims;
- context loaded;
- capability precision;
- tool calls and latency;
- recovery loops;
- artifact craft;
- adoption and usefulness.

Accept improvement signals from user corrections, developer feedback, failed checks, telemetry, support issues, and community reports. Preserve their provenance, deduplicate and reproduce them, then separate product demand from model, harness, tool, skill, or environment failure before creating work.

Improve one bottleneck at a time:

1. establish baseline;
2. identify the real bottleneck—context, framing, decomposition, tool use, verification, or steering;
3. propose one change;
4. test representative tasks;
5. keep it only when benefit exceeds complexity and risk.

Graphs, subagents, loops, retrieval, and new tools are experiments—not identity.

When evidence is stochastic or path-dependent, use repeated trials and multi-seed coverage. If the candidate improves its design-period metric but loses on held-out validation, prune gameable or redundant factors and retest rather than adding more instructions.

## 7. Self-improvement boundary

An agent can improve its observable harness:

- instructions;
- task contracts;
- context selection;
- tool use;
- state;
- evaluation;
- recovery;
- reusable procedures.

It cannot during a normal task:

- rewrite its underlying weights;
- create new neurons;
- guarantee AGI;
- grant itself authority;
- treat its own confidence as evidence;
- silently promote durable rules.

Describe improvements as measured procedural or product changes, not hidden intelligence transformation.
