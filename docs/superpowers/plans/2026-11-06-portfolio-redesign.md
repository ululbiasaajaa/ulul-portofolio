# Portfolio Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ubah `index.html` menjadi satu halaman 5 blok yang melayani recruiter dan klien freelance, tanpa bug layout dan tanpa efek dekoratif berlebihan.

**Architecture:** Tetap statis (`index.html` + aset). Konten unggulan jadi `<article class="case">` inline; proyek lain jadi daftar ringkas yang membuka modal yang sudah ada. Tailwind CDN diganti satu berkas CSS hasil build di akhir, setelah semua class final.

**Tech Stack:** HTML, Tailwind CSS 3.4 (CLI via `npx`), vanilla JS, Python + Pillow (konversi gambar), `npx remotion ffmpeg` (kompres video), `python -m http.server` untuk verifikasi.

**Spec:** `docs/superpowers/specs/2026-11-06-portfolio-redesign-design.md`

## Global Constraints

- Tetap statis; tanpa framework, tanpa backend. `penyihir-tangan/` tidak disentuh.
- Dark dan light mode keduanya harus terbaca. Hero selalu memakai palet gelap.
- Satu warna aksen utama (teal). Tanpa warna per-kartu. Tanpa emoji; pakai ikon SVG inline.
- Dibuang: `.glow-blob`, grain (`body::before`), `.project-card` tilt/sheen, `.grad-text`, `.hero-float`.
- Hero stat persis: **12 proyek**, **25 ribu+ baris TypeScript**, **40 modul**.
- Tagline "From molecules to meaningful code" muncul sekali (hero); dihapus dari footer.
- Copy: pendek, spesifik, tanpa kata "passion". Fakta proyek hanya dari modal yang sudah ada.
- n8n: tanpa tombol "Coba live"; pakai video + label "Demo privat (butuh login)".
- Roblox: screenshot saja (tanpa potongan Luau, Ulul tidak punya tambahan).
- PodLearn tetap di daftar ringkas, bukan unggulan.
- Tidak ada URL instance, email, atau data pribadi di media n8n.

## Review Focus

1. JS gagal/dimatikan: `.reveal` berstatus `opacity: 0` → konten tak terlihat. Harapan: konten tetap terlihat tanpa JS.
2. Video autoplay diblokir (data saver, iOS low power, reduced motion). Harapan: poster tampil dan ada kontrol play.
3. Layar 320px: nama proyek panjang, baris daftar, dan tombol hero tidak meluap atau terpotong.
4. Gambar gagal dimuat: layout tidak loncat dan alt text terbaca (width/height terisi).
5. Light mode: kontras teks sekunder pada kartu dan daftar ≥ 4.5:1.

---

## File Structure

- Modify: `index.html` (semua blok)
- Create: `tests/page-checks.js` (kumpulan assertion DOM yang dijalankan di browser)
- Create: `assets/src/input.css`, `tailwind.config.js`, `assets/site.css` (hasil build), `favicon.svg`, `og-image.jpg`
- Create: `assets/` WebP hasil konversi (`hero-render.webp`, `struktur-kimia.webp`, `project*.webp`), `n8n-demo.mp4`
- Create: `tools/optimize-assets.py` (konversi gambar, idempotent)

## Cara verifikasi (dipakai semua task)

Jalankan server: `python -m http.server 8080` di root repo (background), buka `http://localhost:8080/` di browser pane (file:// tidak memuat aset). Jalankan assertion: isi `tests/page-checks.js` dieksekusi lewat `javascript_tool`; hasil `window.runPageChecks()` berupa array pesan gagal, **kosong = lulus**.

---

### Task 1: Branch, harness pengecekan, dan optimasi aset

**Files:**
- Create: `tests/page-checks.js`, `tools/optimize-assets.py`, `n8n-demo.mp4`
- Modify: —

**Interfaces:**
- Produces: `window.runPageChecks(): string[]` — daftar kegagalan; tiap task berikutnya menambah satu `check()` untuk fiturnya. `tools/optimize-assets.py` menulis `*.webp` di samping sumber dan tidak menimpa file lama.

- [ ] **Step 1: Buat branch** — `git checkout -b redesign` (perubahan Roblox yang belum di-commit ikut terbawa).
- [ ] **Step 2: Tulis `tests/page-checks.js`** dengan helper `check(name, fn)` dan tiga assertion awal: `no-horizontal-overflow` (`scrollWidth <= clientWidth` di lebar saat ini), `hero-heading-readable` (luminance `getComputedStyle(h1).color` > 0.6 di dark dan light), `no-tailwind-cdn` (tidak ada `script[src*="cdn.tailwindcss.com"]`).
- [ ] **Step 3: Jalankan checks pada halaman sekarang** — Expected: gagal pada ketiganya (membuktikan harness menangkap bug asli).
- [ ] **Step 4: Tulis `tools/optimize-assets.py`** — Pillow: `hero-render.png`, `struktur-kimia.png`, `project1-10.jpg` → `.webp` (quality 80, lebar maks 1600); cetak ukuran sebelum/sesudah.
- [ ] **Step 5: Kompres video** — `cd C:\Users\USER\Documents\Remotion-Video && npx --no-install remotion ffmpeg -i public/perkenalan-untuk-upwork/n8n.mp4 -vf scale=1280:-2 -c:v libx264 -crf 28 -preset slow -c:a aac -b:a 96k -movflags +faststart <repo>\n8n-demo.mp4`. Expected: file < 4 MB. Jika ffmpeg ini tidak punya libx264, pakai MP4 asli dan catat sebagai risiko performa.
- [ ] **Step 6: Tonton `n8n-demo.mp4` sampai habis** (browser pane atau pemutar lokal) dan pastikan tidak ada URL instance, email, token, atau data pribadi. Jika ada, hentikan dan minta Ulul memotong/menyensor.
- [ ] **Step 7: Commit** — `git add tests tools *.webp n8n-demo.mp4 && git commit -m "chore: asset optimization and page-check harness"`

### Task 2: Perbaikan bug dan hapus efek dekoratif

**Files:**
- Modify: `index.html` (CSS `:root`, `.hero-section`, `body::before`, `.project-card`, blok `.glow-blob` di body)

**Interfaces:**
- Consumes: `check()` dari Task 1.
- Produces: `.hero-section` mendefinisikan `color: var(--text-primary)` eksplisit (palet gelap); `html { overflow-x: clip }`.

- [ ] **Step 1: Tambah checks** `no-glow-blobs` (`document.querySelectorAll('.glow-blob').length === 0`) dan `no-card-tilt` (tidak ada rule `transform: perspective` pada `.project-card:hover` via `getComputedStyle` setelah hover).
- [ ] **Step 2: Jalankan** — Expected: dua check baru gagal.
- [ ] **Step 3: Hapus** tiga `div.glow-blob`, rule `.glow-blob`, `body::before` (grain), `.project-card::before`/`:hover` tilt, `.grad-text`, `.hero-float`/`@keyframes heroFloat`. Tambah `color: var(--text-primary)` pada `.hero-section` dan `overflow-x: clip` pada `html`.
- [ ] **Step 4: Jalankan checks di 375, 768, 1280 px, dark dan light** — Expected: `[]`.
- [ ] **Step 5: Commit** — `fix: horizontal overflow, hero contrast; remove decorative effects`

### Task 3: Hero baru

**Files:**
- Modify: `index.html` (section hero, navbar)

**Interfaces:**
- Produces: `#hero` dengan `<h1>`, tombol `a[href="#projects"]` dan `a[href^="https://wa.me/"]`, baris tautan kecil (CV, GitHub, email) di `.hero-links`.

- [ ] **Step 1: Tambah checks** `hero-ctas` (ada dua CTA di atas), `hero-quick-links` (tiga `a` di `.hero-links`: `CV_*.pdf` download, `github.com/ululbiasaajaa`, `mailto:sfarmlul@gmail.com`), `hero-stats-exact` (teks stat berisi tepat `12`, `25 ribu+`, `40`), `no-fluff-stats` (tidak ada teks "Bulan Belajar" atau "Problem Solving").
- [ ] **Step 2: Jalankan** — Expected: gagal.
- [ ] **Step 3: Tulis ulang hero** — h1 posisi spesifik (draft dari spec), subteks satu kalimat, dua CTA, `.hero-links`, tiga stat. Hapus chip tagline kanan-bawah jadi satu baris tagline di hero saja. Gambar hero pakai `hero-render.webp` dengan `width`/`height`.
- [ ] **Step 4: Jalankan checks; lihat screenshot 375 dan 1280 px (dark dan light)** — Expected: `[]`, tombol tidak meluap di 320 px.
- [ ] **Step 5: Commit** — `feat: new hero with dual CTA and verifiable stats`

### Task 4: Proyek unggulan (4 case study) dan daftar ringkas

**Files:**
- Modify: `index.html` (section `#projects`, hapus modal `modalPharmacy3D`, `modalN8n`, `modalScentDNA`, `modalRobloxMap`)

**Interfaces:**
- Produces: `<article class="case" data-project="pharmacy3d|scentdna|n8n|roblox">` dengan sub-heading `Masalah`, `Yang dibangun`, `Keputusan teknis`, `Stack`; `<ul class="project-list">` berisi `<li><button data-modal="modalX">` untuk 8 proyek lain, memakai `openModal(id)` yang sudah ada.
- Consumes: `openModal(modalId)` / `closeModal(modalId)` yang sudah ada di `index.html`.

- [ ] **Step 1: Tambah checks** `four-featured` (4 `.case` dengan urutan data-project di atas), `case-sections` (tiap `.case` memiliki empat sub-heading), `list-count` (`.project-list li` = 8), `n8n-no-live-link` (case n8n tanpa `a` bertuliskan "live"/"demo" ke URL eksternal, ada teks "Demo privat"), `n8n-video` (`video[src$="n8n-demo.mp4"][poster][controls][muted][playsinline]`, tanpa `autoplay` bersuara), `pharmacy-links` (link live dan GitHub ada), `scentdna-live-link` (`scentdna-5646.vercel.app`), `list-keyboard` (tiap item daftar adalah `button`), `modal-ids-resolve` (semua `data-modal` menunjuk elemen yang ada).
- [ ] **Step 2: Jalankan** — Expected: gagal.
- [ ] **Step 3: Implementasi** — isi case dari modal lama (lihat tabel di spec). Gambar `loading="lazy"` kecuali yang pertama, dengan `width`/`height`. Delapan proyek lain: SchoolCom, Wedding, LDR, Inventory, PodLearn, Telegram bot, Domain Explorer, dan satu modal `modal1` (cek isinya, sebutkan nama aslinya di daftar).
- [ ] **Step 4: Jalankan checks; klik tiap baris daftar dan tutup modal (Esc dan tombol)** — Expected: `[]`; Esc menutup modal (tambah handler `keydown` jika belum ada).
- [ ] **Step 5: Commit** — `feat: featured case studies and compact project list`

### Task 5: Kenapa farmasi, Layanan, Kontak, footer

**Files:**
- Modify: `index.html` (section `#about`, tambah `#services`, `#contact`, footer, navbar)

**Interfaces:**
- Produces: `#about` (judul bukan lagi "Tentang"), `#services` dengan 4 `.service` dan `ol.process` 4 `li`, kontak berupa `a`.

- [ ] **Step 1: Tambah checks** `skills-grouped` (5 grup: Frontend, Backend, AI, Game/Lua, Infra), `services-four` (4 `.service`, 4 langkah `ol.process li`), `contact-links` (email `mailto:`, GitHub `https://github.com/ululbiasaajaa`, WhatsApp, CV, PPT semuanya `a`), `footer-no-duplicate-tagline`, `nav-matches-sections` (tiap `nav a[href^="#"]` menunjuk id yang ada).
- [ ] **Step 2: Jalankan** — Expected: gagal.
- [ ] **Step 3: Implementasi** — copy singkat bernada Ulul (draft; ditandai untuk diedit). Tombol WhatsApp pakai warna aksen situs. Pertahankan kartu "℞ Contact Label". Hapus `struktur-kimia` dari About jika versi WebP masih >200 KB.
- [ ] **Step 4: Jalankan checks, 375 dan 1280 px** — Expected: `[]`.
- [ ] **Step 5: Commit** — `feat: pharmacy angle, services block, linked contact`

### Task 6: Animasi minimal dan aksesibilitas gerak

**Files:**
- Modify: `index.html` (CSS `.reveal`, script reveal, canvas molekul)

**Interfaces:**
- Produces: `.reveal` hanya aktif bila `html.js` ada; canvas molekul dipindah ke dalam `#hero` dan hanya jalan saat hero terlihat.

- [ ] **Step 1: Tambah checks** `reveal-visible-without-js` (dengan class `js` dihapus dari `<html>`, semua `.reveal` punya `opacity` 1), `canvas-in-hero-only` (`#molecule-canvas` anak dari `#hero`), `reduced-motion` (dengan `matchMedia` dipaksa reduce: canvas `display: none`, video tanpa `autoplay`).
- [ ] **Step 2: Jalankan** — Expected: gagal.
- [ ] **Step 3: Implementasi** — `document.documentElement.classList.add('js')` di `<head>`; CSS `.js .reveal {opacity:0 …}`. Kurangi jumlah node dan opasitas canvas; `IntersectionObserver` menghentikan `requestAnimationFrame` saat hero keluar layar.
- [ ] **Step 4: Jalankan checks** — Expected: `[]`.
- [ ] **Step 5: Commit** — `fix: content visible without JS; hero-only subtle canvas`

### Task 7: SEO, favicon, dan ganti Tailwind CDN ke CSS build

**Files:**
- Create: `tailwind.config.js`, `assets/src/input.css`, `assets/site.css`, `favicon.svg`, `og-image.jpg`
- Modify: `index.html` (`<head>`, tag `<link>`)

**Interfaces:**
- Consumes: semua class final dari Task 2-6 (build dijalankan terakhir agar tidak ada class yang terbuang).
- Produces: `assets/site.css` (minified) dan `<title>`, `meta[name=description]`, `meta[property^="og:"]` (title, description, image, type, url), `link[rel=icon]`.

- [ ] **Step 1: Tambah checks** `meta-complete` (description 50-160 karakter; og:title/description/image ada), `favicon`, `title-specific` (bukan "Web & App Developer Portfolio" generik; menyebut Farmasi atau spesialisasi), `no-tailwind-cdn` (dari Task 1), `images-sized` (semua `img` punya `width` dan `height`), `image-weight` (tak ada resource gambar >300 KB lewat `performance.getEntriesByType('resource')`).
- [ ] **Step 2: Jalankan** — Expected: gagal.
- [ ] **Step 3: Buat `tailwind.config.js`** (`content: ['./index.html']`, `darkMode` mengikuti `[data-theme]` hanya jika dipakai, token warna dari `:root`) dan `assets/src/input.css` (`@tailwind base/components/utilities` + CSS kustom dari `<style>`). Build: `npx tailwindcss@3.4.17 -i assets/src/input.css -o assets/site.css --minify`. Ganti `<script src=cdn.tailwindcss.com>` dengan `<link rel="stylesheet" href="assets/site.css">`.
- [ ] **Step 4: Buat `favicon.svg`** (monogram "UA" dengan warna teal) dan `og-image.jpg` 1200×630 dari `hero-render.webp` (Pillow), tambah meta.
- [ ] **Step 5: Verifikasi visual** — bandingkan screenshot sebelum/sesudah build di 375 dan 1280 px, dark dan light; tidak boleh ada perbedaan layout. Jalankan seluruh `runPageChecks()` — Expected: `[]`. Cek konsol: tanpa error/warning.
- [ ] **Step 6: Commit** — `feat: static CSS build, SEO meta, favicon, OG image`

### Task 8: Verifikasi akhir

**Files:**
- Modify: —

- [ ] **Step 1: Jalankan `runPageChecks()` di 320, 375, 768, 1280 px, dark dan light** — Expected: `[]` di semua kombinasi.
- [ ] **Step 2: Klik semua link eksternal** (Pharmacy live+GitHub, ScentDNA, SchoolCom, LDR, WhatsApp) dan pastikan tidak 404; unduh CV dan PPT.
- [ ] **Step 3: Cek bobot** — total transfer halaman saat load pertama (`performance` API) tercatat; target < 2 MB di luar video.
- [ ] **Step 4: Minta Ulul membaca copy** (hero, About, Layanan) dan mengedit sebelum rilis.
- [ ] **Step 5: Merge ke `main`** hanya setelah Ulul menyetujui; commit gabungan sesuai keinginan Ulul.
