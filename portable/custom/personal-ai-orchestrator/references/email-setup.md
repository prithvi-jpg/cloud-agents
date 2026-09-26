# Email Setup & Integration

Example setup and what is needed to wire email into the personal orchestrator. Verify the target laptop's actual accounts and permissions before using it.

## Example: Himalaya (Hotmail/Outlook)

- **Account:** configure an authorized Outlook address on the target device
- **Backend:** IMAP (imap-mail.outlook.com:993) + SMTP (smtp-mail.outlook.com:587)
- **Config:** `~/.config/himalaya/config.toml`
- **Read/send:** `himalaya read`, `himalaya send` after verifying local setup
- **Limits:** No Gmail API features (labels, threads, rich search)

## Optional: Gmail

Needed for:
- Label-based triage (Inbox/Promotions/Social/Updates)
- Rich search (from:boss has:attachment before:2026-08-01)
- Thread-aware replies
- Draft creation with proper threading

**Setup options:**
1. **OAuth (preferred)** — `gws` CLI via Google Workspace skills (no paid API, free for consumers)
2. **App Password** — 2FA + `himalaya` Gmail IMAP config (simpler, less secure)
3. **MCP bridge** — Codex-style Gmail plugin (not yet available in Hermes)

**Gmail guardrails (from Codex memory skills):**
- Public email attribution only (no guessed patterns)
- Gmail Sent dedupe before every send
- Ledger tracking for campaign state
- No send under: missing verifier, stop event, >3% latest-20 failure rate
- Max daily volume: free tier ~100-200/day

## Email Automation Patterns

| Pattern | What | Tool |
|---|---|---|
| Daily inbox triage | Summarize unread, flag action items | cronjob + himalaya read |
| Weekly digest | All threads with replies needed | cronjob + himalaya search |
| Campaign send | Batch outreach with dedupe + ledger | Python script + himalaya send |
| Auto-follow-up | Find sent-without-reply after N days | cronjob + himalaya search |

## Next Steps for Orchestrator

1. **Verify himalaya works** — send a test email to yourself
2. **Set up Gmail** — choose OAuth or App Password path
3. **Build daily triage** — cron job that runs morning brief + email summary
4. **Integrate with outreach** — connect Codex-style guardrails to live sending
