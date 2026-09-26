# PRD — `<feature/product>`

---

## Problem

`<Subject>` is `<problem>` due to `<root cause>`, causing `<quantified impact>`.

**Evidence:** (research, data, tickets — what makes this true rather than assumed)

**The invisible version of this problem:** what users have adapted to and stopped
reporting.

---

## Users

**Who** (specific, behavioral — not a demographic):
**How their need is met today** (including spreadsheets, manual workarounds, doing
nothing):
**Psychographics** — why they behave this way:

---

## Intent

What this product is *saying* to the user. What they should feel. How the design makes
that felt without stating it.

---

## Jobs to be done

> When I `<trigger/situation>`, I want to `<motivation>`, so I can `<outcome>`.

**Task analysis of that job** — the action sequence, annotated with cognitive cost:
1. action — cost
2. action — cost ← the expensive step; this is the design target

---

## Goals / Non-goals

**Goals:**
**Non-goals** (explicitly out of scope, and why):

---

## User stories

Ranked by **proximity to root cause**, not by effort or by who asked.

| # | Story | Root-cause proximity | Acceptance criteria |
|---|---|---|---|
| 1 | As a…, I want…, so that… | direct | Given/When/Then |

---

## Solution

**What we build now:** (the wedge — buildable this cycle)
**Why this and not the alternatives:**
**Trust ladder:** where this starts (read-only? suggest? act?) and what earns the next rung
**Later stack:** what this unlocks

---

## Success metrics — defined *before* launch

**North Star:**

| Goal | Signal | Metric | Target |
|---|---|---|---|
| | | | |

**HEART where relevant:** Happiness / Engagement / Adoption / Retention / Task Success

**Experiment design** (if testing): OEC · randomization unit · per-capita metrics ·
novelty-effect window · CI

---

## Guardrails and risks

| Risk | Type | Mitigation |
|---|---|---|
| | false positives / latency / platform limits / privacy / abuse / degradation | |

**STRIDE** (if it acts on user data or on the user's behalf): spoofing · tampering ·
repudiation · information disclosure · DoS · elevation of privilege

**Behavior when there is no right answer:**

---

## Second-order effects

We ship this → first-order → **and then what happens?** → **and then?**
Include at least one effect that is bad.

---

## Evaluation chain

Users → Revenue → Privacy → UI → Eng effort → Regulatory

---

## Milestones

| Milestone | Scope | Exit criteria |
|---|---|---|
