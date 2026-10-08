import os, sys, pathlib
from playwright.sync_api import sync_playwright

URL = os.environ.get("TARGET", "file://" + sys.argv[1])
OUT = sys.argv[2] if len(sys.argv) > 2 else "shots"
pathlib.Path(OUT).mkdir(parents=True, exist_ok=True)

VIEWS = [
    ("front", 0, 8),
    ("back", 180, 8),
    ("left", 90, 8),
    ("right", 270, 8),
    ("q3", 40, 14),
    ("q4back", 220, 12),
    ("low", 20, -22),
    ("high", 20, 40),
]

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
    pg.wait_for_timeout(9000)
    for name, az, el in VIEWS:
        pg.evaluate(SET_CAM, {"az": az, "el": el})
        pg.wait_for_timeout(400)
        pg.screenshot(path=f"{OUT}/{name}.png")
    # poke
    pg.evaluate(SET_CAM, {"az": 0, "el": 5})
    pg.wait_for_timeout(300)
    pg.mouse.click(215, 250)
    for i in range(8):
        pg.wait_for_timeout(80)
        pg.screenshot(path=f"{OUT}/poke{i}.png")
    print("\n".join(logs[:40]))
    b.close()
