# OpenCode Zen wiring for Headlong `bin/llm`

Verified 2026-08-25 against `~/.headlong/app/bin/llm` (the live copy the
dispatcher executes; the dev checkout `bin/llm` may differ — check inode/which).

## Endpoint facts
- Base URL: `https://opencode.ai/zen/v1/chat/completions` (OpenAI-compatible).
- Model: `x-preview-f-free` (free preview; no billing).
- Auth: **NONE.** Sending any `Authorization: Bearer` (even an OpenRouter key) → HTTP 401.
  The `opencode` provider case in `bin/llm` only appends an auth header if
  `OPENCODE_API_KEY` is set. Leave it unset.
- `reasoning_content` is returned alongside `content`; extract it as the thought text.

## One-command provider-resolution probe
```bash
bash -c 'model=x-preview-f-free; case "$model" in
  claude-*) echo anthropic;; gpt-*|o1*|o3*|o4*|chatgpt-*) echo openai;;
  gemini-*) echo gemini;; stealth/ox-alpha|ox-alpha|opencode/*|x-preview-*|*-free) echo opencode;;
  */*) echo openrouter;; *) echo die;; esac'
# expect: opencode
```

## Add the detection case (if missing)
In `detect_provider()` inside `bin/llm`:
```bash
        stealth/ox-alpha|ox-alpha|opencode/*|x-preview-*|*-free)   echo "opencode" ;;
```
Place it BEFORE the `*/*) echo "openrouter" ;;` fallback (which would otherwise
swallow `x-preview-f-free` as a vendor/model OpenRouter name and then die on the
missing key).

## Add the provider branch (if missing)
In the `case "$LLM_PROVIDER" in` auth/url block:
```bash
        opencode)
            url="${LLM_API_URL:-https://opencode.ai/zen/v1/chat/completions}"
            headers=(-H "Content-Type: application/json")
            [[ -n "${OPENCODE_API_KEY:-}" ]] && headers+=(-H "Authorization: Bearer ***")
            ;;
```
Reuse the OpenAI-compatible builders: `build_payload_opencode() { build_payload_openai; }`,
`extract_text_opencode() { extract_text_openai; }`, `stream_opencode() { stream_openai; }`,
`check_response_opencode() { check_response_openai; }`, `check_truncated_opencode() { check_truncated_openai; }`.

## The two files that set the model (BOTH must agree)
1. `~/.headlong/.env` → `SHELLM_MODEL=x-preview-f-free`  (and REMOVE `OPENROUTER_API_KEY`).
2. `~/.headlong/app/.identities/<name>/info.txt` → `think_model=x-preview-f-free`
   (read by `activate`, exported as `THINK_MODEL`; WINS over `.env`).

If only (1) is changed, the monolith keeps calling the old model — log shows
`Starting shellm loop (model: stealth/ox-alpha...)` unchanged.

## Verify after restart
```bash
systemctl --user reset-failed headlong-thinkers@<name>
systemctl --user start headlong-thinkers@<name>
sleep 12
tail -5 ~/.headlong/app/.identities/<name>/run/logs/monolith.log
# expect: Starting shellm loop (model: x-preview-f-free, ...)
```
If the log still shows the old model, the restart hit systemd's rate-limit and an
old process is still running — `reset-failed` then `start` ONCE.
