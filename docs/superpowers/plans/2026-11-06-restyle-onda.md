# Restyle Onda-inspired Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans (Native, dipilih Ulul) or superpowers:subagent-driven-development. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ganti bungkus visual `index.html` (tipografi raksasa, section selang-seling gelap/krem, foto besar yang berpindah saat scroll, kalimat farmasi menyala per kata) tanpa mengubah isi.

**Architecture:** Tetap statis. Section diganti satu per satu di antara marker komentar `<!-- N. ... -->` di `index.html`; modal proyek lain tidak disentuh. Semua gerakan memakai CSS scroll-driven (`animation-timeline`) dalam `@supports` + `prefers-reduced-motion: no-preference`; tanpa dukungan = keadaan statis rapi. Satu skrip JS kecil hanya memecah kalimat per kata.

**Tech Stack:** HTML, Tailwind 3.4 CLI (`npm run build:css`), CSS scroll-driven animations, Gabarito + Inter + JetBrains Mono, Pillow.

**Spec:** `docs/superpowers/specs/2026-11-06-restyle-onda-design.md`

## Global Constraints

- Branch `restyle`. Tidak mengubah copy proyek, data, tautan, atau modal 8 proyek lain.
- Tema tunggal: `--ink #0b0d12`, `--paper #f3efe6`; aksen fill `#22e6b5` (gelap) / `#0e9c78` (krem); teks aksen di krem `#087055`. Toggle dark/light dan `localStorage` tema dihapus.
- Foto: diameter `clamp(300px, 34vw, 520px)` desktop; mobile ≥ `72vw`; tidak pernah < 260 px; sumber `ulul-foto-lg.webp` lebar 1000 px; wajah tidak terpotong (`object-position: top`).
- Gerakan hanya 3: huruf hero, foto, kalimat per kata. Semuanya mati di `prefers-reduced-motion: reduce`. Canvas molekul dibuang.
- Judul hero `clamp(5rem, 22vw, 18rem)`; judul section `clamp(2.6rem, 7vw, 6rem)` berakhir titik aksen.
- Kontras teks ≥ 4,5:1 (≥ 3:1 untuk teks ≥ 24 px). Tidak ada scroll horizontal di 320/375/1024 px.
- Selector yang dipakai `tests/page-checks.js` tetap: `.hero-stat-num`, `.case[data-project]`, `.skill-group h3`, `#services .service`, `ol.process li`, `.project-list li > button[data-modal]`.
- Stat hero tetap `12 | 25 ribu+ | 40`; tagline "From molecules to meaningful code." muncul tepat sekali.

## Review Focus

1. Layar 320 px: huruf raksasa "Halo." dan judul panjang ("Pharmacy 3D.") tidak meluap atau terpotong.
2. Browser tanpa `animation-timeline`: semua teks, foto (hero dan about), dan kata-kata kalimat farmasi tampil penuh dan terbaca.
3. `prefers-reduced-motion`: tidak ada gerakan, foto tetap tampil besar.
4. Foto hero tidak menutupi tombol CTA atau teks di 375 px (urutan tumpuk benar).
5. Menu mobile: bisa dibuka/tutup dengan keyboard (Esc menutup), tautan menutup menu setelah diklik.

## File Structure

- Modify: `index.html` (semua section kecuali modal), `assets/src/input.css` (ditulis ulang), `tests/page-checks.js`
- Create: `ulul-foto-lg.webp`
- Output build: `assets/site.css`

## Cara verifikasi (semua task)

`npm run serve` (background) lalu `http://localhost:8080/` di browser pane; `npm run build:css` setelah mengubah CSS/class. Jalankan `(await import('/tests/page-checks.js?'+Date.now())).run(phase)`; hasil `[]` = lulus. Cek visual di 320, 375, 1024 px.

---

### Task 1: Harness baru dan aset

**Files:**
- Modify: `tests/page-checks.js`
- Create: `ulul-foto-lg.webp`

**Interfaces:**
- Produces: check baru (phase = nomor task pemiliknya): `no-theme-toggle` (tidak ada `#theme-toggle`), `no-canvas` (tidak ada `<canvas>`), `photo-min-size` (`.photo-hero` dan `.photo-about` lebar ≥ 260 px), `photo-sharp` (`naturalWidth ≥ 1.5 × lebar tampil`), `giant-type` (font-size `.hero-giant` ≥ 80 px dan lebar elemen ≤ viewport), `section-alternation` (≥ 4 pergantian latar antar section berurutan), `contrast-ok` (h1, `.case h4`, `.note`, `.process li`, `.project-row .meta` ≥ 4,5:1 terhadap latar efektif), `mobile-menu` (`#menu-btn` ada, `aria-expanded` berubah saat diklik, Esc menutup), `reveal-words` (`.statement .w` ada, setiap kata `opacity` 1 saat `animation-timeline` tidak didukung/diabaikan).
- Consumes: helper `check`, `$`, `$$`, `lum` yang sudah ada.

- [ ] **Step 1:** Hapus check `hero-heading-readable`, `canvas-in-hero-only`, `reveal-visible-without-js` dari harness; tambahkan semua check di atas dengan nomor phase task pemiliknya (2-6).
- [ ] **Step 2:** Jalankan di halaman sekarang — Expected: check baru gagal (membuktikan harness menangkap).
- [ ] **Step 3:** Buat `ulul-foto-lg.webp` dari `Ulul Foto Formal.jpg` (Pillow, lebar 1000, quality 82); Expected: file ≤ 120 KB dan 1000×1250.

### Task 2: Fondasi — token, font, nav pil, menu mobile

**Files:**
- Modify: `assets/src/input.css` (tulis ulang), `index.html` (`<head>`, `<header>`, skrip bawah)

**Interfaces:**
- Produces: kelas `.sec-dark` / `.sec-paper` (latar + warna teks + variabel `--accent-text` per latar), `.display` (judul raksasa), `.dot` (titik aksen), `#menu-btn`, `#menu` (panel), `<nav class="pill">`.

- [ ] **Step 1:** Ganti font di `<head>` ke Gabarito (600;800), Inter, JetBrains Mono; hapus skrip tema, `ulul-theme`, dan `#theme-toggle`.
- [ ] **Step 2:** Tulis ulang `input.css`: token palet, `.sec-dark/.sec-paper`, `.display`, `.dot::after { content: "."; color: var(--accent-text) }`, pil nav `position: fixed; top: 14px`, panel menu mobile; pertahankan kelas `.case`, `.chips`, `.chip`, `.project-row`, `.service`, `.process`, `.contact-card` yang dipakai markup (restyle isi ada di task 4-5).
- [ ] **Step 3:** Implementasi `#menu-btn` (toggle `aria-expanded`, panel `hidden`), `keydown` Esc menutup, klik tautan menutup; tidak ada library.
- [ ] **Step 4:** `npm run build:css`; jalankan harness phase 2 — Expected: `no-theme-toggle`, `no-canvas` (hapus `<canvas>` dan skripnya), `mobile-menu`, `no-horizontal-overflow` lulus.

### Task 3: Hero — huruf raksasa dan foto besar

**Files:**
- Modify: `index.html` (section `<!-- 1. Hero -->`), `assets/src/input.css`

**Interfaces:**
- Produces: `#hero.sec-dark` berisi `.hero-giant` ("Halo."), `<img class="photo-hero" src="ulul-foto-lg.webp" width="1000" height="1250">`, kalimat posisi, CTA, `.hero-links`, `.hero-stat-num` ×3, tagline.

- [ ] **Step 1:** Tulis markup hero: kalimat posisi kecil di atas, `.hero-giant` raksasa di bawah, foto bulat besar (cincin teal, satu titik orbit via `@keyframes` rotasi pelan) di kanan dan menimpa sebagian huruf; urutan tumpuk mobile: foto, kalimat, CTA, giant (CTA tidak tertutup foto).
- [ ] **Step 2:** CSS foto: `width: clamp(300px, 34vw, 520px)` desktop, `max(72vw, 260px)` ≤ 640 px; `border-radius: 50%; object-fit: cover; object-position: top`.
- [ ] **Step 3:** Hapus gambar latar `hero-render.webp` dari hero (tidak lagi dipakai); biarkan file di repo.
- [ ] **Step 4:** Build dan jalankan harness phase 3 di 320/375/1024 — Expected: `[]` termasuk `giant-type`, `photo-min-size`, `photo-sharp`, `hero-ctas`, `hero-quick-links`, `hero-stats-exact`, `tagline-once`.

### Task 4: Proyek — panel bernomor selang-seling

**Files:**
- Modify: `index.html` (section `<!-- 2. Proyek unggulan -->`), `assets/src/input.css`

**Interfaces:**
- Consumes: `.sec-dark/.sec-paper`, `.display`, `.dot` dari Task 2.
- Produces: tiap `<article class="case" data-project="…">` dibungkus section penuh lebar bergantian `sec-dark`/`sec-paper` (pharmacy3d gelap, scentdna krem, n8n gelap, roblox krem); berisi nomor `.case-no` (`01`–`04`), judul `.display` ("Pharmacy 3D."), isi 4 sub-heading yang sama; daftar `.project-list` tetap 8 baris, gaya baris besar.

- [ ] **Step 1:** Bungkus ulang empat case tanpa mengubah teks, tautan, media (video n8n, `poster`, `controls`, `muted`, `playsinline`), dan catatan "Demo privat".
- [ ] **Step 2:** Gaya panel: judul raksasa, media lebar penuh `.case-media`, kolom teks 2 kolom ≥ 768 px; hapus bingkai kartu.
- [ ] **Step 3:** Build; harness phase 4 — Expected: `[]` termasuk `four-featured`, `case-sections`, `list-count`, `n8n-*`, `live-links`, `section-alternation`, `contrast-ok`.

### Task 5: Kenapa Farmasi, Layanan, Kontak

**Files:**
- Modify: `index.html` (section `<!-- 3. -->`, `<!-- 4. -->`, `<!-- 5. -->`, footer), `assets/src/input.css`

**Interfaces:**
- Produces: `#about.sec-paper` dengan `.statement` (kalimat besar, kata dipecah `<span class="w" style="--p:N">` oleh skrip kecil, `data-words`), `<img class="photo-about" src="ulul-foto-lg.webp">` `position: sticky; top: 15vh`, `.skill-group` ×5; `#services.sec-dark` dengan 4 `.service` bernomor besar dan `ol.process`; `#contact.sec-paper` dengan judul raksasa "Ayo ngobrol." dan kartu kontak yang sama.

- [ ] **Step 1:** Markup tiga section; teks kalimat farmasi sama dengan sekarang ("Paham apoteknya, makanya sistemnya masuk akal." + paragraf), tidak diubah.
- [ ] **Step 2:** Skrip ≤ 15 baris: pecah `.statement` jadi `.w` dan set `--p` (0-70) berurutan; tanpa JS teks tetap utuh.
- [ ] **Step 3:** Build; harness phase 5 — Expected: `[]` termasuk `skills-grouped`, `services-four`, `contact-links`, `reveal-words`, `photo-min-size` (about), `nav-matches-sections`.

### Task 6: Gerakan (scroll-driven) dan fallback

**Files:**
- Modify: `assets/src/input.css`

**Interfaces:**
- Consumes: `.hero-giant`, `.photo-hero`, `.photo-about`, `.statement .w` dari Task 3 dan 5.

- [ ] **Step 1:** Di dalam `@supports (animation-timeline: view())` dan `@media (prefers-reduced-motion: no-preference)`: (a) `.hero-giant` geser/skala halus `animation-timeline: scroll()`; (b) `.photo-hero` mengecil + memudar saat keluar (`animation-range: exit 0% exit 70%`); (c) `.photo-about` skala 0,7 → 1 + opacity saat masuk (`entry 0% entry 60%`); (d) `.statement .w` abu → terang memakai `view-timeline` pada `.statement` dan `animation-range: calc(var(--p) * 1%) calc(var(--p) * 1% + 25%)`.
- [ ] **Step 2:** Pastikan tanpa blok `@supports`/dengan reduced-motion, semua elemen di atas tampil penuh (opacity 1, ukuran penuh).
- [ ] **Step 3:** Build; verifikasi di browser pane (scroll dan screenshot hero, transisi, about) dan harness phase 6 — Expected: `[]`. Uji fallback dengan menonaktifkan blok lewat devtools/`CSS.supports` override dan memaksa `prefers-reduced-motion` bila bisa; catat bila tidak bisa dipaksa.

### Task 7: Verifikasi akhir dan commit

**Files:**
- Modify: —

- [ ] **Step 1:** Harness penuh `run(8)` di 320, 375, 768, 1024 — Expected: `[]` di semua.
- [ ] **Step 2:** Cek 7 tautan eksternal (`curl` 200), tautan lokal (CV, PPT, video), konsol tanpa error, bobot halaman (target < 1 MB di luar video; foto besar ≤ 120 KB).
- [ ] **Step 3:** Screenshot hero, satu case, about, kontak di 375 dan 1024 px; periksa foto tidak < 260 px dan wajah utuh.
- [ ] **Step 4:** Commit di branch `restyle` setelah Ulul melihat hasilnya; merge ke `main` hanya atas aba-aba Ulul.
