import { chromium } from '/tmp/pwtest/node_modules/playwright/index.js';

const URL = process.env.TARGET || ('file://' + process.argv[2]);
const OUT = process.argv[3] || 'shots';
import fs from 'fs';
fs.mkdirSync(OUT, { recursive: true });

const VIEWS = [
  ['front', 0, 8],
  ['back', 180, 8],
  ['left', 90, 8],
  ['right', 270, 8],
  ['q3', 40, 14],
  ['q4back', 220, 12],
  ['low', 20, -22],
  ['high', 20, 40],
];

const browser = await chromium.launch({ executablePath: '/home/user/.cache/ms-playwright/chromium-1244/chrome-linux64/chrome', args: ['--no-sandbox', '--use-gl=swiftshader', '--enable-unsafe-swiftshader'] });
const page = await browser.newPage({ viewport: { width: 400, height: 400 } });
const logs = [];
page.on('console', m => logs.push(`[${m.type()}] ${m.text()}`));
page.on('pageerror', e => logs.push(`[pageerror] ${e.message}`));
await page.goto(URL, { waitUntil: 'load' });
await page.waitForTimeout(9000);

// expose a helper to set the camera orbit angles
for (const [name, az, el] of VIEWS) {
  await page.evaluate(({ az, el }) => {
    const c = window.__ctl;
    if (!c) return;
    const t = c.target.clone();
    const r = c.object.position.distanceTo(t);
    const th = (90 - el) * Math.PI / 180;   // polar
    const ph = az * Math.PI / 180;
    c.object.position.set(
      t.x + r * Math.sin(th) * Math.sin(ph),
      t.y + r * Math.cos(th),
      t.z + r * Math.sin(th) * Math.cos(ph)
    );
    c.update();
  }, { az, el });
  await page.waitForTimeout(450);
  await page.screenshot({ path: `${OUT}/${name}.png` });
}

// poke test
await page.evaluate(({ az, el }) => { const c = window.__ctl; if (!c) return; const t = c.target.clone(); const r = c.object.position.distanceTo(t); const th = (90 - el) * Math.PI / 180; const ph = az * Math.PI / 180; c.object.position.set(t.x + r * Math.sin(th) * Math.sin(ph), t.y + r * Math.cos(th), t.z + r * Math.sin(th) * Math.cos(ph)); c.update(); }, { az: 0, el: 5 });
await page.waitForTimeout(300);
await page.mouse.click(200, 250);
for (const i of [0, 1, 2, 3, 4, 5]) {
  await page.waitForTimeout(90);
  await page.screenshot({ path: `${OUT}/poke${i}.png` });
}

console.log(logs.join('\n'));
await browser.close();
