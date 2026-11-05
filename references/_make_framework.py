# -*- coding: utf-8 -*-
"""Generate the conceptual framework diagram for the literature review."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "framework.png"

plt.rcParams["font.family"] = "DejaVu Sans"

fig, ax = plt.subplots(figsize=(9, 11.5), dpi=240)
ax.set_xlim(0, 100)
ax.set_ylim(0, 140)
ax.axis("off")
fig.patch.set_facecolor("white")

NAVY = "#0B2545"
GREY = "#595959"
DARK = "#1F1F1F"


def box(x, y, w, h, face, edge, lw=1.6, radius=0.9, alpha=1.0):
    p = FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad=0.35,rounding_size={radius}",
        linewidth=lw, edgecolor=edge, facecolor=face, alpha=alpha,
        zorder=2,
    )
    ax.add_patch(p)
    return p


def layer(x, y, w, h, title, bullets, face, edge, title_color=NAVY):
    box(x, y, w, h, face, edge)
    ax.text(x + w / 2, y + h - 1.4, title, ha="center", va="top",
            fontsize=14, fontweight="bold", color=title_color, zorder=3)
    ax.text(x + 1.6, y + h - 5.0, "\n".join("• " + b for b in bullets),
            ha="left", va="top", fontsize=11.5, color=DARK, linespacing=1.42,
            zorder=3)


def down_arrow(x, y1, y2, color="#1F4E79"):
    ax.add_patch(FancyArrowPatch(
        (x, y1), (x, y2),
        arrowstyle="-|>", mutation_scale=19, linewidth=2.1,
        color=color, zorder=4, shrinkA=2, shrinkB=2,
    ))


# ----------------------------------------------------------------------------
# Title
# ----------------------------------------------------------------------------
ax.text(50, 137.4, "Kerangka Interoperabilitas Sosio-Teknis Berlapis (KIST)",
        ha="center", va="top", fontsize=18, fontweight="bold", color=NAVY)
ax.text(50, 132.8,
        "Sintesis 26 artikel (2020–2026) tentang standar, koding, dan implementasi di Indonesia",
        ha="center", va="top", fontsize=10.5, color=GREY, style="italic")

# ----------------------------------------------------------------------------
# Left context panel
# ----------------------------------------------------------------------------
box(1.0, 36, 22.2, 91, "#F7F7F7", "#7F7F7F", lw=1.3)
ax.text(12.1, 125.2, "KONTEKS INDONESIA", ha="center", va="top",
        fontsize=10.5, fontweight="bold", color="#404040")
context = [
    "Negara kepulauan",
    "Disparitas akses",
    "Literasi digital",
    "Fragmentasi HIS",
    "30 platform/Puskesmas",
    "Regulasi & SATUSEHAT",
    "Anggaran terbatas",
]
ax.text(2.4, 120.8, "\n".join("• " + c for c in context),
        ha="left", va="top", fontsize=9.5, color=DARK, linespacing=1.55)
ax.text(12.1, 38.4, "Konteks membentuk\nprioritas dan kapasitas adopsi",
        ha="center", va="bottom", fontsize=8.2, color=GREY, style="italic")

# ----------------------------------------------------------------------------
# Right actors panel
# ----------------------------------------------------------------------------
box(76.8, 36, 22.2, 91, "#F7F7F7", "#7F7F7F", lw=1.3)
ax.text(87.9, 125.2, "AKTOR & KEPENTINGAN", ha="center", va="top",
        fontsize=10.5, fontweight="bold", color="#404040")
actors = [
    "Kemenkes & DTO",
    "Fasyankes & lab",
    "Profesional & pasien",
    "Vendor & integrator",
    "Akademisi & asosiasi",
    "Mitra pembangunan",
]
ax.text(78.4, 120.8, "\n".join("• " + a for a in actors),
        ha="left", va="top", fontsize=9.5, color=DARK, linespacing=1.55)
ax.text(87.9, 38.4, "Aktor mengoperasikan\nsetiap lapisan kerangka",
        ha="center", va="bottom", fontsize=8.2, color=GREY, style="italic")

# ----------------------------------------------------------------------------
# Central layers
# ----------------------------------------------------------------------------
X, W = 25.0, 50.0

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
      ["Kualitas data dan kesinambungan layanan",
       "Surveilans, riset, dan ekuitas"],
      "#E4DFEC", "#7030A0")

# arrows between layers
for y1, y2 in [(113.5, 107.7), (94.5, 88.7), (75.5, 69.7), (56.5, 50.7), (37.5, 31.7)]:
    down_arrow(50, y1, y2)

# ----------------------------------------------------------------------------
# Feedback loop
# ----------------------------------------------------------------------------
box(25.0, 3.0, 50.0, 10.8, "#D9E2F3", "#1F4E79", lw=1.4)
ax.text(50, 13.3, "UMPAN BALIK & PEMBELAJARAN",
        ha="center", va="top", fontsize=11.5, fontweight="bold", color=NAVY)
ax.text(50, 8.4,
        "Monitoring & evaluasi  |  audit kualitas data\n"
        "Evolusi standar  |  capacity building",
        ha="center", va="center", fontsize=9.5, color=DARK, linespacing=1.3)

# outcome -> feedback
ax.add_patch(FancyArrowPatch(
    (50, 18.5), (50, 14.0), arrowstyle="-|>", mutation_scale=17,
    linewidth=1.9, color="#1F4E79", zorder=4, shrinkA=2, shrinkB=2,
))

# feedback -> governance (left side loop)
ax.plot([23.8, 23.8, 23.8, 25], [8.5, 8.5, 101.0, 101.0],
        color="#1F4E79", linewidth=1.7, linestyle=(0, (4, 2)), zorder=3)
ax.annotate("", xy=(25.0, 101.0), xytext=(23.8, 101.0),
            arrowprops=dict(arrowstyle="-|>", color="#1F4E79",
                            lw=1.7, mutation_scale=16), zorder=4)
ax.text(24.35, 55, "feedback loop", rotation=90, ha="center", va="center",
        fontsize=7.4, color="#1F4E79", style="italic")

# ----------------------------------------------------------------------------
# Legend / note
# ----------------------------------------------------------------------------
ax.text(50, 0.8,
        "Catatan: lapisan 2 bersifat lintas-sektoral;\n"
        "lapisan 3–5 berjalan bersama, bukan berurutan secara kaku.",
        ha="center", va="bottom", fontsize=8.2, color=GREY, style="italic",
        linespacing=1.3)

# thin bracket between context/actors and central stack
for y in (36, 127):
    ax.plot([23.2, 25.0], [y, y], color="#BFBFBF", lw=0.9, zorder=1)
    ax.plot([75.0, 76.8], [y, y], color="#BFBFBF", lw=0.9, zorder=1)

fig.subplots_adjust(left=0.01, right=0.99, top=0.995, bottom=0.005)
fig.savefig(OUT, dpi=240, bbox_inches="tight", facecolor="white")
plt.close(fig)
print("Saved", OUT, OUT.stat().st_size)
