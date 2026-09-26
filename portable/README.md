# Portable Codex skills snapshot

This package is a pinned snapshot of skills found on Prithvi's Windows and WSL installations on 2026-09-26. It contains 189 distinct skill names: 168 fetched from 18 GitHub repositories at the commits in `manifest.json`, and 21 bundled under `custom/` because they lack a mapped GitHub skill path. The manifest also records 31 remote plugin IDs for separate, managed installation. It does not install plugins or configure model access.

The package includes personal skill content, published at the owner's request. Review `custom/` and your work laptop's policy before installing it. Third-party GitHub skills also deserve review before use. Five bundled Orca-related skills were found inside a local `orchestration` skill folder; their usefulness depends on having a compatible Orca runtime.

## Install the adaptive skill from its public repo

For just the adaptive operating skill, share [cloud-agents](https://github.com/prithvi-jpg/cloud-agents) with Codex on the work laptop and ask:

> Use `$skill-installer` to install `https://github.com/prithvi-jpg/cloud-agents/tree/main/skill/adaptive-agent-operating-system`. Inspect the skill first, show me the destination and changes before applying them, and preserve any existing copy. Check that Codex can use it on the next turn; restart only if it does not appear. Use only the model options actually available in this workspace.

The public repository contains the adaptive skill and this full portable snapshot. A link by itself gives Codex a source to inspect; the explicit install request makes the adaptive skill available in future tasks. The built-in `$skill-installer` currently defaults to `$CODEX_HOME/skills` (usually `~/.codex/skills`) and aborts if that skill directory already exists. The ZIP installer below uses the explicit target you provide, such as `~/.agents/skills`.

## Install this full snapshot on another laptop

1. Download the ZIP from the repository and unzip it. Read `manifest.json` and review `custom/`.
2. Open a terminal in that directory. `git` and Python 3.10+ must be available, and GitHub access must work.
3. Preview the exact skill names that would be created or replaced:

   **PowerShell**

   ```powershell
   py -3 .\install.py --target "$HOME\.agents\skills"
   ```

   **WSL, macOS, or Linux**

   ```sh
   python3 ./install.py --target "$HOME/.agents/skills"
   ```

4. When the preview is acceptable, repeat the command with `--install`. The installer stages and validates all selected content first. It then backs up existing skill directories before replacing them and prints a rollback receipt path. Restart Codex to refresh its skill list.

Use `--scope windows_agents`, `--scope wsl_agents`, or `--scope codex` to reproduce only one original location. Use `--only adaptive-agent-operating-system` for a single skill. The default selects all 189 distinct names. The installer uses the explicit `--target` only; it does not touch global settings, plugin caches, model profiles, or credentials.

To undo an installation, run `py -3 .\install.py --rollback "<path printed by the installer>"` on Windows, or `python3 ./install.py --rollback '<path>'` elsewhere. The rollback archives the updated copies and restores the prior directories. Keep the receipt and backup directory until you have checked the result.

To see whether the pinned GitHub repositories have newer default-branch heads, run `py -3 .\install.py --check-updates` (or `python3 ./install.py --check-updates`). This is read-only; updating the pins requires a new reviewed package. A changed GitHub head does not necessarily mean the particular skill changed.

## Other harnesses and plugins

Codex discovers personal skills in `~/.agents/skills`. Claude Code uses `~/.claude/skills`; install to that explicit `skills` directory if desired. Codex reads applicable `AGENTS.md`; this repository's `CLAUDE.md` imports it for Claude Code. Neither file grants access to a model. Select Astra, Sol, or Fable only if the relevant product makes it available.

The 31 remote plugins are listed in `manifest.json` for inventory. Install or authorize them through the Codex plugin manager on the work laptop; copying local plugin cache directories will not reproduce managed installation or connector permissions.
