# Model and harness routing

This is an adapter note, not a requirement on the portable project state. Model names, access, prices, supported effort levels, and tool behavior change. Check the active model picker or provider documentation before setting a model. Keep the task contract, source hierarchy, approval boundary, and verifier the same when switching models.

## Choose for the work in front of you

| Work | Starting choice | Escalate when |
| --- | --- | --- |
| Focused edits, repeatable scans, and structured extraction | The available efficient model at an effort that passes the task's checks | A concrete failure shows that more reasoning is needed |
| Multi-file implementation, debugging, synthesis, and normal agent work | GPT-6 Sol in Codex, or the capable default in the active harness | Ambiguity, long tool chains, or failed verification make the stronger model useful |
| Hard open-ended reasoning, long-horizon recovery, and consequential tradeoffs | GPT-6 Astra in Codex, or Claude Fable in a Claude-capable harness when available | Compare against a cheaper route on representative tasks before making this the default |

The names above are examples, not a ranking across providers. Do not infer that a model is enabled from this file, a local config value, or an API model listing. Confirm the account and harness can actually run it. Do not use a Claude model ID as a Codex model setting unless that Codex installation explicitly supports it.

## Codex adapter

- GPT-6 Sol is a reasonable default for demanding day-to-day work. Increase reasoning effort for a specific hard task when the extra cost and latency are justified by its verifier.
- Use GPT-6 Astra for the hardest ambiguous or multi-step work when the Codex account exposes it. Keep the model selection explicit per task or in a named profile. A profile does not create a missing entitlement.
- Recheck supported effort values before changing a profile. Astra does not support `none` reasoning effort; use a supported level such as `high` or `max` when the task warrants it.
- Keep skill selection just in time. Loading every skill's full text, forcing every task into an orchestration loop, or raising every run to maximum effort makes simple work slower and can weaken instruction clarity.

## Claude-capable adapter

- Claude Fable is an Anthropic model. Route it through a harness and account that support it, using that harness's current model identifier and effort controls.
- Reuse this skill's portable contracts and reference files. Translate only tool, permission, and model configuration into the Claude adapter; do not copy Codex-only paths or config keys into canonical project files.
- Treat different harness tools, prompts, context policies, and approval flows as part of the comparison. A better outcome in one environment does not prove a model-only advantage.

## Compare routes before promoting a default

1. Choose two or three representative tasks with real inputs and acceptance criteria. Include one routine task and one difficult task.
2. Hold the task definition, source set, authority boundary, and verifier constant. Record the model, harness, effort, tool access, skill version, time, cost if available, and result.
3. Inspect the resulting artifact and run a check capable of failing. Record failures and repair attempts, not just final success.
4. Promote a route only when it improves the outcome or time/cost tradeoff without an authority or evidence regression. Recheck after material model or harness changes.

Sources for current model-family and effort behavior: [OpenAI model guidance](https://developers.openai.com/api/docs/guides/latest-model), [OpenAI models](https://developers.openai.com/api/docs/models), [Anthropic Claude Fable](https://www.anthropic.com/claude/fable). Access and behavior still need checking in the target account.
