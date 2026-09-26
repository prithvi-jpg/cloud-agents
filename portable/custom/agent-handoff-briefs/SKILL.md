---
name: agent-handoff-briefs
description: Use when turning a ramble into a one-shot Codex prompt.
---

# Agent Handoff Briefs — one-shot starting prompts from user rambles

The user's standing workflow: he rambles raw ideas → you structure + research + shape → the FINAL deliverable is a single starting prompt that an autonomous coding agent (Codex, prime-agent) receives cold and executes from scratch (own research → prototype → deck → report). This skill encodes his corrections and the workflow that produced `~/dev/codex-brief/STARTING-PROMPT.md` (v1, canonical worked example) and the executed mission in `~/dev/hyperswitch-us-market/`.

## Non-negotiables (user corrections — treat as hard rules)

1. **NOTHING gets omitted.** Every link and detail he gave must appear IN THE FINAL PROMPT, each link with its job. He explicitly rejected a compressed draft: *"i have told u so many details and explicitly warned u not to miss links and details of what i said."* Keep a master link list in the prompt, grouped by purpose.
2. **The prompt IS the deliverable.** Write the actual handoff — direct, imperative: *"research this; think about how motion design plays with these stencils and links; do this; do that."* Do NOT present the working-notes doc (BRIEF.md / STATE.md / decision logs) as the handoff — *"wtf is that brief.md?"* Notes and evidence stay behind the scenes; they feed the prompt, they are not it.
3. **Spark, don't constrain.** Give mission + soul + research mandates + hard bars; let the agent verify and decide for itself (*"it shouldn't be like Codex should only follow these"*). Research mandates, not step-by-step instructions.
4. **Evals-first** whenever the mission includes building a product: outcome/intent-based eval suite (INTENT / OUTCOME / VERIFICATION per flow) written BEFORE the build. *"Evals are the future of product management... the codex should write evals first."* The evals are the spec.
5. **Collaboration & explainability contract** goes IN the prompt: the agent must explain its decisions in plain terms ("this is good decision-making, this is bad decision-making"), ask the user one pointed question when only they can decide, and never end on a promise of unverified work.
6. **Honesty bar**: every claim on screen labeled LIVE (provable) or SIMULATED (seeded); every number sourced with link + year; asserted ≠ observed.

## Workflow

1. **Capture the ramble verbatim** — thread decomposition + master link list, preserved in full (a notes doc, not the deliverable).
2. **Research storm** — batch 3 parallel sub-agents per round (delegate_task). Each MUST write incrementally to a known file path (survives the ~600s hard timeout; on timeout-with-no-summary, salvage the file, don't re-dispatch). On HTTP 503 upstream flakiness: retry once with backoff, then fall back to direct curl/web_extract yourself. Verify top links return HTTP 200 before citing them. Park dossiers in the project's `research/`.
3. **Thesis + decision log** — data-backed picks; name alternatives dismissed in a line each; state what would change the decision.
4. **Eval suite** — before any build (see non-negotiable 4).
5. **Write the handoff prompt** — structure in `templates/starting-prompt-skeleton.md`.
6. **Execute** — `prime-agent -p --autonomous --cwd <project> "$(cat STARTING-PROMPT.md)"` (needs provider+key: `--provider`/`--api-key` or env var like OPENROUTER_API_KEY; if unauthenticated, check env/config first — asking late wastes a turn). Fallback: execute the draft yourself in Hermes with the same prompt as your operating brief.

## Prompt structure that worked (v1)

You-are framing (mission, stakes) → verbatim take-home brief → RESEARCH FIRST (all links grouped by purpose: platform/architecture, sandbox+playground capabilities, market+competitors incl. deep-dive target, community signals) → vertical/flows direction with data + provability tiebreaker (let agent verify) → EVALS FIRST → MOTION & DESIGN (reference links: cobe globe, fudge-design-md standards, pen.dev; motion is a feature: timeline draw, node pop, live pulse, tabular-nums, prefers-reduced-motion) → flows-showcase spec (marketing-grade, live run buttons, step-by-step, what-to-notice) → HONESTY BAR → SETUP FIRST (fresh folder, AGENTS.md, STATE.md, PLAN.md → v01) → DELIVERABLES with done-bars → HOW TO WORK (autonomy boundaries, AUTH rule for outward actions, one pointed question, decision explainability, outcome-first reports).

## Style doctrine (distilled from Fable / GPT-5.6 research — source material in ~/dev/codex-brief/research/)

Goal not steps · bars not adjectives · every line must change behavior or get cut · state each instruction once · evidence before reasoning · verify by observation · never let the builder grade its own work · report outcome-first with honest caveats · lean — but for THIS user, completeness of his links/details beats leanness (see non-negotiable 1).

## Prompt sizing — calibrate length to deliverable type

Not every handoff gets the full v1 structure. Ask: is Codex executing a MULTI-ARTIFACT MISSION (research → prototype → deck → report) or producing ONE artifact (a guide, a doc, a single site)?

- **Multi-artifact mission** → full v1 structure (research mandates, evals-first, setup-first, how-to-work).
- **Single-artifact deliverable** → ONE-PAGE prompt max, ONE named output file, NO research-mandate list ("no additional lookups"), no multi-file plan. User correction (2026-08-22, Juspay systems guide): *"leave multiple files in the prompt that is overkill; the prompt should be short one page max no additional lookups"* — he trimmed my ~9KB prompt to ~3KB and kept only mission + outline + bars + style. Cut scope aggressively when he signals bloat; don't defend structure.

## Delivery format of the prompt itself

He copies prompts out of CHAT, not out of files. After writing STARTING-PROMPT.md, ALWAYS also paste the full prompt verbatim in a single fenced markdown block in the reply. Writing the file + opening a preview pane alone forced him to ask *"what is the prompt that I have to give to Codex? You have given multiple different files and stuff."* One copyable block, no meta-commentary inside it.

## Pitfalls

- **Dropping links/details** — his #1 complaint; recheck the ramble against the final prompt line by line.
- Presenting the notes doc (BRIEF.md §1–§9) as the handoff.
- Delegation 503s (upstream capacity): re-dispatch once, else go direct — never idle waiting.
- Protected reads are approval-gated and time out silently in this desktop env → treat as no-consent, never work around; get creds from project docs or ask the user to export a key.
- prime-agent without auth fails immediately — verify env keys exist before promising a launch.

## References / worked examples

- `~/dev/codex-brief/STARTING-PROMPT.md` — v1 handoff (canonical), `BRIEF.md` §8 = ramble threads + master link list
- `~/dev/hyperswitch-us-market/` — executed mission: research/ dossiers → THESIS.md → evals/SUITE.md → SESSION_LOG.md (live-probe proof)
