# The AI-Era Edge — designing intelligent products

The most original and most personally-held territory. Apply this to anything involving
AI, agents, conversational interfaces, or generative UI.

---

## 1. Voice is a cognitive bypass

> *"Typing forces users to pre-structure and filter thoughts, which takes mental effort.
> Voice allows raw, frictionless brain dumps... the friction of capturing context drops to
> near zero."*

**On input:** typing is a compression step the user performs *before* the system sees
anything. That compression loses exactly the context an intelligent system needs. Voice
removes the pre-structuring tax.

**On output:** audio-first briefings solve **visual fatigue**. If someone has been staring
at dashboards for six hours, another dashboard is not help.

**Applied:** when a product needs rich context from a user, ask whether you are taxing them
to produce structure that the system could infer.

---

## 2. More text is not more help

> *"Adding more text via an AI chat interface actually increased cognitive load."*

A genuinely counterintuitive research finding, and one worth defending. The intuition —
more explanation helps — is wrong often enough that it should be treated as a hypothesis,
not a default.

**Applied:** when an AI feature is confusing, the first instinct is to explain more. Test
the opposite. The fix is frequently *less* text, better placed, or a different modality
entirely.

---

## 3. Agents must earn delegation

**Trust → action. In that order, always.**

> *"Autonomy with Accountability: agents act within clearly defined guardrails; every action
> is logged and reversible."*

The three requirements for any agent that acts on a user's behalf:

- **Clearly defined guardrails** — the boundary is legible to the user *before* the agent
  acts, not discovered afterward
- **Every action logged** — an unobservable agent cannot be trusted no matter how good
- **Every action reversible** — reversibility is what makes delegation psychologically
  affordable

**The delegation ladder:** read-only → suggest → act-with-confirmation → act-and-report →
autonomous. Products that start at the top fail even when the model is good, because trust
is earned sequentially and cannot be assumed.

---

## 4. Conversational UI has a trust fragility

> *"Conversations as UX feel natural and expectations are really high, so trust is easily
> lost when it doesn't work. Tasks or actions matter."*

Conversation sets human expectations, and humans are unforgiving of near-human failure.
The interface promises understanding; a single miss reads as a broken promise, not a bug.

**The question to always ask: how does the system behave when there is no right answer?**
That behavior — not the happy path — determines whether the product is trusted. Most
conversational products are designed entirely for the case where they succeed.

**Also:** conversation is not the goal. Tasks and actions are. A delightful chat that
completes nothing is a failure with good reviews.

---

## 5. Design for the process gulf

Generative AI **breaks wireframes** (Yang et al.). The standard design process is
inadequate because of two properties:

- **Capability uncertainty** — you cannot know in advance what the system can do
- **Output complexity** — you cannot draw the output, because it varies per user, per input

**Consequences for practice:**
- **Prototyping with prompts is now a design activity.** Designers prompt.
- **Prompts are design artifacts** — versioned, reviewed, owned by design, not buried in
  code.
- You cannot design the screen before you know the behavior; explore behavior first,
  interface second.

---

## 6. Human–agent ratio is a design decision

People want **collaborative AI, not replacement** (Human Agency Scale). The ratio of human
control to machine autonomy is a *decision you make per task*, not a global setting — and
it should be re-decided per task within one product.

Requirements for agents in the loop:
- **Legible** — the user can tell what it is doing and why
- **Interruptible** — it can be stopped mid-action, cheaply
- **Explainable** — per XAIR: decide **when** to explain, **what** to explain, and **how**.
  Constant explanation is noise; no explanation is opacity. The *when* is the hard part.

Ties directly to the conviction that **agency and willfulness are the scarce resources**
(`philosophy.md` §4): AI should amplify human willfulness, not absorb it.

---

## 7. Personal computing → personalized software

The thesis bet: **generative UI that adapts per user, per context.**

> *"The next Jarvis-style AI that provides information in customized visual form instead of
> just audio."*

Software stops being one artifact shown to everyone and becomes an artifact *composed for
this person, in this moment, for this task.* The interface itself becomes an output of the
model. This is the frontier being built toward — and the open questions (consistency,
learnability, trust in a UI that changes, how you support someone whose screen you cannot
see) are the real design work.

---

## 8. UXR cannot ignore the philosophy questions

> *"What is good and what is bad? What moves people, drives opinions and decisions... make
> it more difficult to make bad decisions."*

Ethics is a **design input**, not a compliance step. The goal is structural: make bad
decisions *harder to make*. For AI products this is sharper than usual, because these
systems shape what people believe is possible and true.

---

## 9. The standing bet: AI + AR collective intelligence

> *"The mother of all demos comes back with holistic AI and AR augmenting collective
> intelligence."*

Held as a live thesis, not a conclusion. Keep collecting evidence **for and against** —
and note the against, since a bet you only collect confirmation for is not a bet.

---

## AI product design checklist

- [ ] Where on the delegation ladder does this start? What earns the next rung?
- [ ] What happens when there is **no right answer**? Design that path first.
- [ ] Is every action logged and reversible?
- [ ] Are the guardrails legible *before* the agent acts?
- [ ] Human–agent ratio decided per task — does this augment agency or absorb it?
- [ ] When / what / how to explain — decided, not defaulted
- [ ] Is the input modality taxing the user to pre-structure thoughts?
- [ ] Am I adding text where I should be removing it?
- [ ] Have I prototyped the behavior before designing the screen?
- [ ] Black Mirror pass: what is the worst version of this, and who does it harm?
