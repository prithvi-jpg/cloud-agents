# Result contract

Write one JSON object per tester:

```json
{
  "schema_version": "0.1",
  "run_id": "20260728-example",
  "agent_id": "agent-01",
  "profile_id": "first-visit-navigator",
  "status": "completed",
  "started_at": "ISO-8601",
  "completed_at": "ISO-8601",
  "browser": {
    "adapter": "agent-browser",
    "session": "run-agent-01",
    "viewport": "1440x1000",
    "start_url": "http://127.0.0.1:3000",
    "final_url": "http://127.0.0.1:3000/#route"
  },
  "task_outcome": {
    "state": "completed | partial | blocked | failed",
    "summary": "observable outcome",
    "actions_used": 7,
    "time_seconds": 84
  },
  "path": [
    {
      "step": 1,
      "action": "opened the page",
      "observation": "visible result",
      "evidence_refs": ["trace:initial-snapshot"]
    }
  ],
  "findings": [
    {
      "id": "agent-01-f1",
      "claim_type": "observed",
      "severity": "high",
      "category": "orientation",
      "title": "short finding",
      "observation": "what the trace shows",
      "impact": "task consequence",
      "evidence_refs": ["screenshot:agent-01/initial.png"],
      "confidence": "high",
      "human_required": false,
      "suggested_contract": "replayable expectation or null"
    }
  ],
  "positive_signals": ["specific behavior that helped"],
  "open_questions": ["question that the run cannot answer"],
  "authority_receipt": {
    "mode": "read-only",
    "external_writes": 0,
    "target_writes": 0,
    "stopped_before": ["submit"],
    "notes": "none"
  }
}
```

Allowed values:

- `status`: `completed`, `blocked`, `failed`;
- task state: `completed`, `partial`, `blocked`, `failed`;
- claim type: `observed`, `interpreted`, `specified`, `simulated`, `unknown`;
- severity: `blocker`, `high`, `medium`, `low`, `note`;
- confidence: `high`, `medium`, `low`.

Rules:

- `observed` and `specified` findings require at least one evidence reference.
- `simulated` is a declared test-path result, not human evidence.
- `unknown` should normally set `human_required` to `true`.
- A read-only run must report zero target and external writes.
- Do not store hidden chain-of-thought. Store actions, observations, concise rationales, and evidence.
