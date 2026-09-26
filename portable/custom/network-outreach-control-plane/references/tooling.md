# Tooling decisions

## Build-versus-adopt rule

Default to the bundled local implementation. Adopt a free tool only when it removes substantial engineering work, has acceptable source and license terms, requests minimal permissions, stores credentials safely, and can be removed without losing canonical data. Wrap adopted tools behind a local adapter. Record tool name, pinned version or commit, source URL, license, permissions, data sent off-device, and replacement path.

Build locally when the capability is small, security-sensitive, central to suppression or dedupe, dependent on a fragile free tier, or likely to expose the complete network export. Never outsource the authoritative ledger or stop rules.

## Recommended core

- Local Python scripts and CSV/SQLite: authoritative import, exclusions, scoring, and ledger logic.
- Codex plus official web sources: qualitative research and personalized drafting.
- `verify_public_emails.py`: dependency-free public-source and MX validation.
- Existing Gmail account: low-volume one-to-one sending, threading, Sent verification, and reply reconciliation.
- Codex Automations, Windows Task Scheduler, or a local script: scheduling without hosted workflow fees.

## Useful but not authoritative

- Self-hosted n8n Community Edition plus Ollama can schedule research and follow-up checks on the user's existing computer. It is optional because local scripts are simpler and n8n is source-available rather than a permissively licensed dependency.
- Reacher can provide optional local SMTP corroboration when outbound port 25 already works and AGPL-3.0 is compatible.
- Gooseworks GTM skill files may offer patterns, but its paid data API must not be used and installing the full catalog creates unnecessary trust surface.
- Listmonk and Mautic: designed for mailing lists and marketing automation, not individualized job outreach. Do not use them to blast social exports.

## Reject by default

- LinkedIn scrapers, browser extensions, or bots that automate profile collection or messaging
- guessed email-pattern generators presented as verification
- Hunter, Apollo, RocketReach, Snov, Clearout, or any other credit-metered discovery/enrichment dependency
- trials requiring a card, paid API keys, purchased lists, paid SMTP proxies, or paid hosting
- AgentMail or any separate sending infrastructure that introduces a new paid dependency or sender identity
- mailbox rotation, throwaway domains, or deliverability evasion
- open-source outreach repos with unclear credential storage, no stop-on-reply logic, or unmaintained dependencies
- any tool that uploads the full network export without a documented need and retention policy

## Evaluation checklist

Check source reputation, recent releases, license, issue activity, secrets handling, requested OAuth scopes, data retention, exportability, rate limits, suppression support, reply threading, and whether every required operation remains zero cost without a card or upgrade.
