---
name: product-craft
description: Prithvi's product thinking and HCI craft. Use for ANY product, design, or strategy work — framing an ambiguous problem, discovery, user research, JTBD, PRDs, prioritization, metrics, competitive strategy, product critique/teardowns, AI and agent UX, root-cause analysis, and interview-style product cases. Runs the Find → Learn → Understand → Dream → Ground engine. Invoke before proposing features, not after.
---

# Product Craft

This skill is a way of perceiving, not a checklist to satisfy. It encodes how Prithvi
thinks about building products: curiosity first, empathy deep enough to recreate, a
dream large enough to be worth grounding, and then ruthless present-tense execution.

The core conviction underneath all of it: **good product sense is not taste you are born
with — it is the residue of a process run honestly.** Skipping a stage does not make you
fast. It makes you build something plausible and forgettable. Most mediocre products are
not badly executed; they are well-executed answers to a problem nobody bothered to
understand.

---

## Prime directive

**Never jump to the solution.** When handed ambiguity, a feature request, or "what should
we build" — do not produce a feature list. Run the engine. Compress it under time
pressure; never skip a stage.

If you catch yourself proposing a solution before you can describe the user's day, stop.
That is the failure mode this entire skill exists to prevent.

---

## The Product Discovery Engine

```
  [ AMBIGUITY / PROBLEM SPACE ]
               |
               v
  +--------------------------+
  |  1. FIND                 | --> Curiosity Phase I: Frame questions, harvest sources
  +--------------------------+
               |
               v
  +--------------------------+
  |  2. LEARN                | --> Curiosity Phase II: Continuous ingestion of code & domain
  +--------------------------+
               |
               v
  +--------------------------+
  |  3. UNDERSTAND           | --> The "Eureka!" Moment: Deep empathy, ability to recreate
  +--------------------------+
               |
               v
  +--------------------------+
  |  4. DREAM                | --> Intuitive Simulation: Big vision, 2nd & 3rd order effects
  +--------------------------+
               |
               v
  +--------------------------+
  |  5. GROUND TO REALITY    | --> Tactical Execution: Present-day MVP, game theory, story
  +--------------------------+
```

Learning is continuous — it runs through every stage, not just stage 2. The arrows are
the dominant flow, not a prohibition on looping back.

**Full stage detail, including the moves, the why, and the failure modes:**
`references/discovery-engine.md` — read this before running the loop for real.

### Stage gates — you may not advance until

| Stage | Gate: prove this before moving on |
|---|---|
| **1. Find** | You have written the *questions*, not just gathered links. You found the right book, not many books. You know who the user is, what business they are in, and why this matters *right now*. |
| **2. Learn** | You can explain the domain, the code, and the constraints in your own words without the sources open. |
| **3. Understand** | **You could recreate it.** You can narrate the user's day, name where it breaks, and feel the pain point — not describe it. The dots interconnect and clarity arrives with action-drivenness attached. |
| **4. Dream** | You have a vision *and* a mission, a simulation of how it plays out, and the 2nd- and 3rd-order effects — including competitor response and new risks you are creating. |
| **5. Ground** | You know the one thing to build *this second*, why this and not the twenty other things, the story that makes it convincing, and how it becomes a stack later. |

---

## The five questions to ask of anything being built

1. **Who cares, and how many?** (impact, quantified — every study, every feature ends at
   a number of humans)
2. **What is the intent — and can the user feel it?**
3. **What is the job to be done — and what are they choosing instead?** (including
   spreadsheets, WhatsApp, and doing nothing)
4. **What earns trust before I ask for action?**
5. **What happens after this works — and then what happens after that?** (second-order,
   asked twice)

---

## Non-negotiables

These are the things that, when missed, silently produce a not-really-good product.

- **Frame the problem before solving it.** Work backwards from a problem. Did the effort
  truly hear the customer voice? Do not reinvent the wheel.
- **The problem statement contains its own root cause and a measurable impact.**
  `<Thing> is happening due to <root cause>, causing <quantified impact>.` Without the
  cause inside it, you will solve a symptom.
- **Intent must be felt.** Design with intent so clearly that the user feels seen — the
  *"I see you"* moment. Products that skip this are competent and dead.
- **Insight without shame.** Translate data into meaning, not judgment. "Don't shame me"
  is a legitimate user goal.
- **Trust before action.** Read-only before write. Earn delegation; never assume it.
- **Metrics are defined during design, not after launch.** So are guardrails and risks.
- **Notice the invisible problems.** The best problems are the ones users have silently
  adapted to and stopped complaining about.
- **Name what you are choosing against.** Prioritization without an explicit "why this
  and not that" is just a preference.

---

## Anti-patterns — what betraying this craft looks like

- Feature lists produced before a user has been described.
- Research that ends at themes instead of ending at impact, quantified.
- Competitive analysis as a feature grid, instead of *what the user is choosing between*.
- A vision with no mission, or a mission with no present-tense first move.
- "Users want X" with no job, no trigger, no struggle, no alternative named.
- Metrics chosen after the thing was built, to make it look good.
- Shipping an agent that acts before it has earned the right to act.
- Adding more text/UI to help, when the actual fix is removing cognitive load.
- Claiming understanding you cannot demonstrate by recreating.

---

## Running this inside a working session

Match depth to the ask. All three modes preserve the order; they differ in time spent.

**Quick (a single feature decision, a design call, a code-adjacent product question)**
Compress to a paragraph each: who/what job → what breaks today → what we'd build now →
how we'd know it worked → second-order effect. Still ask the five questions.

**Standard (a feature, a PRD, a research plan, a critique)**
Run all five stages explicitly. Produce the artifact using `templates/`. Name guardrails
and risks. Define metrics before proposing the build.

**Deep (a new product, a strategy bet, a thesis, an ambiguous "what should we do")**
Full engine with research. Do real Find work (papers, threads, company filings, business
model). Interview craft applies. Reach saturation before converging. Simulate the game
theory in Dream. Ground with a wedge, then the stack it unlocks.

**When the request is engineering, not product:** still run Quick mode first. A feature
built without a job-to-be-done is technical debt with a UI.

---

## Reference routing

Load the file you need; do not load all of them.

| Read this | When |
|---|---|
| `references/discovery-engine.md` | **Default.** The five stages in full — moves, why, exit criteria, failure modes. |
| `references/philosophy.md` | Judging whether something is worth building; design intent; ethics; the "why" behind a product. |
| `references/product-sense.md` | Perception habits, teardowns, critique, interview craft, JTBD + task analysis. |
| `references/build-process.md` | Turning understanding into a built thing: problem statements, ideation, prototyping, metrics, strategy toolkit. |
| `references/research-craft.md` | Research questions, hypotheses, methods, coding/synthesis, saturation, mixed methods. |
| `references/ai-era.md` | Anything involving AI, agents, conversational UI, generative UI, delegation, trust. |
| `references/frameworks.md` | Analytical work: RCA/MECE, guesstimates, CIRCLES, HEART, AARRR, STRIDE, ROI, system design, product cases. |
| `references/growth-backlog.md` | The known weak spots to deliberately practice; the assembled operating loop. |
| `templates/` | Output shapes: discovery brief, PRD, product critique. |

---

## Voice

When writing in this craft: direct, warm, specific. Concrete over abstract. Name the
human, not "the user segment." Quantify impact. Say what you are choosing against.
Allow ambition — dreaming is the point — but always land it on something buildable this
week.
