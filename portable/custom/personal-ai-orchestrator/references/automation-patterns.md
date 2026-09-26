# Automation Patterns

Cron job recipes, watchdog scripts, and batch pipeline templates for the
personal orchestrator.

## Daily Morning Brief

**What:** Summarize overnight email, today's meetings, top 3 priorities.
**When:** Every weekday 8am.

```yaml
# cronjob.create example
schedule: "0 8 * * 1-5"
prompt: "Run the morning brief: (1) Check email for anything urgent, (2) Scan calendar for today, (3) Read STATE.md for the current focus, (4) Produce a 5-line brief — 3 priorities, 1 risk, 1 next action."
```

## Weekly Review

**What:** Summarize the week, plan next week, update metrics.
**When:** Every Sunday evening.

```yaml
schedule: "0 18 * * 0"
prompt: "Weekly review: summarize progress on all active projects, identify what's blocked, propose next week's priorities."
```

## Email Triage

**What:** Scan inbox for action items, drafts needed, or opportunities.
**When:** 3x daily (morning, midday, evening).

```yaml
schedule: "0 8,13,18 * * 1-5"
prompt: "Email triage: list all unread messages, classify as 'needs reply' / 'action item' / 'informational' / 'ignore'. For each, suggest a 1-line response."
```

## Outreach Sweep

**What:** Find applications without follow-up, send reminders.
**When:** Every 3 days.

## Watchdog Patterns

### Monitor a URL
```bash
# Check if a site returns 200, alert on change
curl -s -o /dev/null -w "%{http_code}" https://example.com
```

### Check CI status
```bash
gh run list --repo owner/repo --limit 3
```

### Verify a deployment
```bash
curl -s https://api.example.com/health
```

## Batch Pipelines

### Parallel email sends
- Use `delegate_task` with `tasks=[]` for 3-5 parallel children
- Each child: compose + send via `himalaya`
- Deduplicate against Gmail Sent first

### Application tracking
- SQLite ledger: company, role, date_applied, last_follow_up, status
- Cron job: scan for stale applications (no reply in 7 days), suggest follow-up

## Sender Health Gates (from Codex)
- No send without verified public email (MX valid)
- No send if Gmail Sent contains the address
- No send if campaign ledger shows prior bounce/rejection
- Stop if latest-20 failure rate > 3%
- Draft-only for: friends, known contacts, peers, PES affiliations
