from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
from PIL import Image

UP = "/mnt/user-data/uploads/"
IMG = {
    "clinical": "project1.jpg",
    "podlearn": "project2.jpg",
    "cloudinv": "project3.jpg",
    "scentdna": "project4.jpg",
    "lume":     "project5.jpg",
    "ldr":      "project6.jpg",
    "schoolcom":"project7.jpg",
    "profile":  "profile_circle.png",
}

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]

BG          = RGBColor(0xFB, 0xF8, 0xF3)
CARD_BG     = RGBColor(0xFF, 0xFF, 0xFF)
TEXT_DARK   = RGBColor(0x33, 0x2F, 0x2B)
TEXT_MUTED  = RGBColor(0x8A, 0x84, 0x7C)

ROSE   = RGBColor(0xC4, 0x74, 0x8C); ROSE_BG = RGBColor(0xFB, 0xE9, 0xED)
SAGE   = RGBColor(0x5B, 0x8A, 0x72); SAGE_BG = RGBColor(0xE6, 0xF0, 0xE8)
LAV    = RGBColor(0x7C, 0x6D, 0xA8); LAV_BG  = RGBColor(0xEC, 0xE7, 0xF6)
TERRA  = RGBColor(0xC1, 0x7A, 0x4A); TERRA_BG= RGBColor(0xFB, 0xEC, 0xDF)
TEAL   = RGBColor(0x3F, 0x8B, 0x8C); TEAL_BG = RGBColor(0xE3, 0xF1, 0xEF)

FONT = "Arial"

def set_bg(slide, color=BG):
    f = slide.background.fill
    f.solid(); f.fore_color.rgb = color

def add_shadow(shape, blur=Inches(0.14), dist=Inches(0.05), alpha=18):
    sp = shape._element.spPr
    effectLst = sp.makeelement(qn('a:effectLst'), {})
    shadow = sp.makeelement(qn('a:outerShdw'), {
        'blurRad': str(blur), 'dist': str(dist), 'dir': '5400000', 'rotWithShape': '0'
    })
    clr = sp.makeelement(qn('a:srgbClr'), {'val': '4A4038'})
    alpha_el = sp.makeelement(qn('a:alpha'), {'val': str(alpha*1000)})
    clr.append(alpha_el); shadow.append(clr); effectLst.append(shadow)
    sp.append(effectLst)

def card(slide, x, y, w, h, fill=CARD_BG, radius=0.06, shadow=True):
    c = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    c.fill.solid(); c.fill.fore_color.rgb = fill
    c.line.fill.background()
    c.adjustments[0] = radius
    if shadow: add_shadow(c)
    c.text_frame.margin_left = Inches(0.35); c.text_frame.margin_right = Inches(0.35)
    c.text_frame.margin_top = Inches(0.3)
    c.text_frame.vertical_anchor = MSO_ANCHOR.TOP
    return c

def icon_chip(slide, x, y, symbol, color, size=0.6):
    chip = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x), Inches(y), Inches(size), Inches(size))
    chip.fill.solid(); chip.fill.fore_color.rgb = color
    chip.line.fill.background()
    tf = chip.text_frame
    tf.margin_left=0; tf.margin_right=0; tf.margin_top=0; tf.margin_bottom=0
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.text = symbol; p.alignment = PP_ALIGN.CENTER
    p.font.size = Pt(18); p.font.color.rgb = RGBColor(0xFF,0xFF,0xFF)
    return chip

def header(slide, title_text, eyebrow, color=ROSE):
    tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.55), Inches(11.7), Inches(1.15))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = eyebrow.upper(); p.font.size = Pt(11); p.font.bold = True
    p.font.color.rgb = color; p.font.name = FONT
    p2 = tf.add_paragraph()
    p2.text = title_text; p2.font.size = Pt(27); p2.font.bold = True
    p2.font.color.rgb = TEXT_DARK; p2.font.name = FONT; p2.space_before = Pt(2)

def fit_image(path, box_w, box_h):
    im = Image.open(path); iw, ih = im.size; ratio = iw/ih
    if box_w/box_h > ratio:
        h = box_h; w = h*ratio
    else:
        w = box_w; h = w/ratio
    return w, h

def place_image_framed(slide, path, x, y, box_w, box_h, pad=0.12, border=True):
    """White frame card with image fit centered inside, subtle shadow + thin border."""
    w, h = fit_image(path, box_w - 2*pad, box_h - 2*pad)
    frame_w, frame_h = w + 2*pad, h + 2*pad
    fx = x + (box_w - frame_w)/2
    fy = y + (box_h - frame_h)/2
    frame = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(fx), Inches(fy), Inches(frame_w), Inches(frame_h))
    frame.fill.solid(); frame.fill.fore_color.rgb = CARD_BG
    frame.line.fill.background()
    frame.adjustments[0] = 0.04
    add_shadow(frame, blur=Inches(0.12), dist=Inches(0.04), alpha=22)
    pic = slide.shapes.add_picture(path, Inches(fx+pad), Inches(fy+pad), width=Inches(w), height=Inches(h))
    return frame, pic

def place_image_plain(slide, path, x, y, box_w, box_h, border_color=None):
    """Just the picture, fit inside box, centered, no frame card (for compact thumbnails)."""
    w, h = fit_image(path, box_w, box_h)
    px = x + (box_w - w)/2
    py = y + (box_h - h)/2
    pic = slide.shapes.add_picture(path, Inches(px), Inches(py), width=Inches(w), height=Inches(h))
    if border_color:
        pic.line.color.rgb = border_color
        pic.line.width = Pt(1)
    add_shadow(pic, blur=Inches(0.08), dist=Inches(0.03), alpha=20)
    return pic

# ============================================================
# SLIDE 1 — COVER
# ============================================================
s = prs.slides.add_slide(BLANK); set_bg(s)

blob = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(8.6), Inches(-2.2), Inches(7.2), Inches(7.2))
blob.fill.solid(); blob.fill.fore_color.rgb = ROSE_BG; blob.line.fill.background()
sp = blob._element; sp.getparent().remove(sp); s.shapes._spTree.insert(2, sp)

blob2 = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(10.8), Inches(3.5), Inches(4), Inches(4))
blob2.fill.solid(); blob2.fill.fore_color.rgb = SAGE_BG; blob2.line.fill.background()
sp2 = blob2._element; sp2.getparent().remove(sp2); s.shapes._spTree.insert(3, sp2)

# profile photo, circular, sitting on top of the blobs
photo_d = 3.3
s.shapes.add_picture(IMG["profile"], Inches(9.85), Inches(1.55), width=Inches(photo_d), height=Inches(photo_d))

tb = s.shapes.add_textbox(Inches(1.0), Inches(2.5), Inches(8.6), Inches(3.3))
tf = tb.text_frame; tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "AVAILABLE FOR FREELANCE & COLLABORATION"
p.font.size = Pt(12); p.font.bold = True; p.font.color.rgb = ROSE; p.font.name = FONT
p2 = tf.add_paragraph()
p2.text = "Muhammad Ulul Albab"
p2.font.size = Pt(48); p2.font.bold = True; p2.font.color.rgb = TEXT_DARK; p2.font.name = FONT
p2.space_before = Pt(10)
p3 = tf.add_paragraph()
p3.text = "Fullstack & AI Application Developer"
p3.font.size = Pt(22); p3.font.color.rgb = TEXT_MUTED; p3.font.name = FONT
p3.space_before = Pt(4)
p4 = tf.add_paragraph()
p4.text = "Perpaduan ketelitian analisis farmasi & rekayasa perangkat lunak modern"
p4.font.size = Pt(14); p4.font.italic = True; p4.font.color.rgb = SAGE; p4.font.name = FONT
p4.space_before = Pt(14)

# ============================================================
# SLIDE 2 — ABOUT ME
# ============================================================
s = prs.slides.add_slide(BLANK); set_bg(s)
header(s, "Tentang Saya & Latar Belakang Analitis", "Profil Profesional", ROSE)

card(s, 0.8, 1.9, 5.6, 4.7, ROSE_BG)
icon_chip(s, 1.1, 2.2, "\u2697", ROSE)
tb1 = s.shapes.add_textbox(Inches(1.9), Inches(2.15), Inches(4.2), Inches(0.7))
tf1 = tb1.text_frame; tf1.word_wrap = True
p = tf1.paragraphs[0]
p.text = "Pendidikan & Fondasi Eksakta"
p.font.bold = True; p.font.size = Pt(16); p.font.color.rgb = TEXT_DARK; p.font.name = FONT

body1 = s.shapes.add_textbox(Inches(1.15), Inches(3.05), Inches(4.9), Inches(3.3))
tfb1 = body1.text_frame; tfb1.word_wrap = True
p = tfb1.paragraphs[0]
p.text = "Universitas Pakuan — Program Studi Farmasi"
p.font.size = Pt(13); p.font.bold = True; p.font.color.rgb = ROSE; p.font.name = FONT
p2 = tfb1.add_paragraph()
p2.text = "Latar belakang Farmasi membentuk ketelitian tinggi, logika eksploratif, serta pola pikir analitis eksakta yang kuat dalam memecahkan masalah kompleks."
p2.font.size = Pt(13); p2.font.color.rgb = TEXT_MUTED; p2.font.name = FONT
p2.space_before = Pt(10)

card(s, 6.9, 1.9, 5.6, 4.7, SAGE_BG)
icon_chip(s, 7.2, 2.2, "\u2699", SAGE)
tb2 = s.shapes.add_textbox(Inches(8.0), Inches(2.15), Inches(4.2), Inches(0.7))
tf2 = tb2.text_frame; tf2.word_wrap = True
p = tf2.paragraphs[0]
p.text = "Transisi ke Software Engineering"
p.font.bold = True; p.font.size = Pt(16); p.font.color.rgb = TEXT_DARK; p.font.name = FONT

points = [
    "Fokus pada pembentukan arsitektur sistem yang bersih, efisien, dan siap pakai di lingkungan cloud.",
    "Menguasai pemecahan masalah teknis end-to-end: dari profil memori PyTorch/Docker hingga optimasi database.",
    "Komitmen pada pembelajaran berkelanjutan tanpa ragu menghadapi tantangan teknologi baru.",
]
body2 = s.shapes.add_textbox(Inches(7.25), Inches(3.05), Inches(4.9), Inches(3.3))
tfb2 = body2.text_frame; tfb2.word_wrap = True
first = True
for pt in points:
    p = tfb2.paragraphs[0] if first else tfb2.add_paragraph()
    first = False
    p.text = f"\u2022  {pt}"
    p.font.size = Pt(13); p.font.color.rgb = TEXT_MUTED; p.font.name = FONT
    p.space_after = Pt(10)

# ============================================================
# SLIDE 3 — TECH STACK
# ============================================================
s = prs.slides.add_slide(BLANK); set_bg(s)
header(s, "Keahlian & Ekosistem Teknologi", "Technical Stack", LAV)

stacks = [
    ("\u25A3", "Frontend & Mobile", "React, React Native, Expo SDK 54, Tailwind CSS, Vite, HTML/JS", TEAL, TEAL_BG, 0.8, 2.0),
    ("\u25A2", "Backend & API", "FastAPI (Python), Laravel 11 (PHP), Node.js/Express, Firebase", ROSE, ROSE_BG, 6.9, 2.0),
    ("\u25C8", "AI & Data Intelligence", "Gemini RAG API, PyTorch, SentenceTransformers, pgvector", LAV, LAV_BG, 0.8, 4.5),
    ("\u25C9", "Database & Cloud", "PostgreSQL, MySQL, Firebase Firestore, SQLite, Docker, Vercel", SAGE, SAGE_BG, 6.9, 4.5),
]
for icon, title, desc, color, bgcol, x, y in stacks:
    card(s, x, y, 5.6, 2.15, bgcol)
    icon_chip(s, x+0.3, y+0.3, icon, color)
    tb = s.shapes.add_textbox(Inches(x+1.05), Inches(y+0.22), Inches(4.3), Inches(1.7))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title; p.font.bold = True; p.font.size = Pt(16); p.font.color.rgb = TEXT_DARK; p.font.name = FONT
    p2 = tf.add_paragraph()
    p2.text = desc; p2.font.size = Pt(12.5); p2.font.color.rgb = TEXT_MUTED; p2.font.name = FONT
    p2.space_before = Pt(6)

# ============================================================
# SLIDE 4 — SCHOOLCOM (split: text left, phone mockup right)
# ============================================================
s = prs.slides.add_slide(BLANK); set_bg(s)
header(s, "SchoolCom — School Management & Communication System", "Featured Enterprise & Mobile Project", TEAL)

img_box_w = 3.4
text_w = 11.733 - img_box_w - 0.3
card(s, 0.8, 1.9, text_w, 4.7, TEAL_BG)
icon_chip(s, 1.1, 2.15, "\u2317", TEAL, size=0.55)
tb = s.shapes.add_textbox(Inches(1.85), Inches(2.12), Inches(text_w-1.1), Inches(0.85))
tf = tb.text_frame; tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "Sistem Pengelolaan & Komunikasi Sekolah Terpadu 3 Peran (Android & Web)"
p.font.bold = True; p.font.size = Pt(16); p.font.color.rgb = TEXT_DARK; p.font.name = FONT

body = s.shapes.add_textbox(Inches(1.15), Inches(3.15), Inches(text_w-0.6), Inches(3.3))
tfb = body.text_frame; tfb.word_wrap = True
p = tfb.paragraphs[0]
p.text = "Tech Stack: React Native (Expo SDK 54), Firebase Firestore/Auth, React, Vite, Tailwind CSS v4, Vercel"
p.font.size = Pt(11.5); p.font.bold = True; p.font.color.rgb = TEAL; p.font.name = FONT
p.space_after = Pt(8)
hi = [
    "Role-Based Architecture (RBAC): Tiga antarmuka terpisah khusus untuk Admin Sekolah, Guru Kelas, dan Orang Tua.",
    "Module Auditability: 40 modul teraudit mencakup presensi harian batch, penginputan nilai rapor, & rekapitulasi.",
    "Parent-Child Scoping: Transparansi pemantauan kehadiran dan catatan insiden/perilaku siswa secara aman.",
    "Landing Page & Conversion: Landing page khusus Vercel terintegrasi ke WhatsApp untuk permintaan demo.",
]
for h in hi:
    p = tfb.add_paragraph()
    p.text = f"\u2713  {h}"
    p.font.size = Pt(12); p.font.color.rgb = TEXT_DARK; p.font.name = FONT
    p.space_after = Pt(7)

place_image_framed(s, IMG["schoolcom"], 0.8+text_w+0.3, 1.9, img_box_w, 4.7)

# ============================================================
# SLIDE 5 — SCENTDNA (split: text left, web mockup right)
# ============================================================
s = prs.slides.add_slide(BLANK); set_bg(s)
header(s, "ScentDNA — AI Fragrance Discovery Engine", "Featured AI Project", ROSE)

img_box_w = 4.6
text_w = 11.733 - img_box_w - 0.3
card(s, 0.8, 1.9, text_w, 4.7, ROSE_BG)
icon_chip(s, 1.1, 2.15, "\u2699", ROSE, size=0.55)
tb = s.shapes.add_textbox(Inches(1.85), Inches(2.12), Inches(text_w-1.1), Inches(0.6))
tf = tb.text_frame; tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "Mesin Rekomendasi Aroma Vector Search & RAG AI (Dockerized)"
p.font.bold = True; p.font.size = Pt(16); p.font.color.rgb = TEXT_DARK; p.font.name = FONT

body = s.shapes.add_textbox(Inches(1.15), Inches(2.95), Inches(text_w-0.6), Inches(3.5))
tfb = body.text_frame; tfb.word_wrap = True
p = tfb.paragraphs[0]
p.text = "Tech Stack: FastAPI (Python), PyTorch, SentenceTransformers, pgvector (PostgreSQL), Docker, Gemini 2.5 Flash API"
p.font.size = Pt(11.5); p.font.bold = True; p.font.color.rgb = ROSE; p.font.name = FONT
p.space_after = Pt(8)
hi = [
    "Semantic Vector Search: Menggunakan pembacaan kemiripan kosinus (<=>) berbasis pgvector PostgreSQL.",
    "RAG Gemini Consultant: Rekomendasi kontekstual terstruktur dari hasil pencarian vektor produk.",
    "Singleton Pattern (Dependency Injection): Restrukturisasi lifespan FastAPI untuk hemat alokasi RAM.",
    "Memory Hardening: Optimasi PyTorch CPU single-threading & garbage collection aktif untuk stabilitas cloud deployment.",
]
for h in hi:
    p = tfb.add_paragraph()
    p.text = f"\u2713  {h}"
    p.font.size = Pt(12); p.font.color.rgb = TEXT_DARK; p.font.name = FONT
    p.space_after = Pt(7)

place_image_framed(s, IMG["scentdna"], 0.8+text_w+0.3, 1.9, img_box_w, 4.7)

# ============================================================
# SLIDE 6 — PODLEARN & TELEGRAM (split cards, podlearn has thumbnail)
# ============================================================
s = prs.slides.add_slide(BLANK); set_bg(s)
header(s, "AI Solutions: PodLearn AI & Telegram Assistant", "Featured AI Projects", LAV)

c1 = card(s, 0.8, 1.9, 5.6, 4.7, LAV_BG)
icon_chip(s, 1.1, 2.2, "\u266B", LAV)
tb = s.shapes.add_textbox(Inches(1.9), Inches(2.15), Inches(4.3), Inches(0.6))
tf = tb.text_frame; tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "PodLearn AI — Podcast & Quiz"
p.font.bold = True; p.font.size = Pt(16); p.font.color.rgb = TEXT_DARK; p.font.name = FONT

place_image_plain(s, IMG["podlearn"], 1.15, 2.95, 4.9, 1.55)

body1 = s.shapes.add_textbox(Inches(1.15), Inches(4.65), Inches(4.9), Inches(1.8))
tfb1 = body1.text_frame; tfb1.word_wrap = True
pts = [
    "Integrasi Gemini AI untuk naskah dialog.",
    "Microsoft Edge Neural TTS multi-suara.",
    "FFmpeg Concat untuk penggabungan audio.",
    "Generator 10 kuis evaluasi interaktif.",
]
first = True
for pt in pts:
    p = tfb1.paragraphs[0] if first else tfb1.add_paragraph()
    first = False
    p.text = f"\u2713  {pt}"
    p.font.size = Pt(11.5); p.font.color.rgb = TEXT_DARK; p.font.name = FONT
    p.space_after = Pt(4)

c2 = card(s, 6.9, 1.9, 5.6, 4.7, TEAL_BG)
icon_chip(s, 7.2, 2.2, "\u2708", TEAL)
tb2 = s.shapes.add_textbox(Inches(8.0), Inches(2.15), Inches(4.3), Inches(0.6))
tf2 = tb2.text_frame; tf2.word_wrap = True
p = tf2.paragraphs[0]
p.text = "Telegram AI Assistant (Live 24/7)"
p.font.bold = True; p.font.size = Pt(16); p.font.color.rgb = TEXT_DARK; p.font.name = FONT

body2 = s.shapes.add_textbox(Inches(7.25), Inches(2.95), Inches(4.9), Inches(3.3))
tfb2 = body2.text_frame; tfb2.word_wrap = True
p = tfb2.paragraphs[0]
p.text = "Bot Telegram personal cerdas yang aktif 24/7 di cloud server tanpa henti."
p.font.size = Pt(12); p.font.color.rgb = TEXT_MUTED; p.font.name = FONT
p.space_after = Pt(8)
pts2 = [
    "Model LLM Llama-3.3 70B via Groq API.",
    "Respon cerdas multibahasa real-time.",
    "System prompt kustom untuk persona unik.",
    "Deployed 24/7 di Railway Cloud.",
]
for pt in pts2:
    p = tfb2.add_paragraph()
    p.text = f"\u2713  {pt}"
    p.font.size = Pt(12.5); p.font.color.rgb = TEXT_DARK; p.font.name = FONT
    p.space_after = Pt(6)

# ============================================================
# SLIDE 7 — LDR ANCHOR & CLINICAL SUITE (both have phone thumbnails)
# ============================================================
s = prs.slides.add_slide(BLANK); set_bg(s)
header(s, "Mobile & Web Dashboard Systems", "Functional Systems", TERRA)

card(s, 0.8, 1.9, 5.6, 4.7, TERRA_BG)
icon_chip(s, 1.1, 2.2, "\u2764", TERRA)
tb = s.shapes.add_textbox(Inches(1.9), Inches(2.15), Inches(4.3), Inches(0.6))
tf = tb.text_frame; tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "LDR Anchor (React Native App)"
p.font.bold = True; p.font.size = Pt(16); p.font.color.rgb = TEXT_DARK; p.font.name = FONT

place_image_plain(s, IMG["ldr"], 4.55, 2.95, 1.55, 3.35)

body1 = s.shapes.add_textbox(Inches(1.15), Inches(2.95), Inches(3.15), Inches(3.4))
tfb1 = body1.text_frame; tfb1.word_wrap = True
pts = [
    "Aplikasi mobile Android khusus pasangan jarak jauh (LDR).",
    "Fitur Mood sharing real-time & pelukan virtual interaktif.",
    "Integrasi FCM V1 Push Notification via Expo.",
    "Firebase Firestore & Auth backend integration.",
]
first = True
for pt in pts:
    p = tfb1.paragraphs[0] if first else tfb1.add_paragraph()
    first = False
    p.text = f"\u2713  {pt}"
    p.font.size = Pt(11.5); p.font.color.rgb = TEXT_DARK; p.font.name = FONT
    p.space_after = Pt(8)

card(s, 6.9, 1.9, 5.6, 4.7, SAGE_BG)
icon_chip(s, 7.2, 2.2, "\u2695", SAGE)
tb2 = s.shapes.add_textbox(Inches(8.0), Inches(2.15), Inches(4.3), Inches(0.6))
tf2 = tb2.text_frame; tf2.word_wrap = True
p = tf2.paragraphs[0]
p.text = "Clinical Suite Dashboard"
p.font.bold = True; p.font.size = Pt(16); p.font.color.rgb = TEXT_DARK; p.font.name = FONT

place_image_plain(s, IMG["clinical"], 10.65, 2.95, 1.4, 3.35)

body2 = s.shapes.add_textbox(Inches(7.25), Inches(2.95), Inches(3.15), Inches(3.4))
tfb2 = body2.text_frame; tfb2.word_wrap = True
pts2 = [
    "Sistem rekapitulasi data medis & manajemen klinis.",
    "Kalkulator parameter medis fungsional otomatis.",
    "Antarmuka bersih & presisi tinggi berbasis Tailwind.",
    "Dirancang khusus untuk efisiensi operasional medis.",
]
first = True
for pt in pts2:
    p = tfb2.paragraphs[0] if first else tfb2.add_paragraph()
    first = False
    p.text = f"\u2713  {pt}"
    p.font.size = Pt(11.5); p.font.color.rgb = TEXT_DARK; p.font.name = FONT
    p.space_after = Pt(8)

# ============================================================
# SLIDE 8 — CLOUD INVENTORY (thumbnail) & DOMAIN EXPLORER
# ============================================================
s = prs.slides.add_slide(BLANK); set_bg(s)
header(s, "Enterprise Serverless & Laravel Systems", "Web Applications", SAGE)

card(s, 0.8, 1.9, 5.6, 4.7, SAGE_BG)
icon_chip(s, 1.1, 2.2, "\u2601", SAGE)
tb = s.shapes.add_textbox(Inches(1.9), Inches(2.15), Inches(4.3), Inches(0.6))
tf = tb.text_frame; tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "Cloud Inventory System (Serverless)"
p.font.bold = True; p.font.size = Pt(16); p.font.color.rgb = TEXT_DARK; p.font.name = FONT

place_image_plain(s, IMG["cloudinv"], 1.15, 2.95, 4.9, 1.55)

body1 = s.shapes.add_textbox(Inches(1.15), Inches(4.65), Inches(4.9), Inches(1.8))
tfb1 = body1.text_frame; tfb1.word_wrap = True
pts = [
    "Sistem inventaris berbasis Google Apps Script.",
    "Concurrency Protection via LockService.",
    "Role-Based Access Control (RBAC) & Anti-XSS.",
    "Audit Trail log & snapshot auto-backup ke Drive.",
]
first = True
for pt in pts:
    p = tfb1.paragraphs[0] if first else tfb1.add_paragraph()
    first = False
    p.text = f"\u2713  {pt}"
    p.font.size = Pt(11.5); p.font.color.rgb = TEXT_DARK; p.font.name = FONT
    p.space_after = Pt(4)

card(s, 6.9, 1.9, 5.6, 4.7, TERRA_BG)
icon_chip(s, 7.2, 2.2, "\u2318", TERRA)
tb2 = s.shapes.add_textbox(Inches(8.0), Inches(2.15), Inches(4.3), Inches(0.6))
tf2 = tb2.text_frame; tf2.word_wrap = True
p = tf2.paragraphs[0]
p.text = "Domain Explorer (Laravel 11)"
p.font.bold = True; p.font.size = Pt(16); p.font.color.rgb = TEXT_DARK; p.font.name = FONT

body2 = s.shapes.add_textbox(Inches(7.25), Inches(2.95), Inches(4.9), Inches(3.3))
tfb2 = body2.text_frame; tfb2.word_wrap = True
pts2 = [
    "Aplikasi manajemen domain berbasis Laravel 11.",
    "Arsitektur MVC bersih dengan Blade views.",
    "Penggunaan SQLite database untuk performa ringan.",
    "Database Migrations & Seeders otomatis.",
]
first = True
for pt in pts2:
    p = tfb2.paragraphs[0] if first else tfb2.add_paragraph()
    first = False
    p.text = f"\u2713  {pt}"
    p.font.size = Pt(12.5); p.font.color.rgb = TEXT_DARK; p.font.name = FONT
    p.space_after = Pt(8)

# ============================================================
# SLIDE 9 — LUME (Undangan Digital) — NEW
# ============================================================
s = prs.slides.add_slide(BLANK); set_bg(s)
header(s, "LUME — Wedding Invitation", "Undangan Digital", ROSE)

img_box_w = 3.0
text_w = 11.733 - img_box_w - 0.3
card(s, 0.8, 1.9, text_w, 4.7, ROSE_BG)
icon_chip(s, 1.1, 2.15, "\u2661", ROSE, size=0.55)
tb = s.shapes.add_textbox(Inches(1.85), Inches(2.12), Inches(text_w-1.1), Inches(0.6))
tf = tb.text_frame; tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "Jasa Pembuatan Undangan Digital Pernikahan"
p.font.bold = True; p.font.size = Pt(16); p.font.color.rgb = TEXT_DARK; p.font.name = FONT

body = s.shapes.add_textbox(Inches(1.15), Inches(2.95), Inches(text_w-0.6), Inches(3.5))
tfb = body.text_frame; tfb.word_wrap = True
p = tfb.paragraphs[0]
p.text = "Layanan custom undangan pernikahan digital yang bisa dibagikan lewat link pribadi."
p.font.size = Pt(12); p.font.color.rgb = TEXT_MUTED; p.font.name = FONT
p.space_after = Pt(8)
hi = [
    "Countdown Pernikahan Real-Time: hitung mundur hari, jam, menit, & detik menuju hari-H.",
    "Desain Hero Elegan: foto pasangan dengan overlay gelap & tipografi serif premium.",
    "Custom Nama & Tanggal: setiap undangan dipersonalisasi sesuai identitas pasangan.",
    "Dibagikan via Link Pribadi: mudah disebar lewat WhatsApp maupun media sosial.",
]
for h in hi:
    p = tfb.add_paragraph()
    p.text = f"\u2713  {h}"
    p.font.size = Pt(12.5); p.font.color.rgb = TEXT_DARK; p.font.name = FONT
    p.space_after = Pt(8)

place_image_framed(s, IMG["lume"], 0.8+text_w+0.3, 1.9, img_box_w, 4.7)

# ============================================================
# SLIDE 10 — CONTACT
# ============================================================
s = prs.slides.add_slide(BLANK); set_bg(s)

blob = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(-2.5), Inches(-2.5), Inches(6), Inches(6))
blob.fill.solid(); blob.fill.fore_color.rgb = LAV_BG; blob.line.fill.background()
sp = blob._element; sp.getparent().remove(sp); s.shapes._spTree.insert(2, sp)

c = card(s, 1.9, 1.6, 9.53, 4.4, CARD_BG)
tf = c.text_frame
p = tf.paragraphs[0]
p.text = "Mari Berkolaborasi!"
p.font.bold = True; p.font.size = Pt(30); p.font.color.rgb = ROSE; p.font.name = FONT
p.alignment = PP_ALIGN.CENTER
p2 = tf.add_paragraph()
p2.text = "Terbuka untuk proyek freelance, pengembangan sistem kustom, maupun posisi software engineer."
p2.font.size = Pt(14); p2.font.color.rgb = TEXT_MUTED; p2.font.name = FONT
p2.alignment = PP_ALIGN.CENTER
p2.space_before = Pt(8); p2.space_after = Pt(20)

contacts = [
    "WhatsApp   : +62 895-4147-81707",
    "Email          : ulula2812@gmail.com",
    "Portofolio    : ulul-portofolio-3odd.vercel.app",
    "Lokasi         : Bogor, Jawa Barat, Indonesia",
]
for cline in contacts:
    p = tf.add_paragraph()
    p.text = cline
    p.font.size = Pt(15); p.font.color.rgb = TEXT_DARK; p.font.name = FONT
    p.alignment = PP_ALIGN.CENTER
    p.space_after = Pt(6)

prs.save("Portfolio_Muhammad_Ulul_Albab.pptx")
print("SAVED")