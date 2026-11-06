# Redesign Portfolio — Muhammad Ulul Albab

Tanggal: 2026-11-06 · Status: menunggu review · Berkas: `index.html` (single page, tetap statis)

## Tujuan

Satu halaman yang melayani dua audiens sekaligus: **recruiter/perekrut** (cari kerja/magang) dan **klien freelance**.
Keduanya butuh bukti kerja yang jelas dan jalur kontak yang mudah. Bedanya hanya di CTA.

Kriteria berhasil:
- Orang paham dalam 10 detik: siapa Ulul, apa spesialisasinya, dan cara menghubunginya.
- Tidak terlihat seperti template AI: efek dekoratif minimal, copy spesifik, klaim bisa dibuktikan.
- Tidak ada bug layout (tanpa scroll horizontal, teks terbaca di dark dan light mode).

## Bug yang harus beres lebih dulu

1. **Scroll horizontal / celah kanan.** `glow-blob` (`index.html` sekitar baris 414-416) meluap dari viewport. Blob dibuang; sebagai pengaman, `overflow-x: clip` di `html`/`body`.
2. **Heading hero gelap di light mode.** `h1` dan angka stat mewarisi `color` dari `body`, bukan dari `.hero-section`. Set `color` eksplisit di `.hero-section` supaya hero selalu memakai palet gelap.

## Struktur halaman (5 blok)

### 1. Hero
- Satu kalimat posisi yang spesifik (draft, diedit Ulul): "Mahasiswa farmasi yang membangun software untuk dunia farmasi dan pendidikan."
- Dua tombol utama: **Lihat proyek** dan **Chat WhatsApp**.
- Baris kecil di bawahnya: Download CV, GitHub, email (semuanya link).
- Stat diganti fakta yang bisa dicek: **12 proyek**, **25 ribu+ baris TypeScript** (Pharmacy 3D), **40 modul** (SchoolCom). Stat "2+ bulan belajar" dan "100% problem solving" dibuang.
- Tagline "From molecules to meaningful code" tampil sekali saja (hero), dihapus dari footer.

### 2. Proyek unggulan (4 case study)
Urutan: Pharmacy 3D Simulator, ScentDNA, n8n Automation Suite, Roblox City Map.
Tiap case study: screenshot lebar (bukan crop 144px), lalu **Masalah**, **Yang dibangun**, **Keputusan teknis**, **Stack**, dan link live/repo bila ada. Isinya diambil dari modal yang sudah ada, tidak mengarang fakta baru:

| Proyek | Keputusan teknis yang disorot (dari modal) |
|---|---|
| Pharmacy 3D Simulator | Stok per batch dengan FEFO, wizard resep 5 langkah, simpan 3 slot (IndexedDB), 25rb+ baris TS dan diuji otomatis |
| ScentDNA | Pencarian vektor pgvector (cosine), RAG Gemini, singleton FastAPI `lifespan` untuk mencegah model HuggingFace dobel di RAM, tuning OOM di Docker |
| n8n Automation Suite | Self-hosted di Google Cloud VM dengan HTTPS, tiga workflow (content idea, job matcher skor 0-100, asisten Gmail/Calendar/Tasks via Telegram) |
| Roblox City Map | Environment building di Roblox Studio, scripting Luau untuk HUD status pemain (uang, energi, lapar), dibuat sendiri oleh Ulul |

Proyek lain (SchoolCom, Wedding, LDR, Inventory, Telegram bot, Domain Explorer, dll.) masuk **daftar ringkas**: satu baris per proyek berisi nama, kategori, stack, dan link. Klik membuka modal yang sudah ada.
PodLearn dikecualikan dulu (server sedang migrasi); nanti dipromosikan jadi unggulan kelima.

### 3. Kenapa farmasi (pengganti "Tentang")
- Inti: latar farmasi adalah pembeda. Contoh klaim yang dibuktikan proyek: FEFO, resep, racikan di Pharmacy 3D.
- Foto profil dipertahankan; panel `struktur-kimia.png` (3,8 MB) diganti versi ringan atau dibuang.
- Skill dikelompokkan (Frontend, Backend, AI, Game/Lua, Infra), bukan chip warna-warni.

### 4. Layanan (blok baru, untuk klien)
Tiga sampai empat penawaran singkat, lalu alur 4 langkah (brief, prototipe, build & revisi, rilis):
- Web & landing page (React/Tailwind, Laravel)
- Aplikasi mobile (React Native/Expo)
- Otomatisasi & AI (n8n, Gemini/RAG, bot Telegram)
- Game/map Roblox (Luau)
Blok pendek, tidak ada harga. Recruiter bisa melewatinya tanpa terganggu.

### 5. Kontak
- Email dan GitHub dijadikan link.
- Kartu "℞ Contact Label" dipertahankan (satu-satunya elemen dekoratif yang punya karakter).
- Tombol WhatsApp memakai palet situs, bukan hijau pekat tersendiri. CV dan PPT tetap bisa diunduh.

## Visual

- **Dipertahankan:** foto hero, tema dark/light, tipografi Lora + Inter + JetBrains Mono.
- **Satu signature saja:** canvas jaringan molekul, versi halus dan hanya di hero. Dimatikan saat `prefers-reduced-motion`.
- **Dibuang:** glow blob, grain, tilt 3D kartu, sheen sweep, gradient text, animasi float.
- **Warna:** satu sistem (teal sebagai aksen utama; amber/violet dipakai hemat). Warna per kartu (cyan, biru, rose, dll.) dihapus. Emoji diganti ikon SVG.
- **Kode:** class `.font-mono` (kini Lora) dinamai ulang agar tidak menyesatkan.

## Teknis

- Tailwind CDN diganti CSS build statis (output satu berkas CSS), supaya tidak ada warning produksi dan lebih cepat.
- Gambar berat dijadikan WebP (`struktur-kimia.png` 3,8 MB, `hero-render.png` 2 MB). `width`/`height` diisi agar layout tidak loncat.
- Tambah `meta description`, Open Graph (judul, deskripsi, gambar), favicon, dan `<title>` yang lebih spesifik.
- Tetap statis: `index.html` + aset; cara deploy tidak berubah. Halaman `penyihir-tangan/` tidak disentuh.

## Copy

Draft ditulis dengan nada Ulul sendiri: pendek, spesifik, tanpa kata "passion". Klaim hanya yang bisa dibuktikan proyek. Ulul mengedit sebelum rilis.

## Di luar cakupan

PodLearn sebagai unggulan (menunggu migrasi server), halaman terpisah per proyek, blog, CMS, dan multi-bahasa.

## Keputusan dari Ulul

- **Roblox:** HUD (uang, energi, lapar) diskrip sendiri oleh Ulul. Klaim "scripting Luau" aman dipakai.
- **ScentDNA:** link live sudah ada (`scentdna-5646.vercel.app`, sudah terpasang di kartu).
- **Pharmacy 3D:** link live dan repo GitHub sudah ada.
- **n8n:** tidak punya demo publik karena aplikasinya butuh login. Case study memakai pengganti demo (lihat di bawah), bukan tombol "Coba live".

### Pengganti demo untuk n8n
- Screenshot canvas workflow (`project8.jpg`) ditampilkan besar sebagai bukti utama.
- Label jujur di tempat tombol demo: "Demo privat (butuh login). Bisa diperagakan lewat call." dengan tombol WhatsApp.
- Opsional, jika Ulul mau: rekaman layar singkat atau GIF satu workflow berjalan (misalnya notifikasi job matcher masuk Telegram), karena itu bukti yang paling meyakinkan tanpa membuka akses.
- Jangan menampilkan URL instance, kredensial, atau data pribadi (email, job, kalender) di screenshot. Cek `project8.jpg` sebelum rilis.

### Roblox
- Tidak ada link game; case study menampilkan screenshot saja (tanpa potongan Luau; Ulul tidak punya tambahan).
- Jika map ada di Roblox sebagai game publik, tambahkan link; kalau tidak, biarkan tanpa tombol live.

## Pertanyaan terbuka

Tidak ada. Jawaban Ulul (2026-11-06): angka hero benar; Roblox tidak ada tambahan (jadi tanpa potongan Luau, screenshot saja); n8n memakai video `n8n.mp4` (16,9 dtk, 1080p, 12 MB) yang dikompres untuk web.

## Catatan proses

Berkas ini sengaja belum di-commit; Ulul ingin commit digabung setelah redesign selesai. Perubahan Roblox (kartu, modal, `project10.jpg`) sudah ada di working tree dan belum di-commit.
