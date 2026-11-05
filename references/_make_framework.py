# -*- coding: utf-8 -*-
"""Generate the conceptual framework diagram for the literature review.

The layout is checked programmatically: every text block must stay inside its
panel (or the figure canvas) so the exported PNG remains readable when it is
scaled to 15.7 cm width inside the DOCX.
"""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "framework.png"

plt.rcParams["font.family"] = "DejaVu Sans"

FIG_W, FIG_H = 8.2, 10.6
fig, ax = plt.subplots(figsize=(FIG_W, FIG_H), dpi=300)
ax.set_xlim(0, 100)
ax.set_ylim(0, 140)
ax.axis("off")
fig.patch.set_facecolor("white")

NAVY = "#0B2545"
GREY = "#565656"
DARK = "#1F1F1F"

TEXTS = []  # (label, artist, x0, x1, y0, y1) for the fit check


def box(x, y, w, h, face, edge, lw=1.5, radius=0.8):
    p = FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad=0.30,rounding_size={radius}",
        linewidth=lw, edgecolor=edge, facecolor=face, zorder=2,
    )
    ax.add_patch(p)
    return p


def text(label, x, y, s, x0, x1, y0, y1, **kw):
    artist = ax.text(x, y, s, zorder=3, **kw)
    TEXTS.append((label, artist, x0, x1, y0, y1))
    return artist


def layer(x, y, w, h, title, bullets, face, edge):
    box(x, y, w, h, face, edge)
    text(f"layer:{title}", x + w / 2, y + h - 1.1, title,
         x, x + w, y, y + h,
         ha="center", va="top", fontsize=13.2, fontweight="bold", color=NAVY)
    text(f"bullets:{title}", x + 1.25, y + h - 4.6,
         "\n".join("• " + b for b in bullets),
         x, x + w, y, y + h,
         ha="left", va="top", fontsize=11.4, color=DARK, linespacing=1.45)


def down_arrow(x, y1, y2, color="#1F4E79"):
    ax.add_patch(FancyArrowPatch(
        (x, y1), (x, y2),
        arrowstyle="-|>", mutation_scale=18, linewidth=2.0,
        color=color, zorder=4, shrinkA=2, shrinkB=2,
    ))


# ----------------------------------------------------------------------------
# Title
# ----------------------------------------------------------------------------
text("title", 50, 137.6,
     "Kerangka Interoperabilitas Sosio-Teknis Berlapis (KIST)",
     0, 100, 132, 140,
     ha="center", va="top", fontsize=17, fontweight="bold", color=NAVY)
text("subtitle", 50, 133.2,
     "Sintesis 15 artikel (2021–2025) tentang standar, koding, dan implementasi di Indonesia",
     0, 100, 129, 134,
     ha="center", va="top", fontsize=10.2, color=GREY, style="italic")

# ----------------------------------------------------------------------------
# Left context panel
# ----------------------------------------------------------------------------
LX, LW = 1.0, 22.0
box(LX, 31.0, LW, 96.0, "#F7F7F7", "#7F7F7F", lw=1.2)
text("panel:left-title", LX + LW / 2, 125.6, "KONTEKS\nINDONESIA",
     LX, LX + LW, 121.0, 127.0,
     ha="center", va="top", fontsize=10.5, fontweight="bold",
     color="#404040", linespacing=1.15)
context = [
    "Negara kepulauan",
    "Disparitas akses",
    "Literasi digital",
    "Fragmentasi HIS",
    "30 platform/Puskesmas",
    "Regulasi & SATUSEHAT",
    "Anggaran terbatas",
]
text("panel:left-body", LX + 1.2, 119.2,
     "\n".join("• " + c for c in context),
     LX, LX + LW, 100.0, 120.0,
     ha="left", va="top", fontsize=9.7, color=DARK, linespacing=1.62)
text("panel:left-note", LX + LW / 2, 32.2,
     "Konteks membentuk\nprioritas dan kapasitas adopsi",
     LX, LX + LW, 31.0, 36.0,
     ha="center", va="bottom", fontsize=8.4, color=GREY, style="italic",
     linespacing=1.25)

# ----------------------------------------------------------------------------
# Right actors panel
# ----------------------------------------------------------------------------
RX, RW = 77.0, 22.0
box(RX, 31.0, RW, 96.0, "#F7F7F7", "#7F7F7F", lw=1.2)
text("panel:right-title", RX + RW / 2, 125.6, "AKTOR &\nKEPENTINGAN",
     RX, RX + RW, 121.0, 127.0,
     ha="center", va="top", fontsize=10.5, fontweight="bold",
     color="#404040", linespacing=1.15)
actors = [
    "Kemenkes & DTO",
    "Fasyankes & lab",
    "Profesional & pasien",
    "Vendor & integrator",
    "Akademisi & asosiasi",
    "Mitra pembangunan",
]
text("panel:right-body", RX + 1.2, 119.2,
     "\n".join("• " + a for a in actors),
     RX, RX + RW, 100.0, 120.0,
     ha="left", va="top", fontsize=9.7, color=DARK, linespacing=1.62)
text("panel:right-note", RX + RW / 2, 32.2,
     "Aktor mengoperasikan\nsetiap lapisan kerangka",
     RX, RX + RW, 31.0, 36.0,
     ha="center", va="bottom", fontsize=8.4, color=GREY, style="italic",
     linespacing=1.25)

# ----------------------------------------------------------------------------
# Central layers
# ----------------------------------------------------------------------------
X, W = 25.6, 48.8

layer(X, 113.5, W, 13.0, "1. INPUT: SISTEM TERFRAGMENTASI",
      ["Rumah sakit, lab, Puskesmas, klinik",
       "Sistem legacy, proprietary, silo data"],
      "#EAF2FA", "#4A7FB5")

layer(X, 94.5, W, 13.0, "2. TATA KELOLA & KEBIJAKAN",
      ["Regulasi, kepemimpinan, pembiayaan",
       "Privasi, keamanan, consent, audit data"],
      "#FCE9D9", "#C55A11")

layer(X, 75.5, W, 13.0, "3. LAPISAN SINTAKTIS",
      ["HL7 FHIR, CDA, DICOM, REST/API",
       "Profil FHIR, validasi skema, pertukaran"],
      "#DEEBF7", "#2E75B6")

layer(X, 56.5, W, 13.0, "4. LAPISAN SEMANTIK",
      ["SNOMED CT, LOINC, ICD-10, UCUM",
       "Binding, mapping, postcoordination"],
      "#E2F0D9", "#548235")

layer(X, 37.5, W, 13.0, "5. LAPISAN FUNGSIONAL",
      ["HIE, SATUSEHAT, EMR/EHR, MPI",
       "Interoperability layer dan alur kerja"],
      "#FFF2CC", "#BF9000")

layer(X, 18.5, W, 13.0, "6. OUTCOME",
      ["Kualitas data & kesinambungan layanan",
       "Surveilans, riset, dan ekuitas"],
      "#E4DFEC", "#7030A0")

# arrows between layers (bottom of one box -> top of the next)
for y1, y2 in [(113.5, 107.5), (94.5, 88.5), (75.5, 69.5),
               (56.5, 50.5), (37.5, 31.5)]:
    down_arrow(50, y1, y2)

# ----------------------------------------------------------------------------
# Feedback loop
# ----------------------------------------------------------------------------
box(X, 4.0, W, 9.8, "#D9E2F3", "#1F4E79", lw=1.3)
text("feedback:title", 50, 12.7, "UMPAN BALIK & PEMBELAJARAN",
     X, X + W, 9.5, 13.5,
     ha="center", va="top", fontsize=11.2, fontweight="bold", color=NAVY)
text("feedback:body", 50, 8.0,
     "Monitoring & evaluasi  |  audit kualitas data\n"
     "Evolusi standar  |  capacity building",
     X, X + W, 4.0, 10.6,
     ha="center", va="center", fontsize=9.6, color=DARK, linespacing=1.3)

# outcome -> feedback
down_arrow(50, 18.5, 13.8)

# feedback -> governance (left-side loop, between context panel and stack)
ax.plot([24.2, 24.2, 24.2, X], [8.2, 8.2, 101.0, 101.0],
        color="#1F4E79", linewidth=1.6, linestyle=(0, (4, 2)), zorder=3)
ax.annotate("", xy=(X, 101.0), xytext=(24.2, 101.0),
            arrowprops=dict(arrowstyle="-|>", color="#1F4E79",
                            lw=1.6, mutation_scale=15), zorder=4)
text("feedback:label", 23.9, 8.2, "feedback loop",
     14.5, 23.9, 6.0, 10.5,
     ha="right", va="center", fontsize=7.4,
     color="#1F4E79", style="italic")

# ----------------------------------------------------------------------------
# Legend / note
# ----------------------------------------------------------------------------
text("note", 50, 0.2,
     "Catatan: lapisan 2 bersifat lintas-sektoral;\n"
     "lapisan 3–5 berjalan bersama, bukan berurutan secara kaku.",
     0, 100, 0.0, 3.8,
     ha="center", va="bottom", fontsize=8.4, color=GREY, style="italic",
     linespacing=1.25)

# thin connectors between side panels and the central stack
for y in (31.0, 127.0):
    ax.plot([LX + LW, X], [y, y], color="#BFBFBF", lw=0.8, zorder=1)
    ax.plot([X + W, RX], [y, y], color="#BFBFBF", lw=0.8, zorder=1)

fig.subplots_adjust(left=0.005, right=0.995, top=0.995, bottom=0.005)
fig.savefig(OUT, dpi=300, bbox_inches="tight", pad_inches=0.08,
            facecolor="white")

# ----------------------------------------------------------------------------
# Fit check (data coordinates)
# ----------------------------------------------------------------------------
fig.canvas.draw()
renderer = fig.canvas.get_renderer()
to_data = ax.transData.inverted()
problems = []
for label, artist, x0, x1, y0, y1 in TEXTS:
    bb = artist.get_window_extent(renderer)
    (xa, ya), (xb, yb) = to_data.transform([[bb.x0, bb.y0], [bb.x1, bb.y1]])
    # small tolerance because glyph bboxes include padding
    if xa < x0 - 0.35 or xb > x1 + 0.35 or ya < y0 - 0.35 or yb > y1 + 0.35:
        problems.append(
            f"{label}: bbox=({xa:.1f},{ya:.1f})-({xb:.1f},{yb:.1f}) "
            f"limits=({x0:.1f},{y0:.1f})-({x1:.1f},{y1:.1f})"
        )

plt.close(fig)
print(f"Saved {OUT} ({OUT.stat().st_size} bytes)")
if problems:
    print("WARNING: text outside its allowed area:")
    for p in problems:
        print(" -", p)
    raise SystemExit(1)
print("Layout check: OK")
