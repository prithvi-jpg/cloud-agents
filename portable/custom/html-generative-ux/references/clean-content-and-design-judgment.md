# Clean content and design judgment

Use this reference to turn “clean” from a visual adjective into a repeatable product-design method.

## Source record

Accessed 2026-07-28:

- [Geist introduction](https://vercel.com/geist/introduction)
- [Geist typography](https://vercel.com/geist/typography)
- [Geist grid](https://vercel.com/geist/grid)
- [Geist colors](https://vercel.com/geist/colors)
- [Teaching agents product design at Vercel](https://vercel.com/blog/teaching-agents-product-design-at-vercel)

These sources are evidence for the rules below. They do not make every shipped Vercel pattern appropriate for every product.

## Clean-content operating contract

Before implementation:

1. **Start with the job.** State what the user is trying to accomplish, not the page or component requested.
2. **Define the outcome.** Write the intended behavior or understanding and the non-goals.
3. **Separate knowledge types.** Mark facts, decisions, assumptions, and open questions distinctly.
4. **Use evidence.** Prefer research, source artifacts, observed behavior, and verified rendered surfaces over taste language.
5. **Choose the smallest coherent intervention.** Solve the current job without redesigning unrelated systems.
6. **Decide before decorating.** Resolve architecture, semantics, action hierarchy, states, and content before polish.
7. **Cover reachable states.** Design only states the user can actually reach, including loading, empty, recoverable error, and success.
8. **Verify the output.** Inspect the rendered surface at representative widths and states.

Treat production code as evidence of prior choices, not as a rulebook. A precedent may encode legacy constraints or one-off compromises.

## Content hierarchy

- Make the primary task and primary action unmistakable.
- Preserve the user's mental model and nearby context across transitions.
- Name the exact object, scope, and consequence of consequential actions.
- Use verb-plus-noun action labels when ambiguity is possible.
- Keep navigation, state, and actions semantically distinct.
- Put supporting explanation near the decision it qualifies.
- Prefer inline disclosure before a modal.
- Use strong defaults and direct behavior before adding preferences.
- Hide advanced controls until they are relevant to the current path.
- Preserve user input through recoverable errors.
- Remove decorative novelty, motion, and copy that do not clarify structure, state, meaning, or brand.

### Text roles

- **Heading:** states the claim, topic, or decision. Keep it short.
- **Label:** names a field, control, category, or compact metadata value.
- **Copy:** explains meaning or consequence. Give it more line height than a label.
- **Precision metadata:** timestamps, identifiers, measurements, commands, and code. Mono may help here.
- **Action:** describes the result of activation, not the component's location.

Do not use tiny uppercase labels as ordinary body copy. Do not let a muted color become low-contrast text.

### Component semantics

- Use tabs only for sibling views of the same object or task, not as a generic navigation bar.
- Keep tab counts small enough to scan and make titles nouns rather than commands.
- Use badges for short, static metadata. Do not make a badge look actionable.
- Use a button or link for an action or destination.
- Use a description-list structure for compact title-value facts.
- Use containers only when they clarify grouping, persistence, or interaction.

## Geist-informed visual grammar

Geist is a system for consistent web experiences, not a license to reproduce Vercel branding. Translate its discipline rather than cloning its appearance.

### Typography first

- Use one sans family for interface and reading text.
- Use mono only where precision or code semantics benefit from it.
- If a display or pixel face is available, restrict it to one deliberate accent moment.
- Build hierarchy through role, size, line height, weight, spacing, and contrast before borders or shadows.
- Keep heading weights restrained and tracking intentional.
- Give reading copy enough line height; labels can be denser.

### Color and material

- Use the default background for most of the surface.
- Introduce a secondary background only for meaningful differentiation.
- Reserve the highest contrast for primary text and essential controls.
- Let secondary text recede without becoming faint.
- Use borders to explain boundaries, not to decorate every region.
- Keep radius, shadow, and material effects consistent and minimal.

### Grid

- Use ordinary CSS grid for responsive columns.
- Show guide lines or cells only when the grid itself is meaningful to the explanation.
- Avoid nesting visible grids.
- Make focus order match reading order.
- Treat guides as decorative for assistive technology.
- Verify contrast and legibility in both light and dark themes.

## Guidance governance

When a repeated design decision becomes a durable rule, record:

- stable rule ID
- status
- scope and trigger
- decision
- rationale
- evidence and canonical source
- exceptions and boundaries
- bad and good examples
- assumptions
- open decisions

Put deterministic rules in automated checks. Keep contextual judgment in prose and examples. Reserve policy changes and exceptions for human approval.

Evaluate guidance with holdout tasks. Score whether the outcome is correct separately from whether it resembles existing production code. Keep coverage gaps visible rather than filling them with invented certainty.

## Application to a morning brief

The brief should feel like a calm editorial scanline, not a control-room dashboard:

1. Put one start action first.
2. Include only three to five current, source-backed items.
3. Give each item a plain-language title, why it matters, suggested action, urgency, and source.
4. Include one short rehearsal, decision, or unresolved question only when it changes today's behavior.
5. Use typography and spacing before cards, badges, borders, or charts.
6. Keep optional FYI material visually subordinate.
7. End with the next physical action, not a menu of possible systems.

If the same information is clearer as concise Markdown, do not generate HTML.
