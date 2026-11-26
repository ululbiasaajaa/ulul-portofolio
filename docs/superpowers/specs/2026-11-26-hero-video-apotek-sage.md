# Redesign "Apotek Sage" + hero video — Muhammad Ulul Albab

Tanggal: 2026-11-26 · Referensi gaya: landing page "Parrot" (burung terbang masuk, nama raksasa di belakang kepala) · Dibuat dengan bantuan skill UI/UX Pro Max (Quick Reference §1–§7, pencarian typography/landing).

## Kenapa diganti

Versi "Onda" masih terasa template/AI: hitam-krem-teal, titik teal di ujung semua judul, label "◆ Rx-0n", emoji di modal, dan foto bulat generik. Isi (copy, 4 case study, 8 proyek lain, layanan, kontak) **tetap**; yang diganti bungkus visual dan hero.

## Sistem visual

- **Palet** (token di `assets/src/input.css`): sage `#e4e9da → #b0be98` (hero & About), paper `#f2f1e9` (Proyek, Kontak), forest `#14211a` (Proyek lain, Layanan, footer), aksen pollen `#e8c547` untuk CTA utama (teks di atasnya ink, kontras ±9.9:1). Teks sekunder di sage gelap hanya pakai `--ink-2` (≥4.5:1).
- **Huruf** (self-hosted di `assets/fonts`, OFL): Instrument Serif untuk judul (italic untuk kata penekanan), Geist untuk isi, Geist Mono untuk label. Tidak ada lagi Google Fonts.
- **Ikon**: satu sprite SVG (stroke 1.75) di awal `<body>`, tanpa emoji.
- **Detail farmasi yang asli, bukan dekorasi**: judul "Meracik resep, meracik kode.", kartu kontak bergaya etiket (℞ Etiket kontak), logo kapsul.

## Hero

- Video asli Ulul (jas lab, 2,7 dtk) → background dihapus (Robust Video Matting), warna dinormalkan dari jas lab, despill kuning, lalu ditempel ke gradien sage yang **sama persis** dengan `--stage` di CSS.
- Dua versi: `assets/hero/hero-d.mp4` 1920×1080 (desktop, Ulul di kanan) dan `hero-m.mp4` 1080×1350 (HP/tablet, ditumpuk di atas teks). ±0,5 MB per video.
- Lapisan di `.hero-stage`: poster frame terakhir → video → teks raksasa "ULUL" → `hero-*-cutout.webp` (Ulul saja, transparan). Karena cutout = frame terakhir, nama terlihat "di belakang" kepala.
- Urutan: video main → copy naik (650 ms) → video selesai → cutout + nama muncul → tombol "Putar ulang".
- Tanpa JS / `prefers-reduced-motion` / hemat data: langsung keadaan akhir (poster + cutout + nama), tanpa video.
- Desktop: stage menempel di bawah dengan tinggi `max(100svh, 680px)` supaya ukuran Ulul tidak berubah walau copy memanjang; copy diberi `padding-right` 0,66 × tinggi hero agar tidak menimpa badan.

## Tes

`tests/page-checks.js` diperbarui: check foto bulat diganti `hero-video`, `hero-stills`, `hero-layers-aligned`, `hero-copy-clear-of-person`, `hero-replay-reachable`; ditambah `no-emoji-icons`, `modal-a11y`, `modal-open-close`, `targets-44`, `self-hosted-fonts`. Lulus di 1920×1080, 1440×900, 1280×800, 1024×768, 768×1024, 390×844, 320×640.
