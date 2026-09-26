# Email discovery and verification

## Evidence ladder

1. `public_mx_valid`: exact individual work email appears on an official company, faculty, lab, professional personal, or publication page and the domain has valid MX routing.
2. `public_unconfirmed`: the address has a cited public source, but automated source matching or mail-routing validation is inconclusive. Hold for manual review.
3. `accept_all`: domain accepts arbitrary recipients. Mailbox existence is not proven. Hold by default.
4. `unknown`: SMTP is blocked, greylisted, throttled, or inconclusive. Hold.
5. `invalid`: syntax, domain, MX, or mailbox validation fails. Suppress.
6. `not_found`: no exact published address. Use a public contact form or skip; never guess.

## Required provenance

Record the exact email, source URL, source type, discovery timestamp, source-page match, DNS resolver, MX records, verification timestamp, result, catch-all state, and notes.

## Tool behavior

Run `scripts/verify_public_emails.py` first. It uses Python's standard library, fetches the cited page, checks for the exact email, and queries public DNS-over-HTTPS for MX records. No API key or paid account is required.

Reacher's `check-if-email-exists` is open source under AGPL-3.0 and can run locally, but SMTP verification often requires outbound port 25 and may produce unknown or catch-all results. Use it only as optional corroboration, not sole proof or a required service.

MX existence proves only that a domain receives mail. A published address plus valid MX is strong evidence, not a guarantee that the mailbox is active or monitored.

## Freshness

Re-check the public source and MX within 72 hours of the first send. Re-check before a follow-up if the first message bounced or the company changed domains. Never reuse a previously invalid address.
