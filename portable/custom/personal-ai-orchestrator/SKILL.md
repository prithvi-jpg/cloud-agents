---
name: personal-ai-orchestrator
description: "Build and run a personal AI orchestrator for automated work."
version: 1.0.0
author: Prithvi Rey
license: MIT
metadata:
  hermes:
    tags: [orchestrator, automation, personal-os, agents, scheduling, context]
---

# Personal AI Orchestrator

Build and operate a personal AI system that knows your context, automates
tasks, runs scheduled jobs, and coordinates agents — a 24/7 chief of staff.

## When to Use

- Building a personal "agentic OS" or copilot brain
- Automating recurring tasks (email, outreach, briefs, reports)
- Setting up scheduled jobs that run without you
- Ingesting context from past sessions, brain dumps, or external sources
- Coordinating multiple agents or sub-agents toward a personal goal
- Any "make AI work for me automatically" brief

## The Operating Model

### 1. Context Ingestion (know thyself)

The orchestrator is only as good as its context. Ingest proactively:

- **Brain dumps** — stream-of-consciousness captures, session transcripts
- **Project state** — AGENTS.md, STATE.md, BRIEF.md, active repos
- **Preferences** — corrections, style rules, "don't do X" patterns
- **External sources** — emails, calendars, job boards, LinkedIn
- **Past sessions** — session_search, Codex/ChatGPT exports, rollout summaries

Label every fact: **user statement / observed fact / inference / UNKNOWN**.
Attach dates to time-sensitive facts (OPT deadlines, credit expirations).

### 2. Outcome-First V1 → Critique → V2

The owner's collaboration mode: AI produces a complete best-current V1,
owner critiques, AI regenerates V2. Don't ask for permission to start —
produce the artifact, then iterate on feedback.

For automation: ship the smallest working version, observe it run, improve.

### 3. Orchestrator + Specialists

- **Orchestrator** — knows all context, decides what to do, routes to specialists
- **Specialists** — narrow agents for email, outreach, research, build, etc.
- **Shared state** — flat files (JSON/Markdown) that all agents read/write
- **Lease/verify** — atomic claims on tasks, verify before merge

### 4. Automation Patterns

| Pattern | Use | Tool |
|---|---|---|
| Scheduled job | Daily brief, weekly review, outreach sweep | cronjob |
| Triggered action | New email → triage, new job → apply | webhook/poll |
| Batch pipeline | 100 emails, 50 applications | delegate_task swarm |
| Watchdog | Monitor a URL, check CI, verify deploys | cronjob + script |
| Digest | Summarize a feed, a thread, a day | cronjob + LLM |

### 5. Human-in-the-Loop

- **Autonomous:** research, read, draft, build locally, organize context
- **Ask first:** external sends, applications, posts, purchases, credentials
- **Enumerate first:** when there are 100+ things to do, list them all with
  one-liners, let the user tick which to explore, then build only those
- **Receipts:** every automated action logs what it did, when, and the evidence

### 6. The "100 Tasks" Protocol

When the user has a large backlog of unfinished work:

1. **Enumerate** — list every task with a title + one-liner, grouped by type
   (bot / thread / sub-agent / scheduled-job / build / fix / outreach)
2. **Categorize** — P0/P1/P2, quick wins vs. deep work
3. **User ticks** — user reviews the list, marks which to explore
4. **Deep dive** — for each ticked item, research and propose a concrete plan
5. **Build** — create threads, scheduled jobs, sub-agents, or bots as appropriate
6. **Verify** — confirm each automation works before claiming done

## Standing Preferences

- **No em dashes** in any writing or outreach
- **"Fix only"** means correct objective errors, don't restructure or reinterpret
- **Preserve original wording** in brain dumps, then connect the dots
- **Free tools only** — no paid APIs or subscriptions
- **bun** over node for JS tooling
- **Ask before bulk/irreversible** operations
- **Scheduled jobs are critical** — job search, outreach, briefs should run
  automatically and deliver notes/guides without being asked

## Integration Points

| Service | Current State | What's Needed |
|---|---|---|
| Email (Hotmail) | ✅ Himalaya IMAP/SMTP | Works now |
| Email (Gmail) | ❌ Not connected | OAuth or App Password |
| Calendar | ❌ Not connected | Google Workspace auth |
| LinkedIn | ❌ Inactive | Manual posting or API |
| Job boards | ❌ Not automated | Scraping + tracking |
| Project mgmt | ❌ Not connected | Linear/Notion MCP |

## Reference Files

- [Codex Brain Dump Context](references/codex-context.md) — projects, preferences,
  frameworks extracted from Codex sessions
- [Email Setup](references/email-setup.md) — current Himalaya config, Gmail bridge
  requirements, sender-health gates
- [Automation Patterns](references/automation-patterns.md) — cron job recipes,
  watchdog scripts, batch pipeline templates
