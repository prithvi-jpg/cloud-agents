# Pinned source repositories

The manifest maps each skill name to an exact repository path and Git tree ID. The installer fetches these commits; their skill files are not copied into this repository.

| Repository | Skills | Pinned commit |
| --- | ---: | --- |
| [EveryInc/compound-engineering-plugin](https://github.com/EveryInc/compound-engineering-plugin) | 12 | `a763b392c3c05faa1a383c0d228b7e95200ecc90` |
| [GoogleChrome/modern-web-guidance](https://github.com/GoogleChrome/modern-web-guidance) | 2 | `22ab18dfb50a5d7e3bdcf471c14076a5534eae4e` |
| [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) | 1 | `19392f7a08264ed00486a251f5b2098321771f94` |
| [cli/cli](https://github.com/cli/cli) | 1 | `9b031151a825bda919203c5202876a725d637368` |
| [cursor/plugins](https://github.com/cursor/plugins) | 67 | `ecc249f1e306fc64ddf83c7bed16cacf7c2239db` |
| [emilkowalski/skills](https://github.com/emilkowalski/skills) | 6 | `d16ebe60d09a5ba2afcb7054ede9d0a10c9f6128` |
| [firecrawl/skills](https://github.com/firecrawl/skills) | 28 | `3a410054eb2a4bbb1545d0fd88d4cb282f64624f` |
| [google/agents-cli](https://github.com/google/agents-cli) | 7 | `e556c95e94d8440e2edf605a13c513bd01d8e602` |
| [heredotnow/skill](https://github.com/heredotnow/skill) | 1 | `0f60d2374d3c8c6ffda1ecad4c0af69f278f7f27` |
| [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes) | 12 | `dce0acd6d2ea26cae80338bdc7bb2f1cce745d27` |
| [jamiemill/layers-skills](https://github.com/jamiemill/layers-skills) | 9 | `a201dc8c2011940b9d93934abb0f40c3b226c7ca` |
| [mvanhorn/last30days-skill](https://github.com/mvanhorn/last30days-skill) | 1 | `084662b501fb0dba95bd55eff0c258d35e0dc499` |
| [prithvi-jpg/cloud-agents](https://github.com/prithvi-jpg/cloud-agents) | 1 | `4f52bcb9e772f9baf90af66c2622d3d2d72d4193` |
| [remotion-dev/skills](https://github.com/remotion-dev/skills) | 6 | `cf49eff5d4463b33966b6618c83f7295797dd028` |
| [stablyai/orca](https://github.com/stablyai/orca) | 3 | `abc4cb0f324538650b34cf47d259cb5665f0ad54` |
| [tmchow/illo-skill](https://github.com/tmchow/illo-skill) | 1 | `0b0abee9214d9cef3c9f42d5c739a0d63cb618e6` |
| [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) | 9 | `063bee94c3f4df8453406c830b0a7df0f2860278` |
| [vercel-labs/skills](https://github.com/vercel-labs/skills) | 1 | `7407f3893ad4dceab546ac002c3ef806e4000c73` |

## Bundled local skills

21 skills are bundled under `custom/` and in the ZIP at the owner's request because they lack a mapped GitHub skill path. `context-dev` came from [its well-known skill source](https://docs.context.dev/.well-known/agent-skills/context-dev/skill.md) and declares MIT in its `SKILL.md`. Five Orca-related skills came from the local `orchestration` directory and depend on a compatible Orca runtime.

Managed Codex plugins are listed only as identifiers and installed versions in `manifest.json`; plugin files and credentials are not copied.
