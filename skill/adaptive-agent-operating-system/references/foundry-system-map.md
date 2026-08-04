# Agent Systems Foundry system map

## Contents

1. System thesis
2. Historical requirements
3. Layered architecture
4. Operating state machine
5. Accepted defaults
6. Product boundary and build order
7. Human experience requirements
8. Non-goals

## 1. System thesis

Agent Systems Foundry is a portable, source-preserving control plane for ambitious human-agent work. It turns evolving human intent into visible project state, routes the smallest competent capabilities, executes bounded work packets, pauses at consequential decisions, verifies claims with task-appropriate evidence, and proposes procedural improvements through an evaluated and reversible skill lifecycle.

It combines:

- a behavioral constitution;
- a durable project-control model;
- a provenance and evidence layer;
- a capability registry and router;
- a typed execution loop;
- an authority and approval policy;
- an evaluation and controlled-learning pipeline;
- a human steering surface;
- thin platform adapters.

The installed skill is the portable constitution and bootstrap. It is not the database, runtime, UI, connector broker, or evaluation history.

## 2. Historical requirements

The design preserves four stages of user intent:

### Collaborative partner and north star

- Work as a peer collaborator that asks useful questions and challenges assumptions.
- Reduce overwhelm to one evidence-backed next action.
- Support research → framing → PRD → prototype → evaluation → stakeholder artifact.
- Take practical action inside permission boundaries.

### AI Product Engineer Studio

- Preserve every source idea while sequencing active, next, backlog, and unresolved work.
- Make HTML the primary human reading surface.
- Give every long surface an actionable journey and next route.
- Avoid generic green AI/SaaS dashboards.
- Use warm paper, ink, yellow/orange signals, editorial typography, physical structure, and restrained motion.
- Show why a recommendation matters and what evidence supports it.

### Capability and skill-system design

- Separate skills, tools, MCPs, APIs, retrieval, memory, and agent roles.
- Route one-to-three relevant capabilities just in time.
- Give each task a subspec and acceptance proof.
- Use a coordinator → bounded implementer → verifier → accept/correct/escalate loop when complexity earns it.
- Scale verification and approval with autonomy and blast radius.
- Use previews when they create execution or human-steering value.

### Operating constitution and controlled improvement

- Infer relevant expertise instead of relying on fake personas.
- Use first principles, meaningful divergence, systems thinking, and human-centered judgment.
- Preserve context with compact checkpoints and handoffs.
- Model downstream effects before consequential choices.
- Treat architectures and procedures as hypotheses to test against simpler baselines.
- Propose candidate skills from repeated validated patterns; never silently rewrite durable rules.
- Remain stubborn about the outcome and flexible about the path.

## 3. Layered architecture

| Layer | Owns | Must not own |
|---|---|---|
| Constitution kernel | truth-seeking, creativity, human agency, authority defaults, completion discipline | project-specific plans, user data, every tool instruction |
| Project control plane | outcome, baseline, constraints, quality, phase, decisions, risks, next action | transcript diary or global capability catalog |
| Evidence ledger | quotes, files, URLs, facts, freshness, test results, confidentiality | assistant interpretation presented as source truth |
| Durable memory | scoped preferences, decisions, facts, lessons, failures, procedures, provenance, freshness, correction | raw transcript archive or embedding-only truth |
| Retrieval projections | FTS, optional vectors, explicit/inferred links, rebuildable indexes | canonical records, authority, or automatic context injection |
| Capability registry/router | skills, tools, plugins, MCPs, subagents, value, cost, risk, availability, freshness | all detailed instructions in permanent context |
| Orchestration runtime | task/attempt FSMs, typed packets, leases, events, delegation, retries, checkpoints, watchdog, reconciliation | vendor-owned canonical project truth |
| Work graph and adapters | normalized tasks, derived readiness, dependencies, source/native fidelity, atomic claims, graph analysis | retry loops, approval loops, or lossless source truth erased by normalization |
| Authority gate | scope, consent, credentials, approval, audit, cancellation, recovery | natural-language-only security |
| Evaluation/learning lab | scenarios, traces, hard gates, graders, held-out cases, baselines, candidate skills | self-congratulation or hidden-reasoning surveillance |
| Human steering UI | journey, phase, why, evidence, preview, permission, correction, receipt, next action | generic telemetry or raw Markdown-only consumption |
| Runtime adapters | Codex, Hermes, Claude, MCP, framework-specific prompt and tool conventions | portable project semantics |

## 4. Operating state machine

```text
Orient
  ↓
Frame ──missing evidence──→ Research
  ↓                         ↓
Explore ←───────────────────┘
  ↓
Commit
  ↓
Build
  ↓
Verify ──failure──→ Recover ──framing wrong──→ Frame
  │                    └────implementation wrong──→ Build
  ├─ consequential ──→ Approve ──approved──→ Deliver
  └─ local/reversible ──────────────────────→ Deliver
                                               ↓
                                            Observe
                                               ↓
                                             Learn
```

### State semantics

- **Orient:** find instructions, current truth, evidence, environment, and authority.
- **Frame:** align outcome, quality, constraints, non-goals, steering, and proof.
- **Research:** resolve consequential uncertainty with primary evidence.
- **Explore:** create meaningfully different approaches when the decision warrants it.
- **Commit:** choose, record rationale, and stop reopening the decision without new evidence.
- **Build:** execute bounded packets and create real artifacts.
- **Verify:** try to refute the result against explicit criteria.
- **Approve:** interrupt before consequential external or irreversible action.
- **Deliver:** return artifact, receipt, limitations, and state.
- **Observe:** collect corrections, adoption, time, cost, and failures.
- **Learn:** propose evaluated procedural changes.

## 5. Accepted defaults

These are accepted design inputs:

### D01 — Runtime

Use portable contracts with a Codex-first execution adapter. Add other adapters only after one complete loop works.

### D02 — Consequential permissions

Use per-action approval by default. Later allow narrow standing policies only with explicit targets, limits, expiry, and revocation.

### D03 — Skill promotion

Allow automatic candidate proposals. Require evaluation, a reviewable diff, explicit human approval, versioning, and rollback for promotion.

### D04 — Project state

Default to `AGENTS.md`, `docs/agent/PROJECT.md`, and `docs/agent/STATE.md`. Split decisions, evals, diagrams, or results only when they earn maintenance.

### D05 — Mutable runtime state

Prefer a transactional store plus append-only events for a future runtime, with readable project exports. Do not force that infrastructure into ordinary projects.

### D06 — First product

Build one Foundry Workbench vertical slice before broad personal-assistant integrations or a full capability catalog.

### D07 — Memory

Keep evidence and state project-local first. Store durable cross-session memory as scoped, human-readable, versionable records with provenance, trust, privacy, freshness, supersession, and deletion. Use SQLite/FTS, optional vectors, and optional graphs only as rebuildable retrieval projections whose value is measured on held-out recall cases.

### D08 — Creative autonomy

Use **wide mind, evidence-bound convergence, bounded action**:

- wide cognitive and exploratory freedom;
- high reversible local execution after alignment;
- explicit approval for consequential actions;
- candidate-only durable self-modification.

## 6. Product boundary and build order

### First: Foundry Workbench

Prove:

- project initialization;
- evidence ledger;
- one final-state work packet;
- shadow capability shortlist;
- scoped local execution;
- compound run manifest;
- visible and held-out verification;
- recovery;
- claim-to-evidence receipt;
- self-contained journey reader.

After that slice passes, add the memory/runtime foundation in evidence-gated stages:

1. Markdown records plus validation and FTS baseline;
2. hybrid vector recall only after held-out gain;
3. transactional task/event state, lease, watchdog, reconciliation, and resume;
   - keep work graph, task lifecycle, and attempt lifecycle separate;
   - derive readiness and recheck it in an atomic compare-and-swap claim;
   - require task-specific artifact plus delivery/readback proof before success;
4. eval flywheel and candidate-skill lab;
5. graph, simulation, WebMCP, or A2A only for proven workflows.

### Later modules

- **Foundry Lab:** capability observatory, failure clusters, evals, candidate-skill lifecycle.
- **Foundry Home:** one source-backed personal next action with evidence, uncertainty, correction, and permission state.
- **Foundry Studio:** research-to-product workflow and source-preserving learning/archive surface.

Do not split these into separate products until repeated use proves distinct ownership or deployment needs.

## 7. Human experience requirements

Every meaningful human surface should expose:

- location and current phase;
- what matters now;
- why it matters;
- source evidence;
- what is fact, inference, assumption, and proposal;
- what the agent may do autonomously;
- what requires approval;
- feedback and repair;
- completion proof;
- one next meaningful route.

For long HTML:

- use a persistent journey map;
- highlight current location;
- provide a clear next route;
- use progressive disclosure;
- render source context before interpretation;
- keep controls keyboard accessible and touch targets usable;
- verify desktop and mobile in a real browser;
- retain the warm editorial/industrial visual language unless a project defines another direction.

## 8. Non-goals

Do not build or claim:

- one mega-prompt containing the whole system;
- a permanent swarm;
- a personality instruction that substitutes for evidence;
- an MCP server for every folder;
- a global autonomous knowledge graph as current truth;
- an embedding or vector database as the only copy of memory;
- one opaque reward number that hides hard-gate failures and metric tradeoffs;
- natural-language-only permission enforcement;
- automatic durable self-rewrites;
- weight-level self-improvement or AGI;
- universal benchmark superiority from a narrow or unmatched comparison;
- maximum architecture before one real workflow passes.
