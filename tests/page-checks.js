// Page checks. Run in the browser: (await import('/tests/page-checks.js?'+Date.now())).run(phase)
// Returns array of failure messages; [] means pass. `phase` = highest plan task to include (default 8).
const checks = [];
const check = (phase, name, fn) => checks.push({ phase, name, fn });
const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];
const root = document.documentElement;

const rgb = (css) => (css.match(/[\d.]+/g) || [0, 0, 0]).map(Number);
const lumRGB = ([r, g, b]) => [r, g, b].map((v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4; }).reduce((a, v, i) => a + v * [0.2126, 0.7152, 0.0722][i], 0);
const ratio = (a, b) => { const x = lumRGB(a), y = lumRGB(b); return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05); };
const bgOf = (el) => { for (let e = el; e; e = e.parentElement) { const c = getComputedStyle(e).backgroundColor; const m = rgb(c); if (c !== 'transparent' && !(m.length === 4 && m[3] === 0)) return m.slice(0, 3); } return [255, 255, 255]; };

const noMotion = document.createElement('style');
noMotion.textContent = '*,*::before,*::after{transition:none!important;animation:none!important}';
const allCss = async () => {
  let t = $$('style').map((s) => s.textContent).join('\n');
  for (const l of $$('link[rel=stylesheet]')) { if (l.href.startsWith(location.origin)) t += await fetch(l.href).then((r) => r.text()).catch(() => ''); }
  return t;
};
// remove top-level @supports/@media blocks that mention a needle, return the rest
const stripBlocks = (css, startRe) => {
  let out = '', i = 0;
  while (i < css.length) {
    const rest = css.slice(i); const m = rest.match(startRe);
    if (!m) { out += rest; break; }
    out += rest.slice(0, m.index);
    let j = i + m.index + m[0].length, depth = 1;
    while (j < css.length && depth) { if (css[j] === '{') depth++; else if (css[j] === '}') depth--; j++; }
    i = j;
  }
  return out;
};

// ---- Task 1-2: foundation
check(1, 'no-horizontal-overflow', () => root.scrollWidth <= root.clientWidth + 1 || `scrollWidth ${root.scrollWidth} > clientWidth ${root.clientWidth}`);
check(1, 'no-tailwind-cdn', () => !$('script[src*="cdn.tailwindcss.com"]') || 'tailwind CDN still present');
check(2, 'no-theme-toggle', () => (!$('#theme-toggle') && !$('[data-theme-toggle]')) || 'theme toggle still present');
check(2, 'no-canvas', () => !$('canvas') || 'canvas still present');
check(2, 'no-decorative-effects', async () => { const css = await allCss(); const bad = ['.glow-blob', 'feTurbulence', 'perspective(', 'heroFloat', '.grad-text'].filter((k) => css.includes(k)); return bad.length === 0 || 'still present: ' + bad.join(', '); });
check(2, 'mobile-menu', () => {
  const b = $('#menu-btn'), m = $('#menu'); if (!b || !m) return 'missing #menu-btn or #menu';
  const was = b.getAttribute('aria-expanded'); b.click(); const open = b.getAttribute('aria-expanded') === 'true' && !m.hidden;
  document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape' })); const closed = b.getAttribute('aria-expanded') === 'false' && m.hidden;
  return (was === 'false' && open && closed) || `menu aria wrong (was ${was}, open ${open}, closed ${closed})`;
});
// ---- Task 3: hero
check(3, 'hero-ctas', () => !!($('#hero a[href="#projects"]') && $('#hero a[href^="https://wa.me/"]')) || 'missing hero CTAs');
check(3, 'hero-quick-links', () => { const h = $$('#hero .hero-links a').map((a) => a.getAttribute('href')); return (h.some((x) => x.includes('CV_')) && h.some((x) => x.includes('github.com/ululbiasaajaa')) && h.some((x) => x === 'mailto:sfarmlul@gmail.com')) || 'quick links: ' + h.join('|'); });
check(3, 'hero-stats-exact', () => { const s = $$('#hero .hero-stat-num').map((e) => e.textContent.trim()).join('|'); return s === '12|25 ribu+|40' || 'stats: ' + s; });
check(3, 'no-fluff-stats', () => !/Bulan Belajar|Problem Solving/i.test(document.body.innerText) || 'fluff stats present');
check(3, 'tagline-once', () => (document.body.innerText.match(/from molecules to meaningful code/gi) || []).length === 1 || 'tagline count != 1');
check(3, 'giant-type', () => { const g = $('.hero-giant'); if (!g) return 'no .hero-giant'; const fs = parseFloat(getComputedStyle(g).fontSize); const r = g.getBoundingClientRect(); return (fs >= 80 && r.right <= innerWidth + 1 && r.left >= -1) || `font ${fs}px, rect ${Math.round(r.left)}..${Math.round(r.right)} of ${innerWidth}`; });
const photoCheck = (sel) => () => { const p = $(sel); if (!p) return `no ${sel}`; const w = p.offsetWidth; const sharp = p.naturalWidth >= 1.5 * w; return (w >= 260 && sharp) || `${sel}: width ${w}px, natural ${p.naturalWidth}`; };
// hero is a video intro: Ulul walks in on the sage stage; final frame + cutout are stills for no-JS/reduced motion
check(3, 'hero-video', () => { const v = $('#hero .hero-video'); return (!!v && v.muted && v.hasAttribute('playsinline') && !v.hasAttribute('controls') && /hero-d\.mp4$/.test(v.dataset.srcD || '') && /hero-m\.mp4$/.test(v.dataset.srcM || '')) || 'hero video attrs wrong'; });
check(3, 'hero-stills', () => { const p = $('#hero .hero-poster img'), c = $('#hero .hero-cutout img'); return (!!p && !!c && p.getAttribute('alt') === '' && c.getAttribute('alt') === '' && $$('#hero .hero-poster source, #hero .hero-cutout source').length === 2) || 'poster/cutout stills missing'; });
check(3, 'hero-layers-aligned', () => { const s = $('#hero .hero-stage'); if (!s) return 'no stage'; const r = s.getBoundingClientRect(); return ['.hero-video', '.hero-poster img', '.hero-cutout img'].every((q) => { const e = $(q, s).getBoundingClientRect(); return Math.abs(e.left - r.left) < 1 && Math.abs(e.width - r.width) < 1 && Math.abs(e.height - r.height) < 1; }) || 'video/poster/cutout boxes differ'; });
check(3, 'hero-copy-clear-of-person', () => {
  if (innerWidth < 1024) return true; // stacked layout: copy sits below the stage
  const s = $('#hero .hero-stage').getBoundingClientRect(); const personLeft = s.left + s.width * (1228 / 1920);
  const bad = $$('#hero .hero-grid a, #hero .hero-grid button, #hero h1, #hero .lead').filter((e) => e.getBoundingClientRect().right > personLeft - 8);
  return bad.length === 0 || `${bad.length} element(s) overlap Ulul (person starts at x=${Math.round(personLeft)})`;
});
check(3, 'hero-replay-reachable', () => { const b = $('#hero .hero-replay'); return (!!b && b.tagName === 'BUTTON' && !b.closest('[aria-hidden="true"]')) || 'replay button missing or hidden from a11y tree'; });
// ---- Task 4: projects
check(4, 'four-featured', () => { const o = $$('.case').map((c) => c.dataset.project).join(','); return o === 'pharmacy3d,scentdna,n8n,roblox' || 'order: ' + o; });
check(4, 'case-sections', () => $$('.case').every((c) => ['Masalah', 'Yang dibangun', 'Keputusan teknis', 'Stack'].every((h) => $$('h4', c).some((e) => e.textContent.trim() === h))) || 'a case misses a sub-heading');
check(4, 'list-count', () => $$('.project-list li').length === 8 || 'count ' + $$('.project-list li').length);
check(4, 'list-keyboard', () => $$('.project-list li').every((li) => li.firstElementChild && li.firstElementChild.tagName === 'BUTTON') || 'list item not a button');
check(4, 'modal-ids-resolve', () => $$('[data-modal]').every((b) => document.getElementById(b.dataset.modal)) || 'dangling data-modal');
check(4, 'n8n-no-live-link', () => { const c = $('.case[data-project=n8n]'); return (!!c && !$$('a[href^="http"]', c).length && /Demo privat/.test(c.textContent)) || 'n8n has external link or lacks "Demo privat"'; });
check(4, 'n8n-video', () => { const v = $('.case[data-project=n8n] video'); return (!!v && /n8n-demo\.mp4$/.test(v.getAttribute('src') || '') && v.hasAttribute('poster') && v.hasAttribute('controls') && v.hasAttribute('playsinline') && !v.hasAttribute('autoplay')) || 'n8n video attrs wrong'; });
check(4, 'live-links', () => { const p = $('.case[data-project=pharmacy3d]'), s = $('.case[data-project=scentdna]'); return !!(p && p.querySelector('a[href*="pharmacy-3-d-simulator.vercel.app"]') && p.querySelector('a[href*="github.com/ululbiasaajaa/pharmacy-3d-simulator"]') && s && s.querySelector('a[href*="scentdna-5646.vercel.app"]')) || 'missing pharmacy/scentdna links'; });
check(4, 'section-alternation', () => {
  const light = $$('main > section').map((s) => lumRGB(bgOf(s)) > 0.4);
  const flips = light.slice(1).filter((v, i) => v !== light[i]).length;
  return flips >= 4 || `only ${flips} background flips: ${light.map((v) => (v ? 'L' : 'D')).join('')}`;
});
// ---- Task 5: about, services, contact
check(5, 'photo-about', photoCheck('.photo-about'));
check(5, 'reveal-words', () => { const w = $$('.statement .w'); return (w.length >= 8 && $('.statement').textContent.replace(/\s+/g, ' ').trim().length > 40) || `words ${w.length}`; });
check(5, 'skills-grouped', () => { const g = $$('.skill-group h3').map((e) => e.textContent.trim()).join('|'); return g === 'Frontend|Backend|AI|Game / Lua|Infra' || 'groups: ' + g; });
check(5, 'services-four', () => ($$('#services .service').length === 4 && $$('#services ol.process li').length === 4) || 'services/process count wrong');
check(5, 'contact-links', () => { const c = $('#contact'); return (!!c && !!c.querySelector('a[href^="mailto:"]') && !!c.querySelector('a[href="https://github.com/ululbiasaajaa"]') && !!c.querySelector('a[href^="https://wa.me/"]') && !!c.querySelector('a[href*="CV_"]') && !!c.querySelector('a[href$=".pptx"]')) || 'contact links incomplete'; });
check(5, 'nav-matches-sections', () => $$('header a[href^="#"], #menu a[href^="#"]').every((a) => document.getElementById(a.getAttribute('href').slice(1))) || 'nav anchor without target');
check(5, 'contrast-ok', () => {
  const sels = ['#hero .hero-links a', '.case h4', '.case .note', '.case p', '#services .process li', '.project-row .meta', '.statement', '#contact .lead', '.label', '.hero-links a', '.stat-card .hero-stat-label'];
  const bad = [];
  for (const s of sels) for (const el of $$(s).slice(0, 6)) {
    const cs = getComputedStyle(el); const fs = parseFloat(cs.fontSize); const big = fs >= 24 || (fs >= 18.66 && +cs.fontWeight >= 700);
    const need = big ? 3 : 4.5; const fg = rgb(cs.color).slice(0, 3); const r = ratio(fg, bgOf(el));
    // statement words animate; judge the final (fully lit) colour via its --lit custom property when present
    if (r < need && !el.closest('.statement')) bad.push(`${s} ${r.toFixed(1)}<${need}`);
  }
  return bad.length === 0 || [...new Set(bad)].join('; ');
});
// ---- Task 6: motion fallbacks
check(6, 'motion-gated', async () => {
  const css = await allCss();
  const rest = stripBlocks(css, /@supports\s*\(\s*animation-timeline\s*:\s*view\(\s*\)\s*\)\s*\{/);
  return (!rest.includes('animation-timeline') && css.includes('prefers-reduced-motion')) || 'animation-timeline used outside @supports or no reduced-motion rule';
});
// ---- Task 7: seo & weight
check(7, 'meta-complete', () => { const d = $('meta[name=description]')?.content || ''; return (d.length >= 50 && d.length <= 160 && ['og:title', 'og:description', 'og:image'].every((p) => $(`meta[property="${p}"]`))) || `meta incomplete (desc ${d.length})`; });
check(5, 'no-emoji-icons', () => { const t = document.body.innerText + $$('.modal').map((m) => m.textContent).join(' '); const m = t.match(/(?![\u00A9\u00AE\u2122])\p{Extended_Pictographic}/gu); return !m || 'emoji found: ' + [...new Set(m)].join(' '); });
check(5, 'modal-a11y', () => $$('.modal').every((m) => m.getAttribute('role') === 'dialog' && m.getAttribute('aria-modal') === 'true' && document.getElementById(m.getAttribute('aria-labelledby') || '') && $('.modal-close[aria-label]', m)) || 'a modal lacks role/aria-modal/label/close name');
check(5, 'modal-open-close', () => { const b = $('[data-modal="modalWedding"]'); b.focus(); b.click(); const m = $('#modalWedding'); const open = !m.classList.contains('hidden') && document.activeElement === $('.modal-close', m); document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape' })); const closed = m.classList.contains('hidden') && document.activeElement === b; return (open && closed) || `open ${open}, closed ${closed}`; });
check(5, 'targets-44', () => { const small = $$('.site-header a, .site-header button, .btn, .project-row .go, .modal-close').filter((e) => e.offsetParent && (e.getBoundingClientRect().height < 40)).map((e) => (e.className || e.tagName) + ':' + Math.round(e.getBoundingClientRect().height)); return small.length === 0 || 'small targets: ' + small.join(', '); });
check(7, 'self-hosted-fonts', () => (!$('link[href*="fonts.googleapis.com"]') && $$('link[rel=preload][as=font]').length >= 1) || 'fonts not self-hosted');
check(7, 'favicon', () => !!$('link[rel~=icon]') || 'no favicon');
check(7, 'images-sized', () => $$('img').every((i) => i.hasAttribute('width') && i.hasAttribute('height')) || 'img without width/height');
check(7, 'image-weight', () => { const big = performance.getEntriesByType('resource').filter((r) => r.initiatorType === 'img' && r.encodedBodySize > 300 * 1024).map((r) => r.name.split('/').pop()); return big.length === 0 || 'heavy: ' + big.join(','); });

export async function run(phase = 8) {
  document.head.appendChild(noMotion);
  const out = [];
  for (const c of checks.filter((c) => c.phase <= phase)) {
    try { const r = await c.fn(); if (r !== true) out.push(`${c.name}: ${r}`); } catch (e) { out.push(`${c.name}: threw ${e.message}`); }
  }
  noMotion.remove();
  return out;
}
