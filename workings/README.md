# Workings

Everything the model produced on the way to [`figure.html`](../figure.html), kept so the iteration loop is auditable. Nothing here is needed to run the deliverable.

## Layout

| Path | What it is |
|---|---|
| `pwtest/` | The Playwright harness scripts used to render and inspect the figure at 400×400. |
| `screenshots/` | One directory per render run — the visual review loop, in chronological order (`shots2` → `s4` → … → `s22`, plus the poke traces). |
| `logs/` | Build-timing output from the first three instrumented runs (marching-cubes field/mesh times, vertex and triangle counts, camera fit). |

## The harness

All scripts drive the system Chromium from `~/.cache/ms-playwright/chromium-1244` with SwiftShader (`--use-gl=angle --use-angle=swiftshader`), because the figure has no GPU here. They were written against a throwaway venv at `/tmp/pwtest` (`uv venv && uv pip install playwright`), so the hardcoded paths are historical — repoint `URL` / `executable_path` at wherever the repo lives to re-run them.

| Script | Purpose |
|---|---|
| `shot.py` / `shot.mjs` | Core capture: sets the camera to eight fixed angles (front, back, left, right, two 3-quarter, low, high) via the `window.__ctl` OrbitControls handle, screenshots each at 400×400, and dumps console output. `shot.sh` is the shell wrapper that passes the target URL and output dir. |
| `poke.py` | Fires clicks at the model and captures the resulting deformation frames. |
| `pokevis.py` | Poke trace at rest: one screenshot before the click, then nine at 70 ms intervals, to see the damped spring oscillate. |
| `perf.py` | FPS measured over 1.5 s of `requestAnimationFrame`, with shadow maps and the swimwear toggled off in turn to attribute cost. |
| `perf2.py` | Same measurement, stripping `sheen` / `clearcoat` and the custom fragment shader, to test whether the skin shader was the bottleneck. It was not — see the FPS note below. |
| `final.py` | Acceptance pass: lists every external network request, collects console errors/warnings/pageerrors, and captures the final multi-angle set. |

## Debug flags that no longer exist

Several runs used query-string flags on `figure.html` to isolate parts of the model — `?onlybody=1`, `?onlyfab=1`, `?nocleft=1`, `?dbg=1`, and `&nx=72&ny=96&nz=64` for marching-cubes resolution. These were **removed from the final file**, so re-running the older scripts against the shipped `figure.html` will not reproduce those variants. The screenshots are the record of them.

## What the runs show

The loop is visible in the sequence: early runs (`shots2`–`s7`) are geometry and mesh-resolution checks with the debug flags on; `s8`–`s17` are the anatomy iterations — leg separation at the crotch, cleft placement, the swimwear cut failing into floating blades of fabric and then being re-derived by surface-clipping the offset shell instead of planar-cutting it; `s18`–`s22` are skin, lighting and framing polish. `pv/`, `pk1/` and `pk2/` are the poke traces, `final/` is the acceptance set (including the 260×520 and 640×300 resize checks that caught the camera not re-fitting on resize).

## Redaction

`session.jsonl` was scrubbed before publishing: the operator's home directory and an internal (non-GitHub) git hostname that were present in the agent's injected global context were replaced with `/home/user` and `REDACTED-internal-*`. No credentials were found in the log — it was scanned for `gh[pousr]_`, `sk-`, `AKIA`, `xox[baprs]-`, PEM private-key blocks, `apiKey`/`baseURL`/`Authorization` fields, emails and IPs; the only hits were the Chromium flag `--password-store=basic` and the word "tokens" in prose. The redactor script itself is not committed; it lives in the repo's gitignored `./scratch/`.
