# Generative UX model

## Core distinction

Generative UI is not arbitrary UI generation. It is the controlled selection and composition of trusted interface primitives around a user's current cognitive job.

For a one-off artifact, generate a self-contained HTML view directly. For a persistent product, constrain generation to a catalog and render a typed specification through trusted components.

## The communication object

Model every generated surface with this contract:

```json
{
  "goal": "understand | decide | act | rehearse | monitor | edit",
  "mode": "brief | compare | sequence | map | explain | rehearse | editor | deck",
  "headline": "the dominant claim, question, or action",
  "context": "minimum information needed to trust the view",
  "evidence": [
    {
      "claim": "what is supported",
      "source": "citation or local artifact",
      "freshness": "current | dated | user-supplied",
      "confidence": "verified | inferred | unresolved"
    }
  ],
  "unknowns": [
    {
      "question": "what is unresolved",
      "impact": "what changes if the answer changes",
      "policy": "assume | ask | stop | research"
    }
  ],
  "blocks": [],
  "actions": [
    {
      "label": "verb-led action",
      "kind": "local-state | copy | follow-up | external",
      "requiresApproval": false
    }
  ]
}
```

The schema is a thinking aid, not a requirement to expose JSON to the user.

## Block grammar

Use a small, controlled vocabulary:

- `focus`: one primary action or decision.
- `fact`: a source-backed statement.
- `unknown`: unresolved state and its consequence.
- `option`: one alternative with common comparison fields.
- `step`: order, dependency, owner, and stopping condition.
- `node`: entity plus relationships.
- `metric`: value, timeframe, source, and interpretation.
- `prompt`: something to say, answer, or rehearse.
- `control`: a consequential parameter or choice.
- `output`: generated prompt, diff, decision, script, or export.
- `source`: nearby citation and freshness.

Do not create a component type for every visual whim. The catalog should encode stable communication semantics.

## Mode contracts

### Brief

Required blocks: `focus`, zero to three `fact` or `unknown` blocks, one `action`.

First render: the next action and why it matters.

### Compare

Required blocks: two to four `option` blocks with shared dimensions, one recommendation, one choice action when needed.

First render: the important difference, not four decorative cards.

### Sequence

Required blocks: ordered `step` blocks with current state, next transition, and stopping or failure condition.

First render: where the user is and what happens next.

### Map

Required blocks: labeled `node` and relationship data; one selected-detail panel.

First render: topology and dominant dependency.

### Explain

Required blocks: one mental model, one example or manipulable `control`, one transfer-to-practice block.

First render: the concept in one sentence and one picture.

### Rehearse

Required blocks: one `prompt` at a time, concise target shape, progress, replay/edit, and final action.

First render: the first spoken prompt.

### Editor

Required blocks: current state, consequential `control` blocks, live consequence, and an `output`.

First render: the artifact being edited and the few controls that matter.

### Deck

Required blocks: ordered scenes; each scene has one claim and one evidence or mechanism object.

First render: the premise and promised payoff.

## State model

Persistent generative interfaces should distinguish:

- `idle`
- `submitted`
- `streaming-structure`
- `streaming-content`
- `tool-input-ready`
- `tool-running`
- `approval-needed`
- `output-ready`
- `empty`
- `error`
- `stale`

Render state explicitly. Never present partial, inferred, or stale data as a finished result.

## Action model

Classify actions before wiring them:

1. **Local state** — selection, filtering, toggling, rehearsal progress. Safe and immediate.
2. **Copy/export** — creates a user-controlled artifact. Show feedback.
3. **Conversation follow-up** — send a bounded prompt back to Codex.
4. **External mutation** — messages, scheduling, purchases, publication, deletion. Keep outside generated layout unless permissions and approval are explicit.

The model may propose an external action. Trusted application code must enforce approval and execute it.

## Renderer architecture

### One-off Codex artifact

```text
task context
  -> choose mode
  -> author HTML fragment
  -> local DOM state
  -> optional sendFollowUpMessage
  -> renderer verification
```

This path is fastest and needs no React runtime.

### Persistent application

```text
conversation + tool results
  -> constrained UI spec
  -> schema validation
  -> trusted component registry
  -> state/data binding
  -> approved action registry
  -> streamed renderer
```

Vercel AI SDK UI maps typed tool-result parts to application components. json-render goes further by letting the model compose a UI specification from a controlled catalog, including standalone or inline generation modes, progressive JSONL patches, bindings, and visibility rules. Use either model to inspire system architecture, but keep Codex inline artifacts framework-free unless building a persistent app.

## Selection heuristic

Ask these questions in order:

1. Would two concise paragraphs solve it? Use prose.
2. Are exact repeated fields the main value? Use a table.
3. Are relationships the main value? Use Mermaid or a map.
4. Does manipulation change understanding or capture a decision? Use inline HTML.
5. Must it be shared, printed, or revisited outside chat? Use standalone HTML.
6. Must the interface persist and stream across turns or tools? Use a schema-driven application.
7. Is timed narration the core experience? Use a deck or video.

## Quality test

An effective generated interface should pass five tests:

- **Compression:** Is it faster to understand than the equivalent prose?
- **Agency:** Does the user know what they can do?
- **Residue:** Does interaction produce a useful decision, artifact, or next step?
- **Truth:** Are sources, unknowns, and synthetic examples distinguishable?
- **Fit:** Is this form better for the task than a table, diagram, or paragraph?
