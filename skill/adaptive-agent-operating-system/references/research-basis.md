# Research basis

This skill treats the current project's source requirements and accepted Foundry decisions as primary. External systems are comparative evidence, not authority.

## Contents

1. K3 frontier-intelligence transfer
2. Hermes operating-system transfer
3. Frontier product and eval practice
4. Agent and harness engineering
5. Skills, tools, and authorization
6. Human-centered AI
7. Memory and knowledge projections
8. Long-horizon runtime and interoperability
9. Farmtable task coordination and proof integrity
10. Evaluation and controlled experimentation
11. Current frontend and browser edge
12. Resulting rule

## K3 frontier-intelligence transfer

Source:

- public Kimi K3 technical report;
- [official Kimi K3 repository](https://github.com/MoonshotAI/Kimi-K3).

Durable findings:

- Capability came from a compound model, harness, environment, evaluation, and runtime system—not one prompt.
- A configurable white-box harness varies tools, system prompts, context strategies, skills, memories, subagents, and interaction protocols to reduce overfitting to one scaffold.
- A hierarchical knowledge graph retrieves real source material and synthesizes diverse tasks across domains and granularities.
- Autonomous Execution Tasks define initial state, constrained goal, action space, budget, and independent verifier without leaking a reference trajectory.
- Web-development training hard-fails broken, runtime-erroring, or fake artifacts before functional, structural, pixel, source, and interaction judgment.
- Evaluation reports effort, sampling, harness, context policy, repeats, tools, caveats, provenance, and date.
- Internal evals refresh from evolving capability and experience failures and feed the next improvement cycle.
- Stable prompt options, dynamic tool announcements, typed calls/results, and externalized state improve context/cache behavior.
- Partial rollout, snapshot, isolation, and scheduling patterns support long work.

Boundary:

- Model architecture, optimizer, data, and weight-level training cannot be reproduced by this skill.
- K3's report says it trails its two strongest evaluated proprietary systems overall while leading important subsets. Never convert a narrow benchmark into universal superiority.

## Hermes operating-system transfer

Source:

- [Nous Research Hermes `AGENTS.md`](https://github.com/NousResearch/hermes-agent/blob/main/AGENTS.md);
- local audit of the Hermes skill library.

Durable findings:

- Preserve stable per-conversation prompt context.
- Use a narrow core with expansive optional edges.
- Add capability through the smallest footprint that solves the problem: extend existing behavior, then CLI + skill, then gated service/tool, plugin, MCP, and core tool last.
- Verify the premise and original intent before “fixing.”
- Encode behavior contracts and repository-specific invariants rather than snapshotting prose.
- Validate real end-to-end paths, not only mocks.
- Isolate test HOME, credentials, time zone, and locale; flaky behavior is a defect.
- Keep optional/heavy capabilities inactive by default.
- Preserve durable job state, failure states, backup, and rollback.

Boundary:

- Hermes' long repository manual is valuable because it captures local invariants and failure memory. Do not copy it wholesale into every project or permanent prompt.

## Frontier product and eval practice

Source:

- [Dianne Penn interview, Lenny's Newsletter](https://www.lennysnewsletter.com/p/anthropics-first-technical-pm-on).

Durable findings:

- Frontier model and frontier product/harness enable each other.
- Strong labs are committed to the problem and weakly committed to a particular prototype.
- Product teams convert vague feedback into exact failure trajectories and executable evals.
- Begin with concrete representative examples and rerun them across model versions.
- Evals can serve as executable behavior specifications; PRDs still align product vision and teams.
- Builders must work hands-on with tokens, context, traces, and artifacts.
- A useful agent constitution permits proactive pushback rather than agreement theater.
- Verification and sign-off matter more than who drafted the artifact.

## Agent and harness engineering

Sources:

- OpenAI, [Harness engineering](https://openai.com/index/harness-engineering/);
- OpenAI, [Unrolling the Codex agent loop](https://openai.com/index/unrolling-the-codex-agent-loop/);
- OpenAI, [Introducing Codex](https://openai.com/index/introducing-codex/);
- OpenAI, [Evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices).

Durable findings:

- Keep `AGENTS.md` short and map-like.
- Treat repository knowledge and project state as the source of truth.
- Manage context as a scarce shared resource.
- Use task-specific datasets, graders, and continuous evaluation.
- Match verification to the claim.

## Skills, tools, and authorization

Sources:

- Anthropic, [Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills);
- [Model Context Protocol specification](https://modelcontextprotocol.io/specification/2025-03-26/index);
- [MCP authorization](https://modelcontextprotocol.io/specification/draft/basic/authorization).

Durable findings:

- Skills are progressively disclosed procedural onboarding.
- Tools, resources, prompts, retrieval, state, and skills are distinct surfaces.
- The model should not handle raw secrets.
- Hosts, runtimes, and servers must enforce access, consent, audit, and recovery; MCP is not the authority system by itself.

## Human-centered AI

Sources:

- [Microsoft Human-AI Interaction Guidelines](https://www.microsoft.com/en-us/haxtoolkit/ai-guidelines/);
- [Google People + AI Guidebook](https://pair.withgoogle.com/guidebook-v2/);
- [NIST AI RMF Playbook](https://www.nist.gov/itl/ai-risk-management-framework/nist-ai-rmf-playbook).

Durable findings:

- Set capability expectations.
- Make correction, feedback, control, and consequences legible.
- Preserve consent, accessibility, and graceful failure.
- Adapt cautiously and keep global controls.
- Tailor governance and verification to context and impact rather than applying one universal checklist.

## Memory and knowledge projections

Sources:

- Microsoft, [GraphRAG](https://github.com/microsoft/graphrag);
- SQLiteAI, [sqlite-memory](https://github.com/sqliteai/sqlite-memory);
- Google Cloud, [Open Knowledge Format specification](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md);
- Graphify Labs, [Graphify](https://github.com/Graphify-Labs/graphify);
- MiroFish, [multi-agent simulation engine](https://github.com/666ghj/MiroFish).

Durable findings:

- Human-readable, versioned Markdown can remain canonical while SQLite, FTS5, vectors, and graphs accelerate recall and traversal.
- Provenance, trust, freshness, lifecycle status, privacy, and supersession belong in queryable metadata.
- Extracted/explicit relationships must be distinguishable from inferred relationships.
- Graph and simulation layers are expensive hypotheses whose output must remain traceable and uncertain.
- Retrieval similarity proposes candidates; reading the canonical record establishes usable evidence.

## Long-horizon runtime and interoperability

Sources:

- OpenAI, [Symphony specification](https://github.com/openai/symphony/blob/main/SPEC.md);
- OpenAI Agents SDK, [Human in the loop](https://openai.github.io/openai-agents-python/human_in_the_loop/);
- A2A Project, [A2A protocol specification](https://github.com/a2aproject/A2A/blob/main/docs/specification.md).

Durable findings:

- An authoritative dispatcher, explicit task/attempt states, leases, heartbeats, reconciliation, retries, and stall detection make long work recoverable.
- Approval is a serializable interruption with exact scope, not a conversational suggestion.
- Remote agents need discoverable capabilities, async task IDs, artifacts, and durable states; local subagents do not need protocol ceremony.
- A2A is agent-to-agent; MCP is agent-to-tool/data.

Boundary:

- The user's ready-to-leased-to-active loop is supported as a mechanism, but the stated Qwen3.8-Max attribution was not verified from a primary source.

## Farmtable task coordination and proof integrity

Source:

- Scion Frontiers, [Farmtable](https://github.com/scion-frontiers/farmtable), audited at commit `154fc428ac6f40d582f15724606d043e1da5c733`.

Durable findings:

- A normalized task object can preserve a portable phase/workflow model while retaining adapter-native state and payload for lossless round-trip fidelity.
- Readiness should be derived from canonical stage/outcome, dependencies, holds, schedule, and other facts, then rechecked inside an atomic compare-and-swap claim.
- Work graph, task lifecycle, and worker-attempt lifecycle are different structures. Retry and approval loops do not belong in circular dependency edges.
- An embedded SQLite/in-process service and a Postgres/remote service can share one domain/client contract, creating a low-complexity deployment ladder.
- MCP works best as a thin typed translation layer while authorization, transitions, persistence, and audit remain in the underlying service.
- A best-effort live event stream may drop and resynchronize; it must not replace the durable event/replay source needed for long-horizon recovery.
- Decomposition must reconcile current artifact state, avoid fixed task quotas, validate packet/DAG quality, and materialize atomically or idempotently before dispatch.
- A green test command is incomplete evidence. Serious suites verify expected population, executed membership, command reachability, unexpected skips, evidence artifacts, and negative-control sensitivity.
- Terminal success requires artifact verification plus task-appropriate delivery/readback evidence; worker self-report is not a receipt.

Boundary:

- Farmtable is a task coordination system, not a model runtime, memory system, evaluator, checkpoint engine, or self-improvement loop. The Foundry borrows its task and proof contracts while adding leases, durable attempts/events, approvals, recovery, memory, and evaluation.

## Evaluation and controlled experimentation

Sources:

- Supabase, [evals](https://github.com/supabase/evals);
- Google, [Agent Platform Eval Flywheel](https://github.com/google/skills/blob/main/skills/cloud/agent-platform-eval-flywheel/SKILL.md);
- Andrej Karpathy, [autoresearch](https://github.com/karpathy/autoresearch);
- Addy Osmani, [agent-skills](https://github.com/addyosmani/agent-skills);
- Software Mansion, [skills](https://github.com/software-mansion-labs/skills).

Durable findings:

- Separate portable scenarios/final state from experiment configuration and compare baselines head-to-head.
- Use deterministic and rubric graders, inspect the actual exported artifact, cluster failures, and preserve machine plus human reports.
- Bound autonomous optimization with a narrow editable surface, fixed environment/evaluator, budget, and keep/discard experiment log.
- Lifecycle skills need proof-bearing exits, progressive disclosure, examples, linters/tests, and anti-skip behavior.
- Use one evaluation envelope with hard gates and a metric vector; do not hide heterogeneous quality in one scalar.

## Current frontend and browser edge

Freshness: 2026-08-03.

Sources:

- Next.js, [official release blog](https://nextjs.org/blog);
- Chrome, [WebMCP and MCP](https://developer.chrome.com/docs/ai/webmcp/compare-mcp);
- Chrome, [WebMCP tool security](https://developer.chrome.com/docs/ai/webmcp/secure-tools);
- W3C, [WebDriver BiDi](https://www.w3.org/TR/webdriver-bidi/);
- Vercel Labs, [agent-browser](https://github.com/vercel-labs/agent-browser).

Durable findings:

- Keep framework/protocol versions in adapters and verify official current docs before use.
- Next.js 16.2 currently exposes agent-oriented scaffolding, browser-log forwarding, experimental agent diagnostics, and a stable Adapter API.
- WebMCP is a proposed, ephemeral, page-native tool surface; it complements persistent backend MCP/API capabilities.
- Browser agents need origin/effect restrictions, untrusted-content handling, isolated sessions, console/network/state inspection, and explicit consequential-action gates.
- Screenshots support visual judgment but do not replace state readback and interaction testing.

## Resulting rule

Use the smallest competent operating loop. Give the agent wide room to think and discover; make outcome, authority, evidence, and completion increasingly explicit as stakes and autonomy rise. Improve the harness through observed traces and evaluated candidates—not through larger prompts, unearned architecture, or claims of self-modifying intelligence.
