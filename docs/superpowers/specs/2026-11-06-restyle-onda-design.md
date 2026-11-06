# Restyle "Onda-inspired" — Muhammad Ulul Albab

Tanggal: 2026-11-06 · Status: menunggu review · Branch: `restyle` · Referensi: https://8b.com/templates/onda/ (MIT, hanya jadi inspirasi; kode ditulis sendiri)

## Tujuan

Situs terasa kaku. Isi (copy, 4 case study, daftar proyek, layanan, kontak) **tidak berubah**; yang diganti adalah bungkus visual dan gerakannya.

Penyebab kaku (hasil audit): semua section selebar sama dan rata tengah, semuanya navy dengan kartu berbingkai, ukuran tipografi nyaris seragam, dan satu-satunya gerakan adalah fade-up.

Kriteria berhasil:
- Ada kontras ukuran yang jelas (huruf raksasa vs teks biasa) dan kontras warna antar section.
- Foto Ulul besar dan jadi titik fokus halaman.
- Gerakan terbatas pada 3 hal yang punya tujuan; sisanya diam.
- Tidak ada regresi: semua check lama di `tests/page-checks.js` tetap lulus (disesuaikan hanya bila selector memang berubah).

## Keputusan (asumsi Ulul menyetujui; koreksi bila salah)

- **Toggle dark/light dibuang.** Section selang-seling gelap dan krem menggantikannya. Tema tetap satu: near-black + krem + aksen teal.
- **Animasi memakai CSS scroll-driven** (`animation-timeline`), tanpa library. Browser tanpa dukungan (mis. Firefox lama) menampilkan keadaan statis yang tetap terbaca.
- **Foto besar** (aturan baru dari Ulul): lihat bagian Foto.

## Sistem visual

- **Palet:** `--ink #0b0d12` (gelap), `--paper #f3efe6` (krem), `--teal` aksen (fill `#22e6b5` di gelap, `#0e9c78` di krem; teks aksen di krem `#087055` agar kontras ≥ 4,5:1).
- **Tipografi:** judul display raksasa (hero `clamp(5rem, 22vw, 18rem)`; judul section `clamp(2.6rem, 7vw, 6rem)`), berat tebal, rapat. Font: Gabarito atau pasangan serupa dari Google Fonts untuk judul, Inter untuk isi, JetBrains Mono untuk label. (Lora tidak dipakai lagi.) Judul section diakhiri titik aksen teal.
- **Ritme section:** Hero gelap, Proyek gelap/krem bergantian per case study, Kenapa Farmasi krem, Layanan gelap, Kontak krem. Lebar konten tetap `max-w-5xl` untuk teks, tetapi judul dan foto boleh keluar dari kolom.
- **Navigasi:** pil melayang di atas (tanpa toggle tema); di mobile ada tombol menu sederhana yang membuka daftar tautan (sekaligus menutup minor "nav mobile" yang tertunda).
- **Dibuang:** bingkai kartu seragam di luar case study, label "Rx-0n" tetap sebagai label kecil (dipertahankan), kartu layanan diganti daftar bernomor besar.

## Foto (besar)

- Sumber: `Ulul Foto Formal.jpg` (1122×1402). Hasilkan `ulul-foto-lg.webp` lebar 1000 px (cukup untuk 2× pada 500 px).
- **Ukuran minimum:** desktop `clamp(300px, 34vw, 520px)` diameter; mobile minimal `72vw` (≈ 270 px di layar 375 px). Tidak pernah di bawah 260 px di viewport mana pun.
- Bentuk bulat dengan cincin tipis teal dan sedikit orbit titik kecil (satu titik aksen berputar pelan, seperti bola Onda).
- **Perjalanan saat scroll:** di Hero foto besar di sisi kanan, sebagian menimpa huruf raksasa. Saat scroll menuju Proyek foto mengecil sedikit dan memudar keluar (tidak menutupi case study). Di "Kenapa Farmasi" foto muncul lagi besar dan `sticky` di samping kalimat besar sampai section selesai.
- Wajah harus terlihat utuh (`object-position: top`), tanpa terpotong lingkaran.

## Tiga gerakan (semua mati bila `prefers-reduced-motion`)

1. **Huruf raksasa hero** bergeser/skala halus mengikuti scroll.
2. **Foto bulat** berpindah dan berubah ukuran seperti di atas.
3. **Kalimat farmasi menyala kata demi kata** di "Kenapa Farmasi" (abu-abu ke terang mengikuti scroll). Konten yang sama dengan teks sekarang, hanya dipecah per kata.

Selain itu hanya hover sederhana pada tautan dan tombol. Canvas jaringan molekul **dibuang** (diganti huruf raksasa + foto sebagai signature).

## Konten per blok

1. **Hero:** kata raksasa "Halo." (bukan "Hello" agar bernuansa lokal) di bawah kalimat posisi yang sama; CTA, tautan cepat, dan stat tetap.
2. **Proyek unggulan:** 4 panel penuh lebar bergantian gelap/krem, nomor besar (`01`–`04`), judul raksasa ("Pharmacy 3D."), media lebar, lalu Masalah / Yang dibangun / Keputusan teknis / Stack seperti sekarang. Daftar 8 proyek lain tetap, dengan gaya baris besar.
3. **Kenapa Farmasi:** kalimat besar menyala per kata + foto sticky + grup skill.
4. **Layanan:** daftar bernomor besar (01–04) dan 4 langkah proses.
5. **Kontak:** judul raksasa "Ayo ngobrol." (draft copy), kartu "℞ Contact Label" dipertahankan.

## Teknis

- Tetap statis. `assets/src/input.css` dan Tailwind build tetap dipakai; font diperbarui di `<head>`.
- `index.html` dirakit ulang (skrip perakit seperti sebelumnya, di luar repo) dengan modal proyek lain dipertahankan.
- `tests/page-checks.js`: hapus check yang tidak relevan (`canvas-in-hero-only`, tema), tambah `photo-min-size` (foto ≥ 260 px di 320/375/1024 px), `photo-sharp` (naturalWidth ≥ 2× ukuran tampil), `no-theme-toggle`, `mobile-menu`, `section-alternation` (≥ 3 section berganti latar), `reveal-words` (kalimat farmasi terpecah per kata dan tetap terbaca tanpa dukungan scroll-driven).
- Lisensi: karena hanya terinspirasi dan kode ditulis sendiri, tidak ada kewajiban atribusi. Bila ada potongan CSS/JS Onda yang disalin, sertakan pemberitahuan MIT.

## Di luar cakupan

Mengubah copy proyek, menambah halaman, library animasi (GSAP), geser-samping horizontal untuk case study (teksnya terlalu padat), dan PodLearn sebagai unggulan (masih migrasi server).

## Risiko

- Huruf raksasa dan foto besar di layar 320 px bisa meluap; dicek oleh `no-horizontal-overflow` dan `photo-min-size`.
- Font display baru menambah request; pakai `display=swap` dan subset yang dibutuhkan.
- Scroll-driven animation tidak ada di semua browser; fallback statis wajib tampil rapi.
