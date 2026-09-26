# Source study: HTML as an effective communication medium

## Scope and evidence

The study read and audited every HTML file present at these repository revisions:

- `ThariqS/html-effectiveness` at `1787245d94aa680edf18b52027e3f859032776ba`
- `ThariqS/cc-video-editing-deck` at `b29cffe55f4f695a39c118f4021e1b7f21bf265e`

Inventory: **34 HTML files, 5,139,823 bytes, approximately 20,348 lines**. The structured per-file receipt is [repo-audit.json](repo-audit.json). `html-effectiveness` contained 33 HTML files; `cc-video-editing-deck` contained one 4.37 MB self-contained deck.

`html-effectiveness` is Apache-2.0 licensed. No license file was present in the studied `cc-video-editing-deck` checkout, so derive patterns from it but do not copy its embedded media, fonts, or authored content.

## Per-file findings

### `html-effectiveness`

| File | Form and construction | Reusable lesson | Watch-out |
|---|---|---|---|
| `index.html` | Editorial gallery organized by purpose, with nine sections and tiny bespoke SVG thumbnails. | A pattern library is easier to navigate by user intent than by implementation technology. | Gallery chrome is not the artifact grammar; do not reuse it everywhere. |
| `01-exploration-code-approaches.html` | Three symmetric implementation columns, code excerpts, tradeoff rows, and a recommendation aside. No JS. | Compare alternatives against the same dimensions and end with a decision. | Equal visual weight can imply false equivalence; recommendation must break the tie. |
| `02-exploration-visual-designs.html` | Four artboards showing the same empty state; one global light/dark control; limited illustrative motion. | Hold content constant while varying the design direction so taste differences are legible. | Motion and theme toggles are useful only when they expose a real direction. |
| `03-code-review-pr.html` | PR metadata, risk map, anchored file cards, inline review notes, collapsible files, and a next-step checklist. | Put risk before diff volume and link overview judgments to exact evidence. | Interactive checkboxes are ephemeral unless their state is persisted elsewhere. |
| `04-code-understanding.html` | One overview flow plus an accordion-like call-stack walkthrough and a gotchas aside. | Pair a global mental model with local source evidence; keep only one deep detail open. | A diagram without exact file/function anchors becomes decorative. |
| `05-design-system.html` | Static token reference with live native component specimens. | Show tokens through rendered behavior, not only token names. | A design-system page is documentation, not a substitute for component states and accessibility tests. |
| `06-component-variants.html` | Variant matrix controlled by CSS variables for padding, border, and shadow. | Parameterize shared dimensions so differences can be felt instead of described. | Too many independent controls obscure the design decision. |
| `07-prototype-animation.html` | One completion interaction, selectable easing curves, keyframe timeline, and copyable CSS. | Let users replay and tune a single motion; connect the feeling to implementation. | Confetti and bounce can overwhelm the semantic state change. |
| `08-prototype-interaction.html` | Drag-to-reorder prototype paired with “what you are feeling” and open questions. | Prototype the gesture and document unresolved interaction decisions beside it. | HTML drag events alone are weak on touch and need keyboard alternatives in production. |
| `09-slide-deck.html` | Six full-height slide sections with keyboard navigation, intersection-aware counter, and varied layouts. | One claim per scene plus quiet progress creates an authored narrative without a framework. | Scroll and keyboard navigation can conflict if active-slide state is ambiguous. |
| `10-svg-illustrations.html` | Three standalone SVG illustrations with direct download actions and a palette/rules appendix. | Deliver the asset, its variants, and the rules that keep future assets coherent. | Export code must preserve namespaces and revoke temporary URLs. |
| `11-status-report.html` | Summary stats, highlights, shipped table, velocity chart, and carryover. | Organize status as outcomes, evidence, and remaining risk rather than a task dump. | Metrics need provenance and denominators to avoid false precision. |
| `12-incident-report.html` | Sticky table of contents, severity/status metadata, timeline, root-cause diff, impact, and action table. | Incident communication needs chronology, causality, impact, and ownership in that order. | A polished report must not soften uncertainty or missing follow-up owners. |
| `13-flowchart-diagram.html` | Clickable SVG nodes update a single details panel from a data object. | Keep the graph overview stable and reveal one selected node's explanation. | Dense SVG coordinates become hard to maintain; use a graph system for larger maps. |
| `14-research-feature-explainer.html` | Sticky navigation, step accordion, code tabs, gotchas, and FAQ. | Explain a feature through request path, configuration, failure modes, then questions. | Too many code blocks can bury the one mental model the reader needs. |
| `15-research-concept-explainer.html` | Interactive hashing ring with sliders, comparison table, glossary linkage, and use cases. | A manipulable model makes an abstract invariant memorable. | Simulation output must preserve the concept's real constraints and edge cases. |
| `16-implementation-plan.html` | Milestones, data-flow SVG, product mockups, key code, risks, and open questions in one plan. | A technical plan should make architecture, UX, risk, and unanswered product decisions visible together. | Length is justified only when sections are anchored to execution decisions. |
| `17-pr-writeup.html` | Why, before/after, collapsible file tour, review focus, test plan, rollout, and local TOC. | Write PRs for the reviewer's attention: purpose, high-risk files, proof, then rollout. | File-by-file narration should not duplicate the diff. |
| `18-editor-triage-board.html` | Data-driven draggable ticket board with filters, counts, reset, and Markdown export. | A small editor becomes valuable when interaction produces a reusable downstream artifact. | Drag-only ordering needs accessibility and persistence for real use. |
| `19-editor-feature-flags.html` | Schema-like flag data renders a form, live warnings, diff, full JSON, copy, and reset. | Separate canonical state, derived warnings, and export formats; show consequences immediately. | Feature-flag UIs need authorization and server validation beyond local controls. |
| `20-editor-prompt-tuner.html` | Content-editable prompt with slot highlighting, sample data, preview, keyboard/paste handling, copy, and reset. | Treat prompts as structured artifacts with visible variables and rendered outputs. | Content-editable caret preservation and sanitization are genuinely complex. |

### `html-effectiveness/unknowns`

| File | Form and construction | Reusable lesson | Watch-out |
|---|---|---|---|
| `index.html` | Examples grouped into pre-, during-, and post-implementation, with a known/unknown quadrant motif. | Organize uncertainty work by when it changes action. | “Unknown unknown” language needs concrete discovery methods, not mystique. |
| `01-blindspot-pass.html` | Seven hidden traps, each with evidence and a copyable prompt fragment, folded into a final prompt. | Convert discoveries into reusable constraints so the next run starts smarter. | Do not mistake plausible traps for verified repository facts. |
| `02-color-grading-explainer.html` | Teaching ladder plus live before/after split, presets, and grading sliders. | Progress from vocabulary to manipulation to better instructions. | Visual filters approximate grading; label simulations honestly. |
| `03-design-directions.html` | Four fully rendered directions using the same data; “steal/skip” chips generate a reply. | Let users compose taste from parts instead of forcing a single style vote. | Direction prototypes need realistic density to reveal scaling failures. |
| `04-toolbar-mock.html` | Working toolbar placement variants, live controls, comments drawer, and four explicit layout decisions. | Mock the uncertain product decisions and collect answers in the artifact itself. | High-fidelity chrome can imply implementation completeness. |
| `05-churn-brainstorm.html` | Ten interventions ordered on an effort spectrum; checkboxes create a concise reply. | Order ideas by a meaningful axis and turn resonance into a selection artifact. | “Cheapest to ambitious” is not prioritization without impact and evidence. |
| `06-interview.html` | Seven questions ordered by blast radius, one at a time, with rationale, options, progress rail, editable summary, and generated prompt. | Ask only questions whose answers change the implementation; convert answers into constraints. | Multiple-choice options can anchor the user; always allow custom wording. |
| `07-reference-port.html` | Side-by-side semantic mapping from source implementation to target, with keep/change/drop and confirmation actions. | Port behavior and invariants, not syntax; surface traps explicitly. | Similar code shape does not prove semantic equivalence. |
| `08-implementation-plan.html` | Plan sorted by likelihood of user revision, with inline alternative toggles, execution sequence, and mechanical details collapsed. | Put consequential decisions first and bury trusted mechanical work. | A plan sorted for review still needs an executable dependency order. |
| `09-implementation-notes.html` | Timestamped implementation ledger with plan-confirmed, discovery, deviation, and human-decision filters; lessons fold into the next attempt. | Preserve mid-build surprises as reusable evidence instead of losing them in chat. | “Conservative choice” still needs an explicit blast-radius and rollback check. |
| `10-pitch-doc.html` | Animated product demo, pitch, anticipated objections, spec, risk, rollback, and requested decision. | A buy-in artifact should show the experience, answer objections, and name the decision needed. | Auto-play theater cannot replace working-product evidence. |
| `11-change-quiz.html` | Mental model, non-obvious behaviors, six-question quiz, pass/fail routing, and targeted reread links. | Retrieval practice reveals whether someone can safely act on a change. | A quiz should test operational consequences, not trivia. |

### `cc-video-editing-deck/index.html`

The deck is a single 4.37 MB, self-contained presentation titled **“How Fable Edited Its Own Video.”**

Construction:

- A fixed `1920 × 1080` stage is scaled to fit the viewport.
- Fifteen slide containers are absolutely layered; the active slide changes by opacity.
- JavaScript is only a small navigation state machine: resize, keyboard, and left/right click.
- Arrow keys, space, page keys, home/end, click regions, and a `1 / 15` HUD handle navigation.
- Videos play only on the active slide; inactive videos pause.
- A `.noadvance` region protects a live embedded control surface from deck navigation.
- Fonts, images, videos, and an iframe are embedded as data URIs, yielding a truly portable but large file.
- The deck uses strong scene composition, large typography, and alternating dark, ivory, and clay backgrounds.
- The story progresses from raw material and a single prompt through transcription, subagents, JSON EDL, ffmpeg, grading, code-built graphics, transcript timing, Figma round-tripping, live controls, final render, repository structure, and results.

Reusable lessons:

1. HTML can be the runtime for a high-production deck; complexity can live in authored composition rather than a presentation framework.
2. A small navigation state machine is enough when each scene is deliberately composed.
3. Show the mechanism, intermediate artifacts, and final payoff—not only claims.
4. Embed a real control surface when the audience benefits from touching the system.
5. Separate navigation clicks from live interaction zones.
6. Pause hidden media and verify every representative scene.

Watch-outs:

- A fully embedded media deck can become very large.
- Absolute slide composition is expensive to author and difficult to make semantically responsive.
- Embedded assets may have separate rights; do not copy them without permission.
- The narrative strength comes from content sequencing and evidence, not from the color palette alone.

## Cross-repository synthesis

### What makes the HTML effective

1. **The page is shaped around the cognitive job.** Comparison, rehearsal, inspection, tuning, and storytelling receive different structures.
2. **Uncertainty becomes visible and manipulable.** The interface asks, compares, filters, toggles, or simulates exactly where prose would hide a decision.
3. **Interaction produces a residue.** Good controls end in a decision summary, prompt, diff, Markdown export, downloaded SVG, or next action.
4. **Overview and detail coexist.** Stable rails, diagrams, or summaries orient the user while one focused panel carries depth.
5. **The authored artifact stays technically small.** Most examples use native HTML, CSS variables, inline SVG, and a small local state machine.
6. **Narrative is a state machine too.** The deck uses the same principle as the editors: a compact model controls which authored view is active.
7. **Consistent tokens help; repeated templates do not.** The shared ivory/slate/clay system creates family resemblance, while information architecture changes per job.

### What not to copy

- Do not turn every answer into cards.
- Do not treat a palette as the design system.
- Do not add controls whose output goes nowhere.
- Do not make an artifact interactive only to seem advanced.
- Do not copy unlicensed embedded media or fonts.
- Do not use a 1920×1080 absolute canvas for ordinary responsive documents.
- Do not confuse a local prototype's behavior with production permissions, persistence, accessibility, or data integrity.
