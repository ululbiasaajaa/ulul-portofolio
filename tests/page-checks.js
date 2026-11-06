// Page checks. Run in the browser: (await import('/tests/page-checks.js')).run(phase)
// Returns array of failure messages; [] means pass. `phase` = highest plan task to include (default 8).
const checks = [];
const check = (phase, name, fn) => checks.push({ phase, name, fn });
const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];
const lum = (css) => {
  const m = css.match(/[\d.]+/g).map(Number);
  const [r, g, b] = m.slice(0, 3).map((v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4; });
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
};
const root = document.documentElement;
const noMotion = document.createElement('style');
noMotion.textContent = '*,*::before,*::after{transition:none!important;animation:none!important}';
const withTheme = (t, fn) => {
  document.head.appendChild(noMotion);
  const prev = root.getAttribute('data-theme');
  t === 'light' ? root.setAttribute('data-theme', 'light') : root.removeAttribute('data-theme');
  try { return fn(); } finally { prev ? root.setAttribute('data-theme', prev) : root.removeAttribute('data-theme'); }
};
const allCss = async () => {
  let t = $$('style').map((s) => s.textContent).join('\n');
  for (const l of $$('link[rel=stylesheet]')) { if (l.href.startsWith(location.origin)) t += await fetch(l.href).then((r) => r.text()).catch(() => ''); }
  return t;
};

// Task 1-2
check(1, 'no-horizontal-overflow', () => root.scrollWidth <= root.clientWidth + 1 || `scrollWidth ${root.scrollWidth} > clientWidth ${root.clientWidth}`);
check(1, 'hero-heading-readable', () => ['dark', 'light'].map((t) => withTheme(t, () => lum(getComputedStyle($('#hero h1') || $('.hero-section h1')).color) > 0.6 || `h1 too dark in ${t}`)).find((r) => r !== true) || true);
check(1, 'no-tailwind-cdn', () => !$('script[src*="cdn.tailwindcss.com"]') || 'tailwind CDN still present');
check(2, 'no-decorative-effects', async () => {
  const css = await allCss();
  const bad = ['.glow-blob', 'feTurbulence', 'perspective(', 'heroFloat', '.grad-text'].filter((k) => css.includes(k));
  return bad.length === 0 || 'still present: ' + bad.join(', ') + ($$('.glow-blob').length ? ' (dom blobs)' : '');
});
// Task 3
check(3, 'hero-ctas', () => !!($('#hero a[href="#projects"]') && $('#hero a[href^="https://wa.me/"]')) || 'missing hero CTAs');
check(3, 'hero-quick-links', () => { const h = $$('#hero .hero-links a').map((a) => a.getAttribute('href')); return (h.some((x) => x.includes('CV_')) && h.some((x) => x.includes('github.com/ululbiasaajaa')) && h.some((x) => x === 'mailto:sfarmlul@gmail.com')) || 'quick links: ' + h.join('|'); });
check(3, 'hero-stats-exact', () => { const s = $$('#hero .hero-stat-num').map((e) => e.textContent.trim()).join('|'); return s === '12|25 ribu+|40' || 'stats: ' + s; });
check(3, 'no-fluff-stats', () => !/Bulan Belajar|Problem Solving/i.test(document.body.innerText) || 'fluff stats present');
// Task 4
check(4, 'four-featured', () => { const o = $$('.case').map((c) => c.dataset.project).join(','); return o === 'pharmacy3d,scentdna,n8n,roblox' || 'order: ' + o; });
check(4, 'case-sections', () => $$('.case').every((c) => ['Masalah', 'Yang dibangun', 'Keputusan teknis', 'Stack'].every((h) => $$('h4', c).some((e) => e.textContent.trim() === h))) || 'a case misses a sub-heading');
check(4, 'list-count', () => $$('.project-list li').length === 8 || 'count ' + $$('.project-list li').length);
check(4, 'list-keyboard', () => $$('.project-list li').every((li) => li.firstElementChild && li.firstElementChild.tagName === 'BUTTON') || 'list item not a button');
check(4, 'modal-ids-resolve', () => $$('[data-modal]').every((b) => document.getElementById(b.dataset.modal)) || 'dangling data-modal');
check(4, 'n8n-no-live-link', () => { const c = $('.case[data-project=n8n]'); return !!c && !$$('a[href^="http"]', c).length && /Demo privat/.test(c.textContent) || 'n8n has external link or lacks "Demo privat"'; });
check(4, 'n8n-video', () => { const v = $('.case[data-project=n8n] video'); return !!v && /n8n-demo\.mp4$/.test(v.getAttribute('src') || '') && v.hasAttribute('poster') && v.hasAttribute('controls') && v.hasAttribute('playsinline') && !v.hasAttribute('autoplay') || 'n8n video attrs wrong'; });
check(4, 'live-links', () => { const p = $('.case[data-project=pharmacy3d]'), s = $('.case[data-project=scentdna]'); return !!(p && p.querySelector('a[href*="pharmacy-3-d-simulator.vercel.app"]') && p.querySelector('a[href*="github.com/ululbiasaajaa/pharmacy-3d-simulator"]') && s && s.querySelector('a[href*="scentdna-5646.vercel.app"]')) || 'missing pharmacy/scentdna links'; });
// Task 5
check(5, 'skills-grouped', () => { const g = $$('.skill-group h3').map((e) => e.textContent.trim()).join('|'); return g === 'Frontend|Backend|AI|Game / Lua|Infra' || 'groups: ' + g; });
check(5, 'services-four', () => ($$('#services .service').length === 4 && $$('#services ol.process li').length === 4) || 'services/process count wrong');
check(5, 'contact-links', () => { const c = $('#contact'); return !!c && !!c.querySelector('a[href^="mailto:"]') && !!c.querySelector('a[href="https://github.com/ululbiasaajaa"]') && !!c.querySelector('a[href^="https://wa.me/"]') && !!c.querySelector('a[href*="CV_"]') && !!c.querySelector('a[href$=".pptx"]') || 'contact links incomplete'; });
check(5, 'tagline-once', () => (document.body.innerText.match(/from molecules to meaningful code/gi) || []).length === 1 || 'tagline count != 1');
check(5, 'nav-matches-sections', () => $$('header nav a[href^="#"]').every((a) => document.getElementById(a.getAttribute('href').slice(1))) || 'nav anchor without target');
// Task 6
check(6, 'reveal-visible-without-js', () => { root.classList.remove('js'); const ok = $$('.reveal').every((e) => getComputedStyle(e).opacity === '1'); root.classList.add('js'); return ok || '.reveal hidden without js class'; });
check(6, 'canvas-in-hero-only', () => { const c = $$('canvas'); return c.length === 1 && !!c[0].closest('#hero') || 'canvas not only in #hero'; });
check(6, 'reduced-motion-css', async () => (await allCss()).includes('prefers-reduced-motion') || 'no reduced-motion rule');
// Task 7
check(7, 'meta-complete', () => { const d = $('meta[name=description]')?.content || ''; return d.length >= 50 && d.length <= 160 && ['og:title', 'og:description', 'og:image'].every((p) => $(`meta[property="${p}"]`)) || `meta incomplete (desc ${d.length})`; });
check(7, 'favicon', () => !!$('link[rel~=icon]') || 'no favicon');
check(7, 'title-specific', () => !/^Muhammad Ulul Albab - Web & App Developer Portfolio$/.test(document.title) || 'generic title');
check(7, 'images-sized', () => $$('img').every((i) => i.hasAttribute('width') && i.hasAttribute('height')) || 'img without width/height');
check(7, 'image-weight', () => { const big = performance.getEntriesByType('resource').filter((r) => r.initiatorType === 'img' && r.encodedBodySize > 300 * 1024).map((r) => r.name.split('/').pop()); return big.length === 0 || 'heavy: ' + big.join(','); });

export async function run(phase = 8) {
  const out = [];
  for (const c of checks.filter((c) => c.phase <= phase)) {
    try { const r = await c.fn(); if (r !== true) out.push(`${c.name}: ${r}`); } catch (e) { out.push(`${c.name}: threw ${e.message}`); }
  }
  return out;
}
