import os, pathlib
from playwright.sync_api import sync_playwright
URL = "file:///home/user/Codebase/ass-bench/figure.html"
OUT = "/tmp/pv"; pathlib.Path(OUT).mkdir(parents=True, exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/home/user/.cache/ms-playwright/chromium-1244/chrome-linux64/chrome",
        args=["--no-sandbox","--use-gl=angle","--use-angle=swiftshader","--enable-unsafe-swiftshader"],
        env={**os.environ,"LD_LIBRARY_PATH":"/home/linuxbrew/.linuxbrew/lib"})
    pg = b.new_page(viewport={"width":400,"height":400})
    errs=[]; pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(URL, wait_until="load"); pg.wait_for_timeout(9000)
    pg.screenshot(path=f"{OUT}/a_rest.png")
    pg.mouse.click(150, 215)          # left buttock-ish
    for i in range(9):
        pg.wait_for_timeout(70)
        pg.screenshot(path=f"{OUT}/b{i}.png")
    print("errors:", errs or "(none)")
    b.close()
