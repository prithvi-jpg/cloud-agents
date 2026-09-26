# Browser adapters

## Common contract

Every adapter must preserve:

- unique session name;
- URL and build identity;
- viewport and input mode;
- initial snapshot;
- observable actions and outcomes;
- decisive screenshots or snapshots;
- console/runtime errors when available;
- stop/authority receipt.

Use a resettable synthetic fixture. Never paste secrets into prompts, commands, snapshots, or result files.

## Agent-browser

Prefer the target’s installed binary. If it is not on `PATH`, look for `node_modules/.bin/agent-browser` and use the target’s declared Node runtime.

Before the first run against a new installed version, read its bundled version-matched guide:

```bash
agent-browser skills get core --full
```

For open-ended exploratory testing, also inspect `agent-browser skills get dogfood --full` and retain its reproduce-first discipline. Use the direct binary rather than `npx` when both are available.

```bash
agent-browser --session <run-agent> --allowed-domains 127.0.0.1 open <url>
agent-browser --session <run-agent> wait --load networkidle
agent-browser --session <run-agent> snapshot -i
agent-browser --session <run-agent> screenshot <absolute-path>
```

After navigation or dynamic DOM changes, take a fresh snapshot before reusing element references. Use semantic locators when possible. Use one browser session per tester and close it at the end.

Use `--allowed-domains` for a fresh controllable local/staging context when compatible. It restricts navigation and page-initiated traffic, including WebRTC containment; it is not an operating-system firewall. Do not combine it with restored state or external profiles when the installed version rejects that combination.

Start a trace before a reproducible interactive issue and stop it into the tester’s trace directory:

```bash
agent-browser --session <run-agent> trace start
# reproduce the issue with before/action/after evidence
agent-browser --session <run-agent> trace stop <absolute-trace-path>
```

Use a HAR only when network behavior is material, and avoid embedding sensitive bodies. Batch independent setup or capture commands to reduce process overhead, but re-snapshot after every page-changing action.

For keyboard profiles, use `press Tab`, `press Shift+Tab`, `press Enter`, and `press Escape`; record the focused element after meaningful transitions.

Do not click a control whose consequence is unclear. In read-only mode, stop before submit, send, publish, delete, permission, billing, connector, or external-navigation actions.

## Controlled Chrome

Use when the user needs the visible browser or agent-browser cannot reach an authenticated local surface. Keep each tester in a separate tab or profile when possible. Record screenshots and the final URL. Do not reuse an authenticated production profile without explicit approval.

## Computer use

Use only for native applications, canvas-heavy surfaces, or browser states unavailable to DOM automation. Record what was visually observed and label coordinate-based action uncertainty. Computer use does not relax the authority boundary.

## Viewports

Default representative checks:

- desktop: `1440 × 1000`;
- narrow: `390 × 844`;
- user-specified device or assistive configuration when relevant.

Do not claim responsive or accessibility quality from one viewport or an automated scan alone.

## Session failure

If the browser cannot start, authentication is unavailable, the fixture is not resettable, or the page contains real sensitive data:

1. stop;
2. preserve the error;
3. mark the tester `blocked`;
4. state the missing capability or approval;
5. do not replace the run with invented observations.
