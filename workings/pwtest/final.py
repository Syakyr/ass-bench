import os, sys, pathlib
from playwright.sync_api import sync_playwright

URL = "file:///home/user/Codebase/ass-bench/figure.html"
OUT = "/tmp/final"
pathlib.Path(OUT).mkdir(parents=True, exist_ok=True)

with sync_playwright() as p:
    b = p.chromium.launch(
        executable_path="/home/user/.cache/ms-playwright/chromium-1244/chrome-linux64/chrome",
        args=["--no-sandbox", "--use-gl=angle", "--use-angle=swiftshader", "--enable-unsafe-swiftshader"],
        env={**os.environ, "LD_LIBRARY_PATH": "/home/linuxbrew/.linuxbrew/lib"})
    pg = b.new_page(viewport={"width": 400, "height": 400})
    reqs = []
    errs = []
    pg.on("request", lambda r: reqs.append(r.url))
    pg.on("console", lambda m: errs.append(f"[{m.type}] {m.text}") if m.type in ("error", "warning") else None)
    pg.on("pageerror", lambda e: errs.append(f"[pageerror] {e.message}"))
    pg.goto(URL, wait_until="load")
    pg.wait_for_timeout(9000)

    print("=== external requests ===")
    for u in sorted(set(reqs)):
        print("  ", u[:110])

    # poke the right buttock from behind, capture the oscillation
    pg.mouse.move(200, 200)
    pg.mouse.down(); pg.mouse.move(260, 200, steps=6); pg.mouse.up()   # drag = orbit, must NOT poke
    pg.wait_for_timeout(300)
    pg.screenshot(path=f"{OUT}/00-after-drag.png")

    pg.mouse.click(150, 210)
    for i in range(10):
        pg.wait_for_timeout(60)
        pg.screenshot(path=f"{OUT}/poke{i:02d}.png")

    # resize test
    pg.set_viewport_size({"width": 260, "height": 520})
    pg.wait_for_timeout(500)
    pg.screenshot(path=f"{OUT}/resize-tall.png")
    pg.set_viewport_size({"width": 640, "height": 300})
    pg.wait_for_timeout(500)
    pg.screenshot(path=f"{OUT}/resize-wide.png")
    pg.set_viewport_size({"width": 400, "height": 400})
    pg.wait_for_timeout(500)
    pg.screenshot(path=f"{OUT}/resize-square.png")

    print("=== console errors/warnings ===")
    print("\n".join(errs) if errs else "(none)")
    b.close()
