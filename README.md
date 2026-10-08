# Ass Bench

As seen from [the WAN show](https://www.youtube.com/live/gvzRPEW5eEc?si=v8MUWOQ9uv4oYr67&t=3202), we have the [LLM AssBench](https://assbench.com/).

Running [Halogen Flash Server](https://github.com/peonist-ai/halogen-flash-server) version 0.17.0 on the base model Qwen 3.8 Flash Next W4B using the [Pi harness](https://github.com/earendil-works/pi). [Metrics](./metrics.md) available exported from [llama-swap](https://github.com/mostlygeek/llama-swap).

Technically it's a fail since I had to do a 2nd prompt of "Looks like it's hanging for 29m. Set timeout next time", but it looks fascinating enough that I'll just leave it here in this repository. Initial prompt is used as-is as per [prompt.md](./prompt.md), from the website itself.

See it in its greatest glory at https://syakyr.github.io/ass-bench.

## Live

The page is a GitHub Page: **https://syakyr.github.io/ass-bench** (redirects to [`figure.html`](./figure.html), which is the same file that ships in this repo). Drag to orbit, click to poke. It needs network access on first load — Three.js `0.170.0` is pulled from jsDelivr via an import map — but nothing else: no images, fonts, textures or model files.

## What's in here

| File | What it is |
|---|---|
| [`figure.html`](./figure.html) | The deliverable. 36 KB, single file, no build step, opens from disk. |
| [`prompt.md`](./prompt.md) | The initial prompt, verbatim from assbench.com. |
| [`session.jsonl`](./session.jsonl) | The full agent session — every tool call, every screenshot it took, ~299 messages. Redacted (see below). |
| [`metrics.md`](./metrics.md) | llama-swap export for the run window: 238k prompt tokens at 1156 t/s, 202k generated at 52.5 t/s, 23.6M cached. |
| [`workings/`](./workings/README.md) | The Playwright harness, every render run's screenshots, and build logs. |

## How it was built

The figure is an implicit surface, not a scanned or modelled mesh: lofted super-ellipse cross-sections for trunk, gluteus maximus and thigh, combined with smooth min/max blends, then meshed with marching cubes. That is what makes it a genuinely continuous genus-0 "pair-of-pants" surface — the legs separate cleanly at the crotch instead of being boolean-joined blocks. The gluteal cleft is a subtractive elliptical groove whose placement is solved numerically against the actual blended back surface, so it stays seated from the small of the back to the perineum at every angle.

The swimwear is an offset shell clipped directly from the body surface with a hem wall at the cut. The first attempt used planar cuts, which produced long thin blades of floating fabric wherever the cut plane went near-tangent to the body; surface-clipping removes that failure mode entirely.

The poke is analytic in the vertex shader — displacement is a smooth falloff along the poke normal plus a lateral bulge, with the deformed normal taken from the displacement Jacobian — so each click is two damped spring scalars rather than a per-vertex simulation. Each click fires two modes (≈3.4 Hz local, ≈1.55 Hz whole-cheek). Skin is one consolidated noise pass per fragment feeding colour mottling, roughness and pore bump, plus a wrapped backlight subsurface term, AO baked into vertex colour, a procedural studio environment through PMREM and ACES tone mapping.

## Verified

- Only 3 external requests, all pinned `three@0.170.0` on jsDelivr.
- Zero console errors or warnings across load, poke, drag and resize.
- Screenshots at front, back, both sides, two 3-quarter angles, low and high, at 400×400 — all in [`workings/screenshots/`](./workings/screenshots/).
- Poke oscillation traced frame by frame; drag orbits and correctly does *not* poke.
- Resize checked at 260×520, 640×300 and 400×400; the figure stays framed and centred via a bounding-radius fit rather than a fixed camera distance. That re-fit was a real bug found in the last few minutes of the run.

## Caveats

FPS was measured at ~15 fps under SwiftShader (software rasterisation). Profiling showed shadows are not the cost — stripping sheen, clearcoat and the custom fragment shader made no measurable difference — it is SwiftShader's baseline overhead for `MeshPhysicalMaterial`. On real GPU hardware the target 60 fps is expected but was not measured here.

## Redaction

`session.jsonl` embeds the agent's injected global context, which contained the operator's home directory and an internal, non-public git hostname. Both were scrubbed before publishing (`/home/user`, `REDACTED-internal-*`). The log was scanned for `gh[pousr]_`, `sk-`, `AKIA`, `xox[baprs]-`, PEM private-key blocks, `apiKey`/`baseURL`/`Authorization` fields, emails and IP addresses; the only matches were the Chromium flag `--password-store=basic` and the word "tokens" in prose. No credentials were present.
