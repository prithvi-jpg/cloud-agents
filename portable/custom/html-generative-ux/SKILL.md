---
name: html-generative-ux
description: Design, build, audit, and deliver clean product content, self-contained HTML, or schema-driven generative UI for inline Codex views, explainers, comparisons, decision aids, reports, prototypes, slide decks, and small editors. Use when a user asks for HTML artifacts, generative UI or UX, inline interactive visuals, dashboards, decks, one-file explainers, interface hierarchy, product copy, or when prose would become materially clearer as a purpose-built interface.
---

# HTML Generative UX

Create the smallest interface that makes the user's next thought or action easier. Choose the information form before choosing the visual style.

## Start with the communication contract

Write these six fields before coding:

1. **Outcome** — What should the user understand, decide, rehearse, or do?
2. **First useful view** — What must be legible without clicking?
3. **Evidence** — Which claims, sources, or artifacts support the view?
4. **Unknowns** — What is unresolved, assumed, stale, or blocked?
5. **Interaction** — What manipulation changes understanding or records intent?
6. **Host** — Markdown, Mermaid, Codex inline HTML, standalone HTML, application UI, or deck?

If interaction does not improve understanding or capture a real choice, omit it.

## Choose the delivery surface

Use the least complex surface that preserves the required meaning:

- **Prose or a short list** for one fact, one recommendation, or a simple sequence.
- **Table** for exact mappings or repeated-field comparisons.
- **Mermaid** for a static flow, hierarchy, dependency graph, or timeline.
- **Codex inline HTML** for a compact in-chat comparison, explainer, selector, rehearsal aid, or stateful decision surface.
- **Standalone HTML** for a portable, longer, or deeply interactive artifact that must work outside Codex.
- **React plus AI SDK or json-render** for a persistent product with streamed tool states, a controlled component catalog, data binding, and multi-turn interaction.
- **Deck** for an authored narrative presented one claim or scene at a time.
- **Video** when timing, narration, or demonstration is itself part of the explanation.

Do not introduce React, AI SDK, or json-render merely to create a one-off Codex visual. Codex inline delivery is a self-contained HTML fragment. Treat framework-based generative UI as the architecture for a persistent application, not as a prerequisite for an inline artifact.

## Choose the information form

Select one primary form. Combine forms only when the secondary form removes a real ambiguity.

### Brief

Use for today's focus, an operational heartbeat, or status.

Order: **decision or next action → why now → evidence/state → smallest follow-up**.

### Compare

Use when two to four alternatives share meaningful dimensions.

Keep the dimensions constant, make tradeoffs symmetric, and state the recommendation. Let users select or annotate a preference only when their response will be reused.

### Sequence

Use for chronology, dependencies, causal chains, or implementation stages.

Show current position, next transition, stopping conditions, and exceptions. Prefer a rail, timeline, or stepper over disconnected cards.

### Map

Use for architecture, ownership, source lineage, or one element affecting several downstream consumers.

Keep labels short. Let selection reveal one focused explanation instead of displaying every detail at once.

### Explain

Use for a difficult concept.

Start with one mental model, pair it with one manipulable visual, then show the transfer: “where this appears” or “what changes in practice.”

### Rehearse

Use for interviews, presentations, scripts, or decisions that must be spoken.

Present one prompt at a time, show a concise target shape, allow replay or self-check, and finish with the next physical action. Do not bury rehearsal inside a long packet.

### Editor

Use when the user needs to tune parameters, sort priorities, choose variants, or generate a downstream artifact.

Expose only consequential controls. Keep state local and visible. Produce a copyable summary, prompt, diff, or decision record at the end.

### Deck

Use when the material has a narrative arc.

Give each scene one job. Alternate evidence, mechanism, decision, and payoff. Keep navigation tiny and predictable. Prefer authored composition over a generic slide template.

## Structure before styling

Build the information hierarchy in this order:

1. One dominant claim, question, or action.
2. The minimum context required to trust it.
3. One main visual or interaction.
4. Evidence, tradeoffs, or unknowns near the claim they qualify.
5. One explicit next action.

For personal-assistant work, preserve:

**source → interpretation → decision → action**

Do not default to a dashboard. A dashboard is appropriate only when several stable metrics or states must be monitored repeatedly. A one-time decision usually needs a comparison, interview, sequence, or explainer.

### Apply clean-content discipline

Treat shipped interfaces as evidence, not automatic precedent. Before composing the surface:

1. Route the task as **shape**, **implement**, **review**, **copy**, or **harden**.
2. Name the user's job, desired outcome, and non-goals before drawing pixels.
3. Separate verified facts, product decisions, assumptions, and open questions.
4. Make the smallest coherent intervention that solves the current job.
5. Decide architecture, semantics, action hierarchy, and reachable states before adding decoration.
6. State the exact object, scope, and consequence of consequential actions.
7. Preserve context and input through loading, empty, recoverable-error, and success states.
8. Verify the real rendered surface rather than judging source code alone.

Use strong defaults and direct behavior before adding settings. Prefer inline disclosure before a modal. Keep navigation and actions semantically distinct. An advanced control must not burden the default path.

## Build with restrained, self-contained primitives

- Use semantic HTML and native controls first.
- Define a small token set with CSS custom properties.
- Use typography, spacing, alignment, and contrast for hierarchy before decoration.
- Use one interface sans family. Reserve mono for code, identifiers, timestamps, measurements, or other precision metadata, not paragraphs.
- Keep heading weights restrained and tracking deliberate. Muted text may recede, but it must remain comfortably legible.
- Use a second background tone sparingly to distinguish a meaningful region, not to stripe every section.
- Use visible grid guides only when the grid itself communicates structure. Do not nest decorative grids.
- Use one dominant visual grammar; avoid a wall of interchangeable cards.
- Use inline SVG for small diagrams and illustrations.
- Keep JavaScript as a tiny state machine around the interaction.
- Use progressive disclosure with `details`, tabs, selection, or focused panels.
- Add clear selected, loading, success, empty, and error states when those states exist.
- Make copy actions produce visible feedback.
- Preserve keyboard access, visible focus, labels, ARIA where needed, and sufficient contrast.
- Respect `prefers-reduced-motion`.
- Avoid external dependencies unless the host and task require them.
- Keep sources, assumptions, and unknowns visible; never style uncertainty as certainty.

Read [clean-content-and-design-judgment.md](references/clean-content-and-design-judgment.md) when the task involves product copy, hierarchy, surface selection, clean content, or design-system judgment. Read [generative-ux-model.md](references/generative-ux-model.md) when choosing a schema or interaction model. Read [source-study.md](references/source-study.md) when selecting a concrete pattern from the studied repositories.

## Deliver inside Codex

Before building an inline visualization, read the current `visualize:visualize` skill exposed in the available-skills catalog. Use its composition, accessibility, and verification guidance. Treat its final reference syntax as host-dependent: the active Codex Desktop delivery contract below controls when thread-scoped visualization roots and `::codex-inline-vis` are present.

### Select the resolver before writing

Do not assume that an HTML file path and an inline-render request use the same resolver.

- When Codex Desktop app context exposes a thread-scoped visualization directory or documents `::codex-inline-vis`, use the Codex Desktop protocol: mirror the fragment to both thread roots, verify it, and emit exactly `::codex-inline-vis{file="basename.html"}`.
- Never pass an absolute `/mnt/c/...` or `/home/...` path to a generic `visualize` content reference in this Codex Desktop mode. It can fail with `Invalid visualization read request` even when the fragment is valid.
- Use an absolute-path visualization content reference only when the active host explicitly requires that protocol and no basename directive is available.
- Never emit both protocols as speculative fallbacks. Resolve the host first.

Treat delivery as four separate layers and debug them in order:

1. **Fragment** — literal HTML fragment, scoped CSS, valid runtime behavior.
2. **Mirror** — byte-identical Windows-backed and WSL thread files.
3. **Resolver** — the host-specific basename directive or absolute-path reference.
4. **Renderer** — actual in-chat load, interaction, layout, and console behavior.

If the error is `Invalid visualization read request`, fix the resolver syntax first; do not rewrite a fragment that already passed rendering and interaction checks. If the error is `ENOENT`, verify the thread ID, date, basename, and WSL mirror.

For a Codex fragment:

- Return a fragment, not a full `html`, `head`, or `body` document.
- Scope all CSS beneath one unique root.
- Do not repeat a title or prose already supplied by the chat.
- Design for roughly 736 CSS pixels and responsive narrowing.
- Use Codex theme variables and host dark/light classes.
- Keep data and assets self-contained; do not depend on WSL-only or Windows-only paths at runtime.
- Use `window.openai.sendFollowUpMessage({ prompt })` for a button that should continue the conversation.
- Use ordinary DOM state for local interactions.
- Keep the fragment below the renderer's size limit.
- Save it to the exact thread visualization directory and emit `::codex-inline-vis{file="name.html"}` with the basename only.
- In mixed Windows/WSL environments, mirror the byte-identical file to both thread-scoped visualization roots when the host resolver has used both paths.
- Do not make a local file link the primary experience when the user asked for inline delivery.

Use [codex-inline-delivery.md](references/codex-inline-delivery.md) for resolver selection, failure triage, and the mixed-runtime receipt. In a mixed Windows/WSL Codex Desktop environment, set `CODEX_WINDOWS_VIS_ROOT` to that laptop's Windows visualization directory, then run `scripts/verify-codex-inline.sh <YYYY/MM/DD> <thread-id> <basename.html>` after mirroring; emit only the directive printed by a successful preflight. Start from [codex-inline-fragment.html](assets/codex-inline-fragment.html) when useful.

## Build a standalone artifact

For a one-file artifact:

- Include the full document shell, descriptive `<title>`, viewport metadata, and semantic landmarks.
- Make it work by opening the file directly when feasible.
- Embed small required assets; avoid embedding huge media unless portability is the explicit goal.
- Keep deep links, print behavior, and narrow viewports usable.
- Provide visible source notes when facts came from external research.

Start from [standalone-artifact.html](assets/standalone-artifact.html) when useful.

## Build a schema-driven application

Use AI SDK or json-render only when the interface must persist, stream, bind to application state, or support a reusable component vocabulary.

1. Define a small component catalog and action catalog.
2. Constrain model output to a typed schema; do not let it emit arbitrary executable code.
3. Render model tool results or JSON specs through trusted components.
4. Model submitted, streaming, approval, success, empty, and error states.
5. Keep data retrieval and side effects in tools/actions, not generated layout.
6. Stream progressively only when partial structure is useful.
7. Log the spec and actions so the interaction can be reproduced.

The model should choose **composition and emphasis** inside the catalog. The application should retain control over **behavior, permissions, data, and safety**.

## Build a deck

For an HTML deck:

- Use a fixed authored stage, commonly 16:9, and scale it to the viewport.
- Keep one active slide in the accessibility and playback path.
- Support arrow keys, space, page keys, home/end, and clear click navigation.
- Pause media on inactive slides.
- Exempt live controls from navigation clicks.
- Show a quiet progress indicator.
- Use large type and scene-specific composition; do not reduce every slide to a heading plus bullets.
- Verify the entire narrative at representative frames.

## Verify before delivery

Run the included corpus audit when studying source HTML:

```bash
node scripts/audit-html.mjs <root> [<root> ...] --output report.json
```

Then verify the actual target surface:

- First render communicates the outcome without interaction.
- Text is not clipped at target and narrow widths.
- Every control works with pointer and keyboard where applicable.
- Selected, success, empty, and error states remain understandable.
- The browser console has no errors.
- External facts have nearby citations.
- The main action is obvious and singular.
- The artifact contains no broken local paths.
- Inline Codex delivery resolves from the actual host path.
- The final response uses the host's one verified resolver protocol, not a generic absolute-path fallback.

Use screenshots or browser automation for visual QA. Treat source validity and renderer validity as separate checks.

## Avoid these failure modes

- Card soup masquerading as information architecture.
- A dashboard for a one-time decision.
- Decorative motion without semantic feedback.
- Controls that do not change understanding or produce an artifact.
- Raw model JSON shown to the user.
- Arbitrary model-generated code in a persistent product.
- Hidden assumptions, stale facts, or unlabeled synthetic data.
- A beautiful first frame with no next action.
- A local file link when the requested experience is inline.
- An absolute-path visualization request in a Codex Desktop task that requires a basename-only `::codex-inline-vis` directive.
- Rewriting valid HTML to fix a resolver-schema or missing-mirror failure.
- Declaring success after file creation without loading and exercising the renderer.
