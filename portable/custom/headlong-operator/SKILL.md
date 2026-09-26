---
name: headlong-operator
description: Operate Headlong; free LLM endpoint, systemd bridge.
version: 1.0.0
author: hermes-agent
license: mit
metadata:
  hermes:
    tags: [orchestration, headlong, shellm, personal-operator, systemd, llm-wiring]
    related_skills: [adaptive-agent-operating-system, personal-ai-orchestrator, build-operating-system]
---

# headlong-operator

Headlong is the agent framework (identities, thinkers, mind log, bridges, dash).
**shellm** is just one tool inside it (the bash Recursive-Language-Model loop).
This skill is about *running and keeping alive* a personal operator identity and
making it think on a chosen (usually free) model, then harvesting its work orders.

## When to load
- User has a Headlong identity and wants it to "keep thinking / work on my goals / be my operator".
- Its LLM calls fail: `Cannot detect provider for model 'X'`, `OPENROUTER_API_KEY is not set`, `Provider returned error, last tried openrouter`.
- You need to talk to it, supervise it across reboots, or wire a Hermes↔identity bridge.

## Mental model
The mind is a loop: a **dispatcher** spawns **thinkers** (monolith + responder).
Each think cycle calls `shellm`, which calls `bin/llm`, which resolves
`$SHELLM_MODEL` → a **provider** → a **base URL + auth**. The trajectory
(`trajectory.jsonl`) is the source of truth; the dash renders it.

## 1. Install / where things live (already-installed case)
- State home: `~/.headlong` (env: `HEADLONG_HOME`/`SHELLM_HOME`).
- Checkout (app dir): `~/.headlong/app` — pointer file `~/.headlong/app_dir`.
  `persona` prepends `$APP_DIR/bin:$APP_DIR/tools` to PATH, so the `llm`/`shellm`
  actually executed live in `$APP_DIR/bin`, NOT necessarily the dev `bin/` you may
  be editing. **Always verify which `bin/llm` the live process uses before patching.**
- Identity: `~/.headlong/app/.identities/<name>/` → `info.txt`, `activate`,
  `memories/`, `trajectories/<root>/trajectory.jsonl`, `run/dispatcher.pid`.
- Talk: `<name> say "..."` (or `persona <name> say "..."` if the name collides with
  another command — `cortona` collides with a Hermes shim, use `persona cortona`).
- Status: `persona <name> status`; pause: `persona <name> stop`; resume: `persona <name> start`.

## 2. LLM provider wiring — THE sharp edges (this is where sessions stall)
`bin/llm` only knows 4 built-in providers plus `opencode`. Model→provider is
detected by name pattern in `detect_provider()`:
- `claude-*`→anthropic, `gpt-*`/`o1-4*`/`chatgpt-*`→openai, `gemini-*`→gemini,
  `stealth/ox-alpha|ox-alpha|opencode/*|x-preview-*|*-free`→**opencode**,
  any other `vendor/model` (`*/*`)→**openrouter**, else die.

**Free OpenAI-compatible endpoint with NO auth (e.g. OpenCode Zen `x-preview-f-free`):**
- Set `SHELLM_MODEL=x-preview-f-free` in `~/.headlong/.env` (state home).
- The `opencode` provider case uses `url=${LLM_API_URL:-https://opencode.ai/zen/v1/chat/completions}`
  and sends **NO Authorization header** unless `OPENCODE_API_KEY` is set. Sending a
  foreign/OpenRouter key makes it 401. So: REMOVE `OPENROUTER_API_KEY` from the
  state-home `.env`; do NOT set `OPENCODE_API_KEY`.
- If `bin/llm` lacks the `x-preview-*` detection case, add it (see references/).

**Model-pin precedence (root cause of repeated "still calling old model" failures):**
The live model is NOT just `SHELLM_MODEL` in `.env`. Resolution order for the monolith:
1. `info.txt` line `think_model=` (read by `activate`, exported as `THINK_MODEL`) — **highest precedence**.
2. `THINK_MODEL` shell var → `$SHELLM_MODEL` (state-home `.env`) → `claude-opus-4-7` default.
So if you change `.env` but `info.txt` still says `think_model=stealth/ox-alpha`, the
monolith keeps calling the dead model and you see `calling stealth/ox-alpha...` in
`run/logs/monolith.log` forever. **Fix the pin in `info.txt` too.**

**Verify the fix landed:** after restarting, `tail` the monolith log and confirm the
model name in `Starting shellm loop (model: ...)`.

## 3. systemd supervision (so it survives reboots / WSL close)
- WSL has real systemd (PID 1) and user units need no sudo.
- Unit files: `~/.config/systemd/user/headlong-thinkers@.service` + `headlong-web.service`.
  For a template unit, the instance spec MUST use a bare `%i` (NOT `%%i` — that
  renders literally and breaks the unit).
- Enable + start: `systemctl --user enable --now headlong-thinkers@<name> headlong-web`.
- **systemd rate-limits `restart`** (default ~5 starts in 10s → "attempted too often",
  unit goes into failed). If you see that, do `systemctl --user reset-failed
  headlong-thinkers@<name>` then `start` ONCE. Rapid restart loops also strand an
  old failing process whose log keeps showing the pre-fix error — reset-failed +
  single start clears it.
- The dispatcher drains in-flight work on stop (up to `restart_drain_timeout`, ~180s);
  a `stop` followed quickly by `start` can thus appear to hang — wait it out.

## 4. Pace it (idle backoff is a feature, not a bug)
Headlong dwells between spontaneous cycles (60s after routine thoughts, up to a 300s
cap) to save cost. Messages wake it instantly. To make it grind goals continuously,
set in `<identity>/.env`: `MONOLITH_THOUGHT_CAP=10 MONOLITH_BACKOFF_BASE=10
MONOLITH_BACKOFF_FACTOR=2 MONOLITH_BACKOFF_CAP=30`.

## 5. Hermes↔identity bridge (the think/delegate loop)
- Native chat: `export IDENTITY_NAME=<name> TRAJ_DIR=.../<traj> ROOT_TRAJ_ID=<id>
  TRAJ_ID=<id> CHATRC=<id>/chat/.chatrc; bin/chat send --to <name> --from prithvi "..."`.
  (`chat send` dies without a sender — it comes from the identity chatrc, not cwd.)
- Pattern that works: cortona (the identity) does recon/verification/direction;
  Hermes executes the patches with proper tooling (its generated bash keeps fumbling
  quoting). Hermes reports "Work Order vN executed, receipts: ..." back via `chat send`,
  cortona lifts its own holds and queues next cycles.
- A recurring cron heartbeat (every 30m) that reads `trajectory.jsonl`, sends context
  via `chat send`, restarts the unit if dead, and relays blockers back is the durable
  form of this bridge.

## 6. Reading the mind (verification)
- Trajectory: `python3 -c "import json;[print(json.loads(l).get('type'),'::',str(json.loads(l).get('content'))[:160]) for l in open('trajectories/<root>/trajectory.jsonl').read().splitlines()]"`.
- Health: `cat <identity>/.shellm/run/llm_health.json` (ok/err + provider).
- Dash: http://localhost:8080 (binds localhost; for Windows browser use localhost,
  WSL forwards it; or flip service to 0.0.0.0 and use the WSL IP).

## Pitfalls (learned the hard way)
- Editing the dev `bin/llm` but the live process uses `$APP_DIR/bin/llm` (installed copy) → fix never lands. Verify inode/path.
- Changing `.env` but not `info.txt` `think_model=` → old model keeps running.
- Leaving a foreign API key in `.env` for a no-auth endpoint → HTTP 401.
- `persona <name>` vs bare `<name>`: if the name clashes with another command, bare
  invocation silently runs the wrong binary (e.g. `cortona` → Hermes shim). Always use
  `persona cortona` for control commands.
- systemd `restart` spam → rate-limit lockout. reset-failed + single start.

See `references/opencode-zen-wiring.md` for the exact `bin/llm` patch recipe and the
one-command provider-resolution probe.
