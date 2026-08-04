# Durable memory and retrieval

## Contents

1. Memory is not one store
2. Canonical record contract
3. Write policy
4. Hybrid retrieval
5. Vector and graph activation gates
6. Retrieval use and context assembly
7. Memory evaluation
8. Privacy, correction, and deletion

## 1. Memory is not one store

Keep four categories separate:

| Category | Purpose | Canonical home |
|---|---|---|
| working context | current phase packet and immediate observations | active context with `STATE.md` pointers |
| project state | objective, decisions, evidence, risks, authority, next action | `PROJECT.md` and `STATE.md` |
| episodic run history | events, attempts, checks, approvals, failures, receipts | append-only event store or readable export |
| durable memory | confirmed preferences, decisions, facts, lessons, failures, procedures | human-readable records with metadata and source links |

Do not automatically turn raw chats, tool traces, speculative summaries, or retrieved web text into durable memory. They remain evidence until a write policy accepts a bounded record.

## 2. Canonical record contract

Use Markdown plus a small YAML-frontmatter subset:

```md
---
id: project-journey-map-preference
type: preference
scope: user
status: active
created_at: 2026-08-03T12:00:00-07:00
updated_at: 2026-08-03T12:00:00-07:00
source_refs: ["task:019f..."]
confidence: confirmed
privacy: internal
tags: ["html", "navigation"]
related: []
supersedes: []
stale_after: null
---

# Persistent journey navigation

## Memory

Long-lived interactive HTML should show current location and one actionable next route.

## Applicability

Use for substantial multi-page or long-scroll reading and work surfaces; not for a trivial one-page artifact.
```

Required semantics:

- `id` is stable and unique;
- `type` is `preference`, `decision`, `fact`, `lesson`, `failure`, `procedure`, or `checkpoint`;
- `scope` prevents cross-project leakage;
- `status` is `active`, `tentative`, `superseded`, `stale`, or `rejected`;
- `source_refs` resolve back to user input, files, URLs, events, or receipts;
- `confidence` distinguishes observed, confirmed, and inferred content;
- `privacy` is an access filter, not decoration;
- `supersedes` preserves correction history;
- `stale_after` makes freshness queryable.

Use `assets/schemas/memory-record.schema.json` as the normalized JSON contract. Use `scripts/validate_memory_bundle.py` for the Markdown bundle.

## 3. Write policy

Write durable memory only when the content is likely to matter beyond the current phase and is one of:

- an explicit user preference or correction;
- a consequential decision with rationale;
- a verified fact with source and freshness;
- a repeated failure or lesson with applicability;
- an evaluated reusable procedure;
- a checkpoint intentionally promoted beyond project state.

Before writing:

1. identify the exact source;
2. choose the narrowest scope;
3. label fact, inference, and confidence;
4. search for an existing or contradictory record;
5. update through supersession rather than erasing history;
6. set privacy and freshness;
7. obtain approval when the memory is sensitive, cross-project, or changes durable behavior.

Prefer one atomic, reusable claim per record. Do not store a polished omnibus summary that cannot be corrected independently.

## 4. Hybrid retrieval

Canonical Markdown remains the authority. A database is a rebuildable acceleration layer.

Recommended derived index:

```text
records metadata
chunks with record + heading pointers
FTS5 lexical index
optional embeddings with model/version/dimensions
explicit links
separately labeled inferred edges
source content hashes and index generation
```

Retrieval order:

1. apply user/workspace/project/component, privacy, and status filters;
2. get lexical candidates;
3. add vector candidates only when semantic recall is enabled;
4. traverse a small explicit-link neighborhood only when the query needs relationships;
5. merge ranks using a calibrated method such as reciprocal-rank fusion;
6. adjust for trust, freshness, and supersession;
7. diversify and surface contradictions;
8. return record IDs, snippets, source reasons, and scores;
9. read the canonical records before using them.

Similarity is candidate recall, not evidence that a statement is true or applicable.

## 5. Vector and graph activation gates

Start with file navigation plus exact/FTS search.

Add vectors only when a held-out query set shows that lexical retrieval misses relevant paraphrases or conceptual matches. Keep them only if the hybrid system improves recall without unacceptable false positives, scope leakage, latency, cost, or privacy risk.

Add graph projection only when tested workflows require:

- multi-hop provenance or decision lineage;
- contradiction and supersession traversal;
- repeated relationship-heavy recall;
- capability/evaluation coverage analysis;
- source-to-claim-to-eval impact tracing.

Every edge must say whether it is explicit/extracted or inferred, with provenance and freshness. A generated graph never replaces `PROJECT.md`, `STATE.md`, or the canonical memory record.

## 6. Retrieval use and context assembly

Retrieve in two stages:

1. **discover:** IDs, titles, snippets, scope, status, freshness, and why each item matched;
2. **read:** only the strongest canonical records needed for the current decision.

The context assembler must:

- preserve source IDs and status;
- include contradictions rather than silently choosing one;
- avoid stale or superseded content unless history is requested;
- prefer current project state over broad personal memory;
- impose a token budget and stop when marginal value is low;
- log which memories materially influenced a decision.

Do not inject a top-k vector dump into every turn.

## 7. Memory evaluation

Maintain representative and held-out queries for:

- recall@k and precision@k;
- correct scope isolation;
- stale and superseded suppression;
- contradiction surfacing;
- source/provenance readback;
- deletion and full rebuild;
- embedding-model migration;
- untrusted-content and prompt-injection handling;
- latency and context-token cost;
- whether retrieved memory improves the final decision, not merely retrieval similarity.

Compare files/FTS, vector, hybrid, and graph-assisted variants on the same query set. Do not adopt a heavier store from one anecdotal success.

## 8. Privacy, correction, and deletion

- Keep sensitive records out of third-party embedding APIs unless explicitly approved.
- Make access control apply before candidate retrieval.
- Store only what is needed, with an owner and deletion path.
- On user correction, create a new active record and mark the older one superseded.
- Rebuild all derived indexes after correction or deletion and verify the removed content cannot be retrieved.
- Treat backups, vector rows, caches, and graph projections as part of the deletion surface.
