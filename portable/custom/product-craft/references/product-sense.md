# Product Sense — how to perceive like a PM

Product sense is not innate taste. It is trained perception plus a habit of asking better
questions than the situation requires. This file holds the training practices and the
interview craft.

---

## Daily perception habits

These build the eye. They are cumulative and boring, which is why they work.

**Sketchbook practice.** Record interactions and products that stand out. It builds a
designer's eye and forces the question: *what was the product thought process that went
behind making this?* Not "do I like it" — *what decision produced this?*

**Love It / Hate It lists.** Three designs you love, three you hate, with reasons. Trains
taste by forcing articulation. The reason is the artifact; the list is just scaffolding.

**Product teardowns.** Take ~15 products across different themes. For each, write what you
would build at that company and where they should take the product. Teardowns convert
consumption into judgment.

**Psychographics over demographics.** Understand *why* people behave, not just *who* they
are. Demographics predict segments; psychographics predict behavior. Only one of those
tells you what to build.

---

## JTBD + Task Analysis — the synthesis

> *"If we can combine jobs-to-be-done (struggles, progress, triggers, outcomes) with task
> analysis (actions + cognitive processes), we create a powerful technique to build UX
> that deeply understands users."*

This is the personal synthesis, and it is genuinely more powerful than either alone:

| Layer | Gives you | Answers |
|---|---|---|
| **JTBD** | struggles, progress sought, triggers, desired outcomes | *Why* they move, and *when* |
| **Task analysis** | the actions taken + the cognitive processes behind them | *How* they move, and *where it costs them* |

JTBD alone tells you what to build but not where it breaks. Task analysis alone tells you
where it breaks but not whether it matters. Together they produce UX that understands
users at both the motivational and the mechanical level.

**Practice:** write the job statement, then decompose the job into the actual action
sequence, then annotate each action with the cognitive load it carries. The expensive
steps are your design targets.

**Job statement form:**
> When I `<situation/trigger>`, I want to `<motivation>`, so I can `<expected outcome>`.

---

## Interview craft

### The moves

- **"Yes, and || why?"** — build on the answer, then probe the reason. The second layer is
  where the truth is.
- **Leave comfortable silence.** The interviewee will fill it, and what they fill it with
  is usually more honest than the answer to your question. Comfortable is the operative
  word — silence that reads as judgment shuts people down.
- **Photo journals / phone galleries as prompts.** Artifacts beat recall. People
  reconstruct their life accurately when looking at evidence of it.
- **Never make a character out of the interviewee.** They are not a persona, an archetype,
  or a quote to be harvested. Flattening a person into a type is how you end up designing
  for someone who does not exist.
- **Retrospective questions.** *"Walk me through a time when..."* triggers real memory
  rather than opinion. Memory is data. Opinion is noise dressed as data.

### Question types to avoid

| Avoid | Because |
|---|---|
| Leading | You get your own hypothesis back |
| Double-barreled | You cannot tell which half they answered |
| Biased | Same as leading, harder to spot in your own script |
| Hypothetical | People are terrible predictors of their own future behavior |
| Forced-choice | You imposed the option set; the real answer may not be in it |

### Saturation

- **Minimum ~15 interviews. 20–30 ideal.**
- Saturation = new interviews stop producing new codes.
- **When saturated, triangulate with surveys** — qualitative depth establishes the *what
  and why*; quantitative breadth establishes *how many*, which is what turns insight into
  a decision.

---

## The 10-questions spine

The backbone check for any design, any presentation, any recommendation. Three of them
carry most of the weight:

1. **Who cares?**
2. **What will happen?**
3. **What does this mean?**

If a deck, a doc, or a feature cannot answer these three in one line each, it is not ready
to be shown to anyone. "Who cares" must resolve to a specific human and a count. "What
will happen" must be a prediction, which means it can be wrong. "What does this mean" is
the interpretation you are being paid for — the part nobody else can do from the same data.

---

## Running a critique or teardown

Use `templates/critique.md` for the output shape. The thinking order:

1. **What is this product's intent?** Can a first-time user feel it?
2. **What job is it hired for, and what is it competing against** (including spreadsheets
   and doing nothing)?
3. **Where does the core interaction break?** Narrate the day, find the seam.
4. **What invisible problem has this product's users adapted to?**
5. **What would I build here, and why that and not the obvious thing?**
6. **Second-order:** if that shipped and worked — then what happens?
