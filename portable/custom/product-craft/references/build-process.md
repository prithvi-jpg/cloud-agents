# The Building Process — from problem to shipped product

The loop from understanding to a shipped, measured thing.

---

## 1. Frame the problem first — and frame it well

> *"Design thinking = looking for a problem first, framing the problem really well. Did the
> effort really hear the customer voice? Do not reinvent the wheel. Work backwards from a
> problem."*

Three checks before any solution work:

- **Did the effort truly hear the customer voice**, or a proxy for it?
- **Are we reinventing the wheel?** Someone has probably solved a version of this.
- **Are we working backwards from a problem**, or forwards from a capability we happen to
  have? Forwards-from-capability is the most common way good teams build useless things.

---

## 2. Write the problem statement with the cause inside it

**Form:** `<Subject> is <problem> due to <root cause>, causing <quantified impact>.`

**The model:**
> *"Supreme's ad spend is being optimized toward fraudulent traffic due to inaccurate pixel
> signals and lack of automated guardrails, causing 40% of traffic from non-target
> segments."*

Problem → root cause → measurable impact, in one sentence.

**Why the cause must be inside it:** a problem statement without a root cause produces
solutions aimed at symptoms, and symptom-solutions always look reasonable in review. The
quantified impact is what makes prioritization possible later — without a number, every
problem is equally urgent, which means none are.

---

## 3. Convert to JTBD and user stories

> *"When I launch campaigns, I want to deliver ads within my target segment and optimize to
> real conversions, so my budget isn't wasted."*

Then **rank stories by proximity to the root cause.** Not by effort, not by enthusiasm, not
by who asked. The story closest to the root cause is the one that, if solved, collapses
the most downstream symptoms.

Every story must be **testable** and map to acceptance criteria an engineer can consume.

---

## 4. Ideate wide, then converge

- **100 > 10 > 1** — generate 100 ideas; 10 get one slide each; 1 gets built. The width is
  not decoration; the 87th idea is where the non-obvious ones live.
- **Crazy 8s** — eight sketches, eight minutes. Speed defeats self-editing.
- **"Yes, and…"** — build before you critique.
- **"I Like / I Wish / I Wonder"** — critique structure that keeps people generative.
- **Silent critiques** — everyone writes before anyone speaks, so the loudest voice does
  not set the anchor.

---

## 5. Prototype to learn, not to be right

> *"The best thing about prototyping is you get instant feedback... and decide on features
> then and there itself. Feedback can inspire features users deeply connect with."*

- **Lo-fi for ideation** — cheap enough that you are willing to be wrong
- **Hi-fi for validation** — real enough that the feedback is about the product, not the
  fidelity

The purpose is instant feedback and features that emerge from real reactions. A prototype
built to prove you were right is a demo, and demos teach nothing.

---

## 6. Ship small — read-only first when trust is at stake

Earn trust before asking for action. The read-only version is the trust-building instrument,
not a reduced-scope compromise. (Ribbit Wrapped: *"read-only by design → earns trust before
action."*)

---

## 7. Measure what matters — defined before launch

**Define metrics during the design, not after.** Metrics chosen after the build exist to
justify it.

---

## 8. Name guardrails and risks explicitly

Always list them: false positives, latency, platform limits, privacy exposure, abuse
vectors, degradation when the model/system is wrong. A recommendation without named risks
reads as naive to anyone senior, and more importantly, unnamed risks do not get designed
for.

---

## Metric frameworks

| Framework | What it measures | Use when |
|---|---|---|
| **HEART** | Happiness, Engagement, Adoption, Retention, Task Success | UX quality of a feature or product surface |
| **Goals → Signals → Metrics** | Links product goals to observable signals to countable metrics | Always — this is the bridge that stops metric theater |
| **North Star + supporting** | One primary (e.g. Share Rate) with activation/conversion beneath | Product-level focus and org alignment |
| **Detection / quality metrics** | MTTD, precision, duplication rate | Anything detection-, safety-, or ML-driven |
| **Core values → attributes → metrics** | Under each core value define the attribute; under each attribute the metric | Human-factors evaluation; making abstract values measurable |
| **Experimentation rigor** | Clear OEC, randomization unit, per-capita metrics, novelty effect, 95% CI | Any A/B test — all five, or the result is not a result |

**The GSM discipline is the important one.** Goal (what we want), Signal (what would be
observably different if we got it), Metric (the countable form of that signal). Most bad
metrics are signals skipped — a goal wired directly to whatever was easy to count.

**Experimentation gotchas to always check:** Is the OEC stated in advance? Is the
randomization unit right (user, not session, when learning effects exist)? Are metrics
per-capita rather than absolute? Is this a novelty effect that decays? Does the CI actually
exclude zero?

---

## Strategy toolkit

### Competitive analysis, done right

The default version — a feature grid against the three companies you already think about —
is nearly worthless. Do this instead:

1. **Define the trigger first.** Why are we doing this *now*? A launch? Churn? A
   repositioning? The trigger determines what the analysis is for, and an analysis without a
   purpose produces a slide nobody uses.
2. **Find competitors from the user's frame of reference.** *"What they're choosing between,
   not who you think you're up against."* This includes **spreadsheets, manual workarounds,
   WhatsApp groups, and doing nothing.** For most products, the real competitor is inertia.
3. **Study emotional drivers and switching behavior**, not feature parity. Why did someone
   leave? What did it cost them emotionally to switch? What would it take again?

### The rest of the toolkit

- **SWOT** — internal/external position
- **5 C's** — Company, Customers, Competitors, Collaborators, Context
- **Positioning maps** — where you sit on the two axes the customer actually uses
- **JTBD comparison** — same job, different hires; the most honest competitive lens
- **Business Model Canvas** — how the money actually moves
- **Situation → Complication → Resolution** — the structure for making any recommendation
  land; also the fastest way to test whether you have a real recommendation

---

## The build loop, in order

1. Frame the problem (with cause and impact inside the statement)
2. Convert to JTBD + testable user stories, ranked by root-cause proximity
3. Ideate wide (100 > 10 > 1), converge deliberately
4. Prototype to learn — lo-fi to explore, hi-fi to validate
5. Ship small; read-only first where trust is at stake
6. Metrics and guardrails defined *before* launch
7. Measure, then reflect: second-order effects, what did I miss, update the framework
