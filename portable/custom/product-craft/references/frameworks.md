# Analytical Frameworks — the working toolkit

The structured tools for analysis, cases, root-cause work, and estimation. Use these
*inside* the engine, not instead of it. A framework applied without understanding produces
a confident wrong answer, which is worse than an uncertain right one.

---

## 1. System architecture basics

**Request flow:**

```
Client → CDN (is the object here?) → Load Balancer → Web Server → Database
```

**Caching and optimization:** if the object is not in the CDN → fetch from server/cache →
send back to client.

**Why a PM needs this:** latency, cost, and failure modes are product decisions. Where a
thing is cached determines how fresh it is, what it costs, and how it breaks — all of
which the user feels. You cannot make a real tradeoff call without knowing where the
request goes.

---

## 2. Root Cause Analysis (RCA) — metric drop

### MECE

**M**utually **E**xclusive, **C**ollectively **E**xhaustive — the branches must not overlap
and together must cover everything. This is what stops an investigation from being a
list of guesses.

```
                             [ METRIC AFFECTED ]
                                      |
         +--------------------+-------+-------+--------------------+
         |                    |               |                    |
     [ SYSTEM ]          [ EXTERNAL ]    [ INTERNAL ]     [ OUT OF CONTROL ]
         |                    |               |                    |
  - Metric Logger     - Competitors    - New Products       - Political Changes
  - Metric            - External News    & Features         - Natural Disasters
    Calculation       - Trending       - Specific Devices
                        Market           Affected
                      - Demographics   - Product
                      - Seasonality      Cannibalization
                                       - High Volume of
                                         Errors & Feedback
```

**Always check SYSTEM first.** A large share of "metric dropped" incidents are logging or
calculation changes, not behavior changes. Confirm the metric is real before investigating
why reality changed.

### Investigation steps

1. **Understand the product** — what it does, who uses it, what the metric means
2. **MECE breakdown:** `Users → Journey` — segment the users, then walk the journey
3. **Get data for each segment** — platform, geo, cohort, device, tenure, funnel step
4. **Hypothesize** — form falsifiable hypotheses, then test against the data

Also establish: **when** did it start, is it a **step change or a gradual drift**, is it
**one segment or all**? Step change in one segment = a release or an outage. Gradual drift
across all = market, seasonality, or cannibalization.

---

## 3. Guesstimates — worked example: Gmail ad revenue

```
[ Total Annual Income: $11.6B ]
             |
             v  (divide by 52 weeks)
[ Gmail Weekly Revenue: ~$223M/week ]
             |
             v  (divide by 7 days)
[ Total Daily Revenue ]  ×  [ Cost per Click ]
             |
             v
[ Total Ads per Week ]  ×  [ Click-Through Rate (e.g. 0.01%) ]
             |
             v
[ Total Sessions ] = [ Ads per Session (e.g. 62) ] × [ Total Users ] (small vs. large users)
```

**Method:** anchor on a known top-line number → decompose by time → decompose by the unit
economics chain (revenue = impressions × CTR × CPC) → bottom out at users × sessions ×
ads per session. **Segment users into small vs. large** — averages across a skewed
population produce nonsense.

**What matters is the structure, not the answer.** State assumptions out loud, keep the
arithmetic round, and sanity-check the result against something you know.

---

## 4. ROI and solution analysis

Run any proposed solution through these five columns before committing.

| Impact & Unknowns | Scalability | Backward Compatibility | Performance & Engineering | Security (STRIDE) |
|---|---|---|---|---|
| Who will be impacted? | Does the solution scale? | Roll-out plan | Performance & application speed | See STRIDE below |
| What are the unknowns? | | Migration / compatibility | Feasible dev time & resources | |

### STRIDE threat model

| Threat | Meaning |
|---|---|
| **S**poofing | Directing to an incorrect action / impersonation |
| **T**ampering | Modifying user data on their behalf |
| **R**epudiation | Denying an action occurred |
| **I**nformation Disclosure | Unintended data access |
| **D**enial of Service | Harm from misuse or resource exhaustion |
| **E**levation of Privilege | Unauthorized permission gain |

**Especially important for AI/agent products** — an agent that acts on a user's behalf
touches nearly every row: spoofing (acting as the user), tampering (modifying their data),
repudiation (was it the agent or the human?), and elevation (scope creep in permissions).

---

## 5. PM frameworks

### STAR

**S**ituation → **T**ask → **A**ction → **R**esult

Workflow form: `Goals → Action → Metric → Evaluation`

### Product design flow

```
[ Users ] → [ Pain Points ] → [ Ideas / Solution ] → [ Vision ] → [ Feature Priority ] → [ Pitfalls ]
```

**Key questions:**
- Who are the users?
- What do they want?
- **How are their needs being met today?** ← the one people skip, and the one that reveals
  the real competitor (usually a spreadsheet or a workaround)

**Evaluation criteria:** `Metrics / Privacy → Profit over 3 years`, plus **Retention** and
**Risk Mitigation**.

### CIRCLES — product design questions

| | Step | What you do |
|---|---|---|
| **C** | Comprehend the Situation | What? / Why? / How? / Who? |
| **I** | Identify the Customer | Choose and justify a specific user |
| **R** | Report the Customer's Needs | State needs as jobs / user stories |
| **C** | Cut Through Prioritization | ROI estimate; what matters most and why |
| **L** | List Solutions | Brainstorm features — go wide |
| **E** | Evaluate Trade-offs | Be thoughtful, analytical, objective |
| **S** | Summarize Recommendation | Clear, actionable summary |

The two most commonly botched steps: **I** (picking a customer specific enough to design
for) and **E** (actually naming what you give up).

### HEART — UX metrics

```
[ Happiness ] → [ Engagement ] → [ Adoption ] → [ Retention ] → [ Task Success ]
```

**Map each to `Goals → Signals → Metrics`.** HEART without GSM is a vocabulary, not a
measurement system.

### AARRR funnel

1. **A**cquisition / Reach
2. **A**ctivation
3. **R**etention — *sticks; solves a symptom; should be easy to use*
4. **R**eferral
5. **R**evenue

Retention is the load-bearing one — acquisition without retention is a leaking bucket you
are paying to fill.

---

## 6. Company goals and strategic considerations

**Core evaluation chain — run any proposal through all six:**

```
Users → Revenue → Privacy → UI → Eng Effort → Regulatory
```

**MECE categorization of metrics:**
- **Revenue metrics** vs. **Non-revenue metrics** (engagement, retention)

Keeping these separate prevents the classic trap of justifying an engagement win that
costs revenue, or a revenue win that burns retention.

### Case example — Spotify

- **Scope:** *Spotify exists everywhere* — the product is not the app, it is presence
  across every context in which a person listens
- **Value proposition:** fit for purpose → search, discovery, curation, podcasts
- **Ecosystem balance:** support small artists hand-in-hand with big artists

**The generalizable lesson:** a marketplace/platform has *two* customers whose interests
diverge, and the strategy is the balance between them — not the optimization of either.
Whenever you analyze a platform, ask who the second customer is and what balance is being
struck.

---

## When to reach for which

| Situation | Tool |
|---|---|
| A metric moved and nobody knows why | RCA + MECE tree, system branch first |
| "How big is this market/opportunity?" | Guesstimate decomposition |
| "Design a product for X" | CIRCLES, product design flow |
| "Should we build this?" | ROI table + core evaluation chain |
| "How will we know it worked?" | HEART + GSM; AARRR for lifecycle |
| Agent or data-touching feature | STRIDE |
| Behavioral question about the story | STAR |
