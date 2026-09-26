---
name: hci-agent-test-lab
description: Run a local, evidence-bounded multi-agent UX and human-AI interaction rehearsal against a website or browser application. Use when Codex should test a local or staging product from several task-relevant perspectives, operate the app with agent-browser, Chrome, or computer use, preserve screenshots and traces, render a SimFrancisco-style living test room, compare disagreements, and produce a reviewable findings handoff for the product-building agent. Default to read-only and synthetic fixtures; do not use this skill to claim simulated feelings are user research, replace human participants, test production with consequential actions, or stereotype behavior from demographic labels.
---

# HCI Agent Test Lab

Run one inspectable loop:

`mission → bounded cohort → isolated browser traces → evidence-typed findings → living test room → human-reviewed fix brief`

The small characters are an observer interface for agent state, disagreement, and replay. They are not evidence that the agents represent a population.

## 1. Establish the test contract

Read the target workspace’s nearest `AGENTS.md`, project contract, and current state. Define:

- one user job and one critical flow;
- local or staging URL;
- source/build identifier;
- allowed accounts and data;
- read-only or isolated-sandbox authority;
- forbidden effects;
- success, failure, and “needs humans” outcomes.

Default to `read-only`. Never submit a consequential form, send a message, purchase, publish, delete, change permissions, use production credentials, or mutate real user data. Use a resettable synthetic fixture for any write path.

Initialize a run:

```bash
python3 scripts/init_run.py \
  --run-root <absolute-run-root> \
  --target-name "<product>" \
  --workspace <absolute-workspace> \
  --url <local-or-staging-url> \
  --mission "<one observable user job>" \
  --profiles first-visit-navigator,evidence-skeptic,keyboard-pathfinder \
  --mode read-only
```

Inspect the emitted `manifest.json` and profiles before browsing. Read [cohort-design.md](references/cohort-design.md) when selecting or authoring profiles.

## 2. Prepare the real application safely

Prefer an already-running local server. Otherwise use an isolated fixture, copied database, disposable account, or target-provided demo mode. Do not weaken the target’s safety controls to make testing easier.

Read [browser-adapters.md](references/browser-adapters.md) before choosing the browser capability. Prefer:

1. `agent-browser` for reproducible DOM/accessibility snapshots and screenshots;
2. controlled Chrome when the user wants the visible browser;
3. computer use only when the surface cannot be reached otherwise.

Record the adapter, browser/session name, viewport, start-state receipt, and any untested state.

## 3. Run the cohort

Use three profiles by default. Add a fourth only when it covers a distinct risk. Do not create ceremonial agents.

When collaboration/subagent tools are available, spawn one tester per profile, up to the host concurrency limit. Give each tester only:

- `manifest.json`;
- its own profile JSON;
- [agent-packet.md](references/agent-packet.md);
- the browser adapter reference;
- its unique session name and result path.

Do not give testers other agents’ findings. Do not let them communicate during the isolated exploration. If the product’s job is inherently collaborative, create a separate, explicitly declared shared-sandbox experiment after the isolated baseline.

Each tester must:

1. open the declared URL in its own browser session;
2. capture the initial interactive snapshot;
3. attempt only the assigned mission within its time/action budget;
4. capture decisive before/after screenshots or snapshots;
5. distinguish observation from interpretation and simulation;
6. stop at the authority boundary;
7. write one result JSON matching [result-contract.md](references/result-contract.md);
8. close its browser session.

If subagents are unavailable, run profiles sequentially with separate browser sessions and context packets.

## 4. Aggregate before interpreting

After results exist:

```bash
python3 scripts/aggregate_run.py --run-dir <absolute-run-directory>
python3 scripts/render_test_room.py --run-dir <absolute-run-directory>
python3 scripts/validate_run.py \
  --run-dir <absolute-run-directory> \
  --require-complete \
  --require-aggregate
```

The generated artifacts are:

- `aggregate.json` — machine-readable combined result;
- `FINDINGS.md` — prioritized evidence and disagreement report;
- `HANDOFF.md` — bounded fix packet for the product agent;
- `test-room.html` — small-character observer surface;
- `manifest.json` — run state and authority receipt.

Serve the observer surface when live character state is useful:

```bash
python3 scripts/serve_test_room.py \
  --run-dir <absolute-run-directory> \
  --host 127.0.0.1 \
  --port <free-local-port>
```

The page polls the read-only `/api/state` endpoint and moves agents from waiting to completed, blocked, or failed as result files appear. The standalone HTML also works without the server.

Inspect the observer surface with a real browser. Verify character selection, issue selection, keyboard operation, narrow layout, and console errors. The visual state never upgrades a simulated claim into human evidence.

## 5. Apply the claim boundary

Use exactly these claim types:

- `observed`: visible UI, DOM, accessibility tree, state, console, network, or deterministic output;
- `interpreted`: a reviewer’s explanation of an observation;
- `specified`: a project requirement, policy, or accessibility rule;
- `simulated`: a path or reaction produced under one declared profile;
- `unknown`: evidence is insufficient or real people are required.

An `observed` finding needs an evidence reference. A simulated statement cannot claim adoption, prevalence, emotion, trust, delight, accessibility lived experience, or market demand.

Human review owns:

- whether a finding is a real product problem;
- severity for subjective issues;
- changes to research interpretation;
- accessibility-conformance claims;
- release or implementation decisions;
- any handoff to another Codex task.

Do not edit the target application automatically. Present `HANDOFF.md` first. Send it to another task or implement fixes only when the user explicitly requests that next action.

## 6. Close with a run receipt

Report:

- target and mission;
- cohort and why each profile existed;
- completed, blocked, and failed runs;
- strongest convergent finding;
- important disagreement;
- deterministic failures;
- unknowns needing people;
- artifact paths;
- authority receipt;
- exactly one next experiment.

Run `python3 scripts/self_test.py` after changing this skill. Run the skill validator when its Python dependencies are available; if not, independently check frontmatter, metadata, scripts, and schemas and state the limitation.
