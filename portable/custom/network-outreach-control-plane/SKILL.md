---
name: network-outreach-control-plane
description: Run a zero-cost personal network and relationship outreach control plane from official LinkedIn and X/Twitter exports plus Gmail threads. Build explainable relationship circles, preserve conversation continuity, protect friends and known contacts from cold automation, identify U.S. founders and hiring decision-makers, verify exact publicly published professional emails, draft human work-first introductions, pace Gmail sends, hand substantive replies to the user, and maintain auditable state. Use for personal network dashboards, relationship care, free export-driven networking, founder or hiring-manager discovery, public email verification, and Gmail-safe communication.
---

# Network Outreach Control Plane

Build a relationship system first and a reviewed, evidence-backed outreach queue second. Never turn a social export directly into a sending list.

## Preserve the conceptual boundaries

Model these facts independently:

- `circle_explicit`: inner, close, familiar, new, or unknown; the user owns this field.
- `relationship_goal`: maintain, explore, opportunity, or pause.
- `contact_policy`: remind_only, draft_only, networking_allowed, no_job_outreach, or do_not_contact.
- `campaign_eligibility`: unknown, researching, eligible, held, or excluded.
- `contactability`: unknown, public_source_found, mx_valid, contactable, bounced, rejected, or unsubscribed.

A friend can be close and excluded. A U.S. founder can be new and eligible. A bounced address can remain a valuable relationship.

Keep people, identities, affiliations, conversations, messages, relationship decisions, evidence edges, next actions, automation actions, and stop events as separate objects. Allow many email or platform identities to resolve to one person, but never merge X and LinkedIn identities from names alone.

Treat one-to-one human messages as relationship evidence. Treat group-thread co-presence and shared organizations as shared context only. Never draw or claim a person-to-person connection that the exports do not prove.

## Enforce zero incremental cost

- Use only existing local compute, open-source software, public web sources, and the user's existing Gmail account.
- Do not use paid enrichment, credit-based finders, paid APIs, purchased lists, trials requiring a card, paid proxies, paid hosting, or mailbox rotation.
- A free tier that can later block the workflow is not a core dependency.
- Before adding any tool, record its license, hosting location, credential needs, and monetary cost. Stop if the required cost is not zero.
- Accept lower coverage. If an exact email is not publicly published and freely verifiable, set `not_found` and use an official contact form or skip.

## Build first, adopt selectively

Own the critical workflow locally. Build import, identity matching, exclusions, scoring, evidence capture, verification state, approval, sending state, ledgers, and dashboards inside this skill or its local companion application.

Use an external agent, package, or MCP only when all of these are true:

1. It is genuinely free for the complete intended workflow, without expiring credits or a required card.
2. Its source, license, maintenance, permissions, and credential handling are inspectable and acceptable.
3. It is materially easier or more reliable than a small local implementation.
4. It is replaceable through a narrow adapter and never becomes the system of record.

Otherwise, implement the capability locally. Prefer Python standard library, SQLite, and self-contained HTML before adding dependencies. The user has authorized installing a qualifying free tool after this inspection; log the tool, version, license, source, and reason for adoption.

## Run the engineering evaluation loop

The requested `/loop` skill is not installed. Use `references/engineering-loop.md` as the bounded replacement. Every milestone must pass deterministic, privacy, delivery-safety, and HCI gates before promotion. Narrative confidence is not verification.

## Start with the local control plane

1. Read the candidate handoff, resume, campaign ledger, reply-event log, and this automation's memory when available.
2. Run `scripts/prepare_review.py` on the supplied LinkedIn and X exports.
3. Give the user the generated relationship workspace. Let them set a circle, relationship goal, and contact policy independently; persist the decisions to SQLite rather than browser storage alone.
4. Run `scripts/build_lead_queue.py` with the exported decisions. Treat only `Target` rows as candidates.

Do not scrape or automate LinkedIn. Use the member-provided official export. Read `references/architecture.md` for expected export shapes and system stages.

## Qualify before email research

For each target:

1. Confirm the person's current employer and title from a current official company, personal, GitHub, publication, or other public source.
2. Require one target role: founder/cofounder, C-suite, VP, director, head, engineering manager, hiring manager, recruiting leader, or recruiter. Hold ambiguous `manager` titles for review.
3. Require a concrete fit or timing signal: active role, hiring announcement, funding, launch, product shift, recent publication, or clearly relevant team problem.
4. Search the campaign ledger and mailbox before enrichment. Stop on any previous substantive reply, rejection, bounce, unsubscribe, or equivalent outreach.
5. Rank the queue. Research only the highest-value unsent contacts so human review time stays bounded.

## Discover email without guessing

Apply the evidence ladder in `references/email-verification.md`.

- Require an exact individual work email published on an official company, faculty, lab, professional personal, or publication page.
- Run `scripts/verify_public_emails.py` to confirm that the cited page contains the exact address and that the domain publishes working MX records.
- Reacher may be used locally only when its AGPL license is compatible and outbound port 25 already works. It is optional and never a required dependency.
- Do not use Hunter or another credit-based finder in zero-cost mode, including a limited free tier.
- Never synthesize an email pattern and call it verified.
- Never use a personal email unless the person published it for professional contact and the user approves that channel.

Set `email_status` to one of: `public_mx_valid`, `public_unconfirmed`, `accept_all`, `unknown`, `invalid`, or `not_found`. Only `public_mx_valid` is sendable by default.

## Draft human, one-to-one communication

- Research the person and company immediately before drafting.
- For a first note, open with one specific current observation about their work.
- Offer a thoughtful interpretation, useful connection, or concrete insight from Prithvi's HCI product-builder perspective.
- Establish genuine context briefly and ask one easy human question.
- Do not lead with job availability, a role request, a meeting request, or a resume.
- Keep the first note concise, warm, curious, direct, and free of em dashes.
- Do not attach a resume to the first relationship note.
- Permit role context only in a later stage when the conversation or a new signal makes it natural.
- Include an easy opt-out sentence when the message could reasonably be treated as commercial or repeated outreach.

For known contacts, create private care reminders or reviewable drafts only. Never auto-send to friends, known contacts, peer-level contacts, PES affiliations, or Bangalore/Bengaluru signals.

## Deliver through a paced queue

Use the user's existing Gmail account for the conversation record. Use Codex Automations, Windows Task Scheduler, or a local script for orchestration. Do not require a hosted automation service.

Before every send:

1. Re-check ledger and Gmail dedupe.
2. Re-check verification freshness and source evidence.
3. Confirm status is `approved_to_send` and no stop event exists.
4. Send sequentially, never in a burst. Start with one relationship canary, permit at most 3 new messages per weekday only after a healthy canary period, wait at least 90 seconds between messages, and contact no more than 2 people per company per 30 days.
5. Verify the exact message in Sent plus Gmail message/thread IDs. Verify an attachment only when the approved message intentionally includes one.
6. Append the campaign row immediately.

Stop the run on Gmail quota/rate errors, two consecutive send failures, bounce rate above 3% over the latest 20 sends, or any inability to perform mandatory dedupe. Do not route around a damaged sender reputation with throwaway inboxes.

## Reconcile and follow up

- Append immutable reply events before new sends.
- Separate automated acknowledgments, bounces, human replies, positive replies, rejections, and unsubscribes.
- Stop all scheduled sends after a bounce, rejection, unsubscribe, or substantive reply.
- A substantive reply creates a human-handoff task. The system may draft from the full thread, but it must not autonomously impersonate an ongoing personal relationship.
- Send at most one follow-up after 7 business days, and only with a concrete new contribution or current signal.
- Never exceed two unanswered messages in a thread and never send a hollow check-in.

## Evaluate tools conservatively

Read `references/tooling.md` before adding an agent, MCP, npm package, or sending platform. Inspect source, license, maintenance, permissions, credential handling, and actual monetary cost. Reject any required paid or credit-metered dependency. This workflow is authorized to install a qualifying zero-cost tool only when it passes the build-versus-adopt test above.

## Required outputs

Maintain:

- normalized contacts CSV
- user decisions CSV
- qualified lead queue CSV
- evidence and verification fields
- immutable campaign and reply-event ledgers
- a review dashboard with separate counts for source, target class, verification state, delivery, reply, positive reply, and suppression reason
- relationship circles, conversation timelines, relationship-care reminders, explainable network-edge provenance, and a visible automation activity trace
- an architecture decision record and engineering-loop result for every promoted milestone
