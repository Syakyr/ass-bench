import os
from playwright.sync_api import sync_playwright
URL = "file:///home/user/Codebase/ass-bench/figure.html?t=1"
MEAS = """() => new Promise(res => { let n=0; const t0=performance.now();
  function tick(){ n++; if (performance.now()-t0 < 1500) requestAnimationFrame(tick); else res(+(n/(performance.now()-t0)*1000).toFixed(1)); }
  requestAnimationFrame(tick); })"""
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/home/user/.cache/ms-playwright/chromium-1244/chrome-linux64/chrome",
        args=["--no-sandbox","--use-gl=angle","--use-angle=swiftshader","--enable-unsafe-swiftshader"],
        env={**os.environ,"LD_LIBRARY_PATH":"/home/linuxbrew/.linuxbrew/lib"})
    pg = b.new_page(viewport={"width":400,"height":400})
    pg.goto(URL, wait_until="load"); pg.wait_for_timeout(8000)
    print("baseline", pg.evaluate(MEAS))
    pg.evaluate("window.__scene.bodyMesh.material.sheen=0; window.__scene.bodyMesh.material.needsUpdate=true; window.__scene.briefMesh.material.sheen=0; window.__scene.briefMesh.material.clearcoat=0; window.__scene.briefMesh.material.needsUpdate=true;")
    print("no sheen/clearcoat", pg.evaluate(MEAS))
    pg.evaluate("window.__scene.bodyMesh.material.roughness=0.5; window.__scene.bodyMesh.onBeforeCompile=()=>{}; window.__scene.bodyMesh.material.customProgramCacheKey=()=>'plain'; window.__scene.bodyMesh.material.needsUpdate=true;")
    print("plain physical (no custom fs)", pg.evaluate(MEAS))
    b.close()
