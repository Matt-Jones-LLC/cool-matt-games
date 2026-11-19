/* Retake the home-page thumbnails. Needs Playwright and a local server:
     python3 -m http.server 8123 &   then   node _build/shots.js
   Each thumbnail is the top of the piece's own stage, 1440 x 900, saved to assets/shots/<slug>.jpg. */
const { chromium } = require('playwright');
const path = require('path');
const PIECES = {
  'slick-shift': { prep: () => window.__slick.load(10), sel: '.ss-canvas' },
  'goldfish': {}, 'second-opinion': {}, 'llmadness': {}, 'context-budget': {}, 'windhover': {}, 'thermostat': {}, 'breather': {}, 'calendar': {},
  'cry-wolf': { sel: '.cw .mapcard' },
  'downhill': { prep: () => { for (let i = 0; i < 14; i++) window.__dh.drop(.1 + Math.random() * 1.4, .1 + Math.random() * .8); }, wait: 2500 },
  'follow-the-sun': { sel: '#fts .mapcard' },
};
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 860, height: 1000 }, deviceScaleFactor: 2, colorScheme: 'light' });
  for (const [slug, o] of Object.entries(PIECES)) {
    await p.goto('http://localhost:8123/' + slug + '/');
    await p.waitForTimeout(700);
    if (o.prep) await p.evaluate(o.prep);
    await p.waitForTimeout(o.wait || 500);
    const el = p.locator(o.sel || '.stage').first();
    await el.scrollIntoViewIfNeeded();
    const r = await el.boundingBox();
    const h = Math.min(r.height, r.width * 450 / 720);
    await p.screenshot({ path: path.join(__dirname, '../assets/shots', slug + '.jpg'), type: 'jpeg', quality: 82, clip: { x: r.x, y: r.y, width: r.width, height: h } });
    console.log('shot', slug, Math.round(r.width), Math.round(h));
  }
  await b.close();
})();
