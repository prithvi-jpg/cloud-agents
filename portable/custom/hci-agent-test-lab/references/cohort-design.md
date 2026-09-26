# Cohort design

## Purpose

Create a small set of task-relevant behavioral envelopes that expose different interaction risks. A profile is a test configuration, not a synthetic human or market segment.

## Default profiles

| ID | Distinct lens | Useful for |
|---|---|---|
| `first-visit-navigator` | No product history; must infer the conceptual model from the surface | Orientation, labels, information scent, first useful action |
| `timeboxed-operator` | Ninety-second attention budget; wants one safe next action | Hierarchy, prioritization, excessive reading, interruption cost |
| `evidence-skeptic` | Checks provenance, freshness, uncertainty, and fact/interpretation boundaries | AI recommendations, research claims, trust, auditability |
| `keyboard-pathfinder` | Keyboard-only input configuration; follows focus and semantic structure | Focus order, names, dialogs, reachable actions, escape/recovery |
| `recovery-explorer` | Intentionally takes one wrong turn and tries to repair it | Undo, error states, cancellation, backtracking, state preservation |

## Selection rules

1. Start from the mission’s causal risks.
2. Select three profiles whose likely failure modes differ.
3. Add evidence or product requirements to each profile.
4. Specify time and action budgets.
5. Specify the stop condition.
6. Remove biography that cannot change the task.

Do not derive behavior from race, gender, disability label, age, income, occupation, personality type, or family status. If accessibility matters, configure the actual input mode, viewport, zoom, screen reader, contrast, motion, or cognitive load and retain a human-testing boundary.

## Custom profile fields

```json
{
  "id": "stable-kebab-case",
  "name": "short visible name",
  "lens": "one distinct interaction risk",
  "starting_knowledge": ["facts available at the start"],
  "behavioral_constraints": ["observable test behavior"],
  "mission_questions": ["questions this profile may answer"],
  "time_budget_seconds": 180,
  "max_actions": 20,
  "stop_conditions": ["authority or evidence boundary"],
  "claim_boundary": "what this profile cannot establish",
  "character": {
    "color": "#hex",
    "accent": "#hex",
    "station": "orientation | flow | evidence | recovery"
  }
}
```

## Same cohort across releases

Reuse the versioned profile and mission contract, not an invented persistent identity. A later build comparison is valid only when the start state, data, browser configuration, task, evaluator, and contract are comparable.
