import os, sys, pathlib
from playwright.sync_api import sync_playwright

URL = "file:///home/user/Codebase/ass-bench/figure.html?t=1"
OUT = sys.argv[1] if len(sys.argv) > 1 else "pokes"
pathlib.Path(OUT).mkdir(parents=True, exist_ok=True)

SET_CAM = """(a) => {
  const c = window.__ctl; if (!c) return;
  const t = c.target.clone();
  const r = c.object.position.distanceTo(t);
  const th = (90 - a.el) * Math.PI / 180;
  const ph = a.az * Math.PI / 180;
  c.object.position.set(
    t.x + r * Math.sin(th) * Math.sin(ph),
    t.y + r * Math.cos(th),
    t.z + r * Math.sin(th) * Math.cos(ph));
  c.update();
}"""

with sync_playwright() as p:
    b = p.chromium.launch(
        executable_path="/home/user/.cache/ms-playwright/chromium-1244/chrome-linux64/chrome",
        args=["--no-sandbox", "--use-gl=angle", "--use-angle=swiftshader", "--enable-unsafe-swiftshader"],
        env={**os.environ, "LD_LIBRARY_PATH": "/home/linuxbrew/.linuxbrew/lib"})
    pg = b.new_page(viewport={"width": 400, "height": 400})
    logs = []
    pg.on("console", lambda m: logs.append(f"[{m.type}] {m.text}"))
    pg.on("pageerror", lambda e: logs.append(f"[pageerror] {e.message}"))
    pg.goto(URL, wait_until="load")
    pg.wait_for_timeout(8000)

    # back view, poke the right buttock
    pg.evaluate(SET_CAM, {"az": 180, "el": 5})
    pg.wait_for_timeout(400)
    pg.mouse.click(140, 200)
    for i in range(14):
        amps = pg.evaluate("window.__scene.pokes.map(p => +p.a.toFixed(4)).filter(v=>v!==0)")
        pg.screenshot(path=f"{OUT}/b{i:02d}.png")
        pg.wait_for_timeout(70)
        print("t", i, "amps", amps)

    # fps measurement
    fps = pg.evaluate("""() => new Promise(res => {
        let n = 0; const t0 = performance.now();
        function tick(){ n++; if (performance.now() - t0 < 2000) requestAnimationFrame(tick); else res((n / (performance.now()-t0)*1000).toFixed(1)); }
        requestAnimationFrame(tick);
    })""")
    print("fps(swiftshader):", fps)
    print("\n".join(logs[:20]))
    b.close()
