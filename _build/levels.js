/* Picks the Slick Shift levels. Run:  node _build/levels.js   (then python3 _build/site.py)

   For each level it makes a few thousand random floor plans with the listed ingredients, solves every
   one with the game's own solver, and keeps the plan whose shortest solution is longest (up to a cap)
   and actually uses each ingredient. The result is written into _build/src/pieces/slick-shift.html.
   The random numbers are seeded, so the same levels come out every time. */
const fs = require('fs'), path = require('path');
const file = path.join(__dirname, 'src/pieces/slick-shift.html');
let src = fs.readFileSync(file, 'utf8');
const core = src.match(/\/\*core\*\/([\s\S]*?)\/\*end core\*\//)[1];
const G = new Function(core + '; return { parse, start, move, solve };')();

let seed = 20261119;
const rnd = () => { seed |= 0; seed = seed + 0x6D2B79F5 | 0; let t = Math.imul(seed ^ seed >>> 15, 1 | seed); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
const ri = n => Math.floor(rnd() * n);

// name, width, height, wall share, ingredients, [fewest, most] moves in the shortest solution
const SPEC = [
  ['Clocking in',     8, 6, .10, {},                                  [3, 4]],
  ['Battery run',     9, 6, .10, { '*': 2 },                          [5, 6]],
  ['Mind the gap',    9, 7, .08, { '*': 2, x: 4 },                    [6, 8]],
  ['Sticky situation', 10, 7, .07, { '*': 3, o: 3, x: 2 },            [7, 9]],
  ['Thin ice',       10, 7, .08, { '*': 3, '~': 6 },                  [8, 10]],
  ['Open sesame',    10, 7, .08, { '*': 2, b: 1, D: 3, d: 2 },        [8, 11]],
  ['Conveyor belt',  11, 7, .07, { '*': 3, conv: 5 },                 [8, 11]],
  ['Shortcut',       11, 7, .09, { '*': 3, '1': 2, x: 2 },            [9, 12]],
  ['Double booked',  11, 8, .07, { '*': 3, o: 2, '~': 5, b: 1, D: 3, d: 2 }, [11, 14]],
  ['Rush hour',      12, 8, .07, { '*': 4, conv: 5, '1': 2, x: 4 },   [12, 15]],
  ['The works',      12, 9, .07, { '*': 4, o: 2, '~': 4, b: 1, D: 3, d: 2, conv: 4, '1': 2, x: 3 }, [14, 18]],
  ['Overtime',       13, 9, .07, { '*': 5, o: 3, '~': 5, b: 2, D: 4, d: 3, conv: 4, '1': 2, '2': 2, x: 4 }, [16, 22]],
];

function make(w, h, walls, items) {
  const g = Array.from({ length: h }, (_, y) => Array.from({ length: w }, (_, x) => (x === 0 || y === 0 || x === w - 1 || y === h - 1) ? '#' : (rnd() < walls ? '#' : '.')));
  const free = () => { for (let k = 0; k < 200; k++) { const x = 1 + ri(w - 2), y = 1 + ri(h - 2); if (g[y][x] === '.') return [x, y]; } return null; };
  const put = ch => { const p = free(); if (p) g[p[1]][p[0]] = ch; };
  put('S'); put('E');
  for (const k in items) for (let i = 0; i < items[k]; i++) put(k === 'conv' ? '^v<>'[ri(4)] : k);
  return g.map(r => r.join(''));
}
/* Which ingredients does the shortest solution actually touch? */
function used(L, sol) {
  let s = G.start(L); const seen = new Set();
  for (const d of sol) {
    const r = G.move(L, s, d);
    for (const p of r.path) {
      const c = L.t[p.y * L.w + p.x];
      if (c === 'D' || c === 'd') seen.add('door');
      if (p.ev === 'stick') seen.add('o');
      if (p.ev === 'btn') seen.add('b');
      if (p.ev === 'tpin') seen.add('tp');
      if ('^v<>'.includes(c)) seen.add('conv');
      if (c === '~') seen.add('~');
    }
    s = r.s;
  }
  return seen;
}
const out = [];
for (const [name, w, h, walls, items, [lo, hi]] of SPEC) {
  let best = null;
  for (let tries = 0; tries < 60000 && !(best && best.n === hi && tries > 6000); tries++) {
    const rows = make(w, h, walls, items), L = G.parse(rows);
    const sol = G.solve(L, G.start(L), 60000);
    if (!sol || sol.length < lo || sol.length > hi) continue;
    const u = used(L, sol);
    if (items.o && !u.has('o')) continue;
    if (items.b && !(u.has('b') && u.has('door'))) continue;
    if (items['1'] && !u.has('tp')) continue;
    if (items.conv && !u.has('conv')) continue;
    if (items['~'] && !u.has('~')) continue;
    // a first move that wins nothing but is forced makes for a dull opening: prefer levels with a choice
    const firsts = ['U', 'D', 'L', 'R'].filter(d => { const r = G.move(L, G.start(L), d); return r && !r.dead; }).length;
    const score = sol.length * 10 + firsts;
    if (!best || score > best.score) best = { rows, n: sol.length, score, sol: sol.join('') };
  }
  if (!best) throw new Error('no level found for ' + name);
  console.log(name.padEnd(18), 'shortest', best.n, best.sol); console.log(best.rows.join('\n'));
  out.push({ name, par: best.n, rows: best.rows });
}
src = src.replace(/\/\*levels\*\/[\s\S]*?\/\*end levels\*\//, '/*levels*/' + JSON.stringify(out).replace(/\{"name"/g, '\n  {"name"') + '\n/*end levels*/');
fs.writeFileSync(file, src);
console.log('wrote', out.length, 'levels');
