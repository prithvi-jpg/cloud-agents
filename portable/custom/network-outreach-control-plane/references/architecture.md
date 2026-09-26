# Architecture

## Stages

`official exports -> normalized people -> user exclusions -> role and company research -> ranked targets -> email discovery -> verification -> approval -> paced send -> reply reconciliation`

Each transition writes a durable file. No downstream stage may silently rewrite an upstream decision.

## Export inputs

LinkedIn normally supplies `Connections.csv` with fields similar to First Name, Last Name, URL, Email Address, Company, Position, and Connected On. Missing emails are expected because LinkedIn only exports addresses members allow connections to download.

X archives commonly contain `data/following.js` with `window.YTD.following.part0 = [...]`. Each item has an account ID and user link. Display names and titles usually require later public research.

Accept a ZIP, directory, CSV, or JS file. Preserve raw source values and add normalized fields rather than modifying the export.

## Identity and dedupe

Use stable identifiers in this order:

1. LinkedIn profile URL
2. X handle or profile URL
3. normalized professional email
4. normalized full name plus company

Do not merge two people solely because names match.

## Review decisions

- `target`: eligible for research, not for automatic send
- `known_person`: user knows the person and does not want cold outreach
- `peer_level`: same-level contact excluded from this decision-maker campaign
- `do_not_contact`: permanent suppression
- `research_later`: potentially useful but incomplete
- `unreviewed`: no user decision

User decisions override scoring. Suppressions are append-only unless the user explicitly changes them.

## Target scoring baseline

- founder/cofounder/owner: 35
- C-suite/VP/head/director: 28
- engineering or hiring manager: 24
- recruiter/talent acquisition: 20
- current hiring or role signal: 20
- strong candidate evidence match: 15
- official public contact route: 10
- prior reply or known person: hard stop

Use scores to order research, never to decide whether a human relationship should be contacted.

## Recommended data model

Keep `contacts.csv`, `decisions.csv`, `lead_queue.csv`, `campaign_ledger.csv`, and `reply_events.csv`. Add fields for source URL, source date, company domain, role class, fit signal, email source type, verification provider, verification timestamp, confidence, catch-all, approval, Gmail IDs, status, and suppression reason.
