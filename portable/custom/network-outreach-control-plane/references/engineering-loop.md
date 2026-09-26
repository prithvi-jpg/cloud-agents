# Engineering evaluation loop

Use this loop because no trusted `/loop` skill is installed.

For each milestone:

1. Define deterministic acceptance tests and human-experience checks.
2. Implement the smallest end-to-end vertical slice.
3. Run unit, integration, crash-recovery, and policy tests.
4. Review privacy, platform restrictions, credential scope, and irreversible actions.
5. Walk through the experience using keyboard and narrow-width layouts.
6. Measure correctness, latency, evidence coverage, and failure behavior.
7. Record defects and refine, up to three rounds.
8. Promote only when the weighted rubric is at least 90/100 and every critical gate passes.

Critical gates:

- no duplicate-send path
- no suppression bypass
- no sendable guessed email
- no unsupported message claim
- no bulk export uploaded to a third party
- no paid dependency
- verified Gmail Sent record for every successful send

If a gate fails after three rounds, stop and perform an architecture review instead of continuing to patch locally.
