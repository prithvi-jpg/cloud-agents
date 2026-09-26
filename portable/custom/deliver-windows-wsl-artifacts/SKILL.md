---
name: deliver-windows-wsl-artifacts
description: Preflight and verify builds and local artifact delivery across Windows, WSL, and Codex. Use before any build, render, browser preview, or handoff when paths include /home, /mnt/c, C:\, or \\wsl.localhost; when using Node/npm/npx from WSL; when showing local images, video, HTML, PDFs, or inline visualizations; or when errors mention Windows npm inside WSL, UNC paths, ENOENT, sandboxCwd, missing images, broken playback, native-module platform mismatch, or content that exists on disk but does not render in Codex.
---

# Deliver Windows/WSL Artifacts

Prevent mixed-runtime builds and broken local-media handoffs. Treat disk existence, browser rendering, Codex inline delivery, and master-quality playback as separate proofs.

## Mandatory order

Perform this workflow before building or presenting an artifact:

1. Establish the authoritative execution environment.
2. Run the deterministic preflight.
3. Build with binaries native to that environment.
4. Package media for the destination surface.
5. Mirror thread-scoped inline artifacts when Windows and WSL are both involved.
6. Verify the actual rendered surface and interactions.
7. Hand off exact Linux and Windows paths plus verification evidence.

Do not begin with the build and repair path problems afterward.

## 1. Select one execution environment

- Treat `/home/...` and `\\wsl.localhost\<distro>\home\...` repositories as WSL-owned. Run Linux `node`, `npm`, `npx`, `bun`, Python, browser tooling, and native dependencies.
- Treat `C:\...` repositories as Windows-owned. Run Windows tooling from a Windows-local drive, not from a WSL UNC working directory.
- Treat `/mnt/c/...` as Windows-backed storage accessed from WSL. If the active shell is WSL, still use Linux executables. Keep one platform's `node_modules`; never alternate Windows and Linux package managers over the same install.
- Reject an executable in WSL when its resolved path starts with `/mnt/<drive>/`, contains a Windows path, or ends in `.exe`, `.cmd`, `.bat`, or `.ps1`.
- If native dependencies were installed by the wrong platform, use a clean environment or request approval before removing or rebuilding dependency state. Do not silently delete user files.

## 2. Run preflight first

Use the bundled script before a JavaScript build:

```bash
python3 <skill-dir>/scripts/preflight.py \
  --workspace "$PWD" \
  --require-linux-runtime node \
  --require-linux-runtime npm \
  --require-linux-runtime npx
```

Use the absolute Linux executable paths reported by the script. Do not continue after a runtime-coherence error.
Replace or extend the `--require-linux-runtime` arguments when the project uses Bun, FFmpeg, Python, or another inspected runtime.

For an inline artifact and its WSL mirror:

```bash
python3 <skill-dir>/scripts/preflight.py \
  --workspace "$PWD" \
  --artifact <windows-backed-fragment.html> \
  --mirror <wsl-thread-mirror.html> \
  --inline
```

For video verification, add `--media <file.mp4> --decode-media`. Add `--json` when producing a receipt.

## 3. Package for the actual surface

### Codex inline images and video

- Create a self-contained HTML fragment under 2 MB.
- Embed preview media with `data:image/...;base64,...` or `data:video/mp4;base64,...`.
- Use native `<img>` or `<video controls playsinline>` elements.
- Do not depend on `file://`, `/home/...`, `/mnt/c/...`, `C:\...`, UNC, or relative local asset URLs inside the fragment.
- Keep a full-resolution master separately. An embedded proxy proves only inline playback, not master quality.

### Standalone HTML and browser players

- Keep relative asset links only when the HTML and assets ship together.
- Serve from a common ancestor directory high enough for every relative link to resolve.
- Verify every asset request returns HTTP 200.
- For a video master, verify the browser's `currentSrc`, intrinsic dimensions, duration, readiness, and advancing playback.

### Markdown and final responses

- Use clickable absolute Linux file links for Codex.
- Also print the exact Windows path. For WSL-owned files, use `\\wsl.localhost\<distro>\...`.
- Never claim a Markdown path alone is an inline preview.

## 4. Mirror Codex visualizations

When the thread exposes both Windows-backed and WSL visualization roots:

1. Write the canonical fragment to the current thread's Windows-backed visualization directory.
2. Copy the same bytes to the corresponding `/home/<user>/.codex/visualizations/...` thread directory.
3. Compare SHA-256 hashes.
4. Render and inspect the directive-resolved basename.

Derive the current date and thread ID from the active environment context. Never reuse an older thread's visualization directory.

## 5. Verify before handoff

Require evidence appropriate to the artifact:

- **Image:** source loaded, nonzero `naturalWidth` and `naturalHeight`, no broken placeholder.
- **Inline video:** embedded source selected, metadata ready, expected dimensions and duration, playback time advances, controls usable.
- **Master video:** full decode passes; browser loads the master itself; `currentSrc`, decoded dimensions, file size, and duration match.
- **HTML:** no console or page errors; primary controls work; all local links resolve.
- **Responsive surface:** no horizontal overflow at approximately 736 px and 320–390 px.
- **Mixed path:** both visualization copies exist and hashes match.

Use browser automation for rendering proof. The bundled script validates files, runtimes, hashes, HTML dependencies, and media decoding; it does not substitute for browser inspection.

## 6. Handoff contract

State all of the following in the final response:

- What is shown inline and whether it is a proxy.
- Clickable full-quality artifact and browser-player links.
- Exact Linux path and exact Windows/UNC path.
- Resolution, duration or dimensions, size, and relevant hash/receipt.
- What was actually verified and any remaining physical-device or host limitation.

Do not claim completion when content only exists on disk.
