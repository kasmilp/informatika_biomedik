# -*- coding: utf-8 -*-
"""Post-process the Pandoc-generated DOCX into an academic manuscript layout."""
import copy
import sys
from pathlib import Path

from docx import Document
from docx.enum.section import WD_ORIENT
from docx.enum.table import WD_ALIGN_VERTICAL, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

SRC = Path("Literature Review and Critical Synthesis.docx")
DST = SRC

FONT = "Times New Roman"
BLACK = RGBColor(0, 0, 0)
ACCENT = RGBColor(0x1F, 0x3B, 0x63)


def set_run_font(run, size=None, bold=None, italic=None, color=BLACK):
    run.font.name = FONT
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts")
        rPr.insert(0, rFonts)
    for attr in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
        rFonts.set(qn(attr), FONT)
    if size is not None:
        run.font.size = Pt(size)
    if bold is not None:
        run.font.bold = bold
    if italic is not None:
        run.font.italic = italic
    if color is not None:
        run.font.color.rgb = color


def style_font(style, size=None, bold=None, italic=None, color=BLACK):
    style.font.name = FONT
    rPr = style.element.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts")
        rPr.insert(0, rFonts)
    for attr in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
        rFonts.set(qn(attr), FONT)
    if size is not None:
        style.font.size = Pt(size)
    if bold is not None:
        style.font.bold = bold
    if italic is not None:
        style.font.italic = italic
    if color is not None:
        style.font.color.rgb = color


def set_lang(style, lang="id-ID"):
    rPr = style.element.get_or_add_rPr()
    el = rPr.find(qn("w:lang"))
    if el is None:
        el = OxmlElement("w:lang")
        rPr.append(el)
    el.set(qn("w:val"), lang)
    el.set(qn("w:eastAsia"), lang)


def add_field(paragraph, instruction, placeholder="1"):
    run = paragraph.add_run()
    fld = OxmlElement("w:fldChar")
    fld.set(qn("w:fldCharType"), "begin")
    run._r.append(fld)

    run = paragraph.add_run()
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = f" {instruction} "
    run._r.append(instr)

    run = paragraph.add_run()
    fld = OxmlElement("w:fldChar")
    fld.set(qn("w:fldCharType"), "separate")
    run._r.append(fld)

    run = paragraph.add_run(placeholder)

    run = paragraph.add_run()
    fld = OxmlElement("w:fldChar")
    fld.set(qn("w:fldCharType"), "end")
    run._r.append(fld)


def rebuild_tblpr(table, top=30, bottom=30, left=70, right=70):
    """Rebuild w:tblPr with children in the OOXML schema order."""
    tblPr = table._tbl.tblPr
    style = tblPr.find(qn("w:tblStyle"))
    look = tblPr.find(qn("w:tblLook"))
    for child in list(tblPr):
        tblPr.remove(child)

    if style is not None:
        tblPr.append(style)

    tbl_w = OxmlElement("w:tblW")
    tbl_w.set(qn("w:w"), "5000")
    tbl_w.set(qn("w:type"), "pct")
    tblPr.append(tbl_w)

    jc = OxmlElement("w:jc")
    jc.set(qn("w:val"), "center")
    tblPr.append(jc)

    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = OxmlElement(f"w:{edge}")
        el.set(qn("w:val"), "single")
        el.set(qn("w:sz"), "4")
        el.set(qn("w:space"), "0")
        el.set(qn("w:color"), "7F7F7F")
        borders.append(el)
    tblPr.append(borders)

    layout = OxmlElement("w:tblLayout")
    layout.set(qn("w:type"), "fixed")
    tblPr.append(layout)

    mar = OxmlElement("w:tblCellMar")
    for side, val in (("top", top), ("left", left), ("bottom", bottom), ("right", right)):
        el = OxmlElement(f"w:{side}")
        el.set(qn("w:w"), str(val))
        el.set(qn("w:type"), "dxa")
        mar.append(el)
    tblPr.append(mar)

    if look is not None:
        tblPr.append(look)


def set_grid(table, fractions, content_cm):
    widths = [round(content_cm * f, 2) for f in fractions]
    tbl = table._tbl
    grid = tbl.tblGrid
    cols = grid.findall(qn("w:gridCol"))
    for col, cm in zip(cols, widths):
        col.set(qn("w:w"), str(int(Cm(cm).twips)))
    for row in table.rows:
        for cell, cm in zip(row.cells, widths):
            cell.width = Cm(cm)
    return widths


def shade(cell, fill):
    tcPr = cell._tc.get_or_add_tcPr()
    old = tcPr.find(qn("w:shd"))
    if old is not None:
        tcPr.remove(old)
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill)
    tcPr.append(shd)


def mark_header_row(row):
    trPr = row._tr.get_or_add_trPr()
    el = trPr.find(qn("w:tblHeader"))
    if el is None:
        el = OxmlElement("w:tblHeader")
        trPr.append(el)
    # Word repeats the header only for the canonical "true" value; "on" is
    # accepted by the schema but is not honoured by every Word version.
    el.set(qn("w:val"), "true")


def no_split(row):
    trPr = row._tr.get_or_add_trPr()
    if trPr.find(qn("w:cantSplit")) is None:
        el = OxmlElement("w:cantSplit")
        header = trPr.find(qn("w:tblHeader"))
        if header is not None:
            header.addprevious(el)
        else:
            trPr.append(el)


def fmt_table(table, fractions, content_cm, font_size, header_fill="D9E2F3"):
    table.autofit = False
    rebuild_tblpr(table)
    set_grid(table, fractions, content_cm)

    for r_idx, row in enumerate(table.rows):
        no_split(row)
        if r_idx == 0:
            mark_header_row(row)
        for cell in row.cells:
            if r_idx == 0:
                shade(cell, header_fill)
            cell.vertical_alignment = (
                WD_ALIGN_VERTICAL.CENTER if r_idx == 0 else WD_ALIGN_VERTICAL.TOP
            )
            for p in cell.paragraphs:
                pf = p.paragraph_format
                pf.space_before = Pt(0)
                pf.space_after = Pt(0)
                pf.line_spacing = 1.0
                # Compact inherits Body Text's first-line indent, which would
                # shrink the usable width of narrow table cells.
                pf.first_line_indent = Cm(0)
                pf.left_indent = Cm(0)
                pf.right_indent = Cm(0)
                pf.alignment = (
                    WD_ALIGN_PARAGRAPH.CENTER
                    if r_idx == 0
                    else WD_ALIGN_PARAGRAPH.LEFT
                )
                for run in p.runs:
                    set_run_font(
                        run,
                        size=font_size,
                        bold=True if r_idx == 0 else None,
                        color=BLACK,
                    )


def sect_copy(section):
    return copy.deepcopy(section._sectPr)


def set_page(sectPr, landscape=False, margin_cm=2.5):
    pgSz = sectPr.find(qn("w:pgSz"))
    if pgSz is None:
        pgSz = OxmlElement("w:pgSz")
        sectPr.append(pgSz)
    if landscape:
        pgSz.set(qn("w:w"), str(int(Cm(29.7).twips)))
        pgSz.set(qn("w:h"), str(int(Cm(21.0).twips)))
        pgSz.set(qn("w:orient"), "landscape")
    else:
        pgSz.set(qn("w:w"), str(int(Cm(21.0).twips)))
        pgSz.set(qn("w:h"), str(int(Cm(29.7).twips)))
        pgSz.set(qn("w:orient"), "portrait")

    pgMar = sectPr.find(qn("w:pgMar"))
    if pgMar is None:
        pgMar = OxmlElement("w:pgMar")
        sectPr.append(pgMar)
    m = int(Cm(margin_cm).twips)
    pgMar.set(qn("w:top"), str(m))
    pgMar.set(qn("w:bottom"), str(m))
    pgMar.set(qn("w:left"), str(m))
    pgMar.set(qn("w:right"), str(m))
    pgMar.set(qn("w:header"), str(int(Cm(1.25).twips)))
    pgMar.set(qn("w:footer"), str(int(Cm(1.25).twips)))
    pgMar.set(qn("w:gutter"), "0")


def add_sectpr_to_paragraph(paragraph, sectPr):
    pPr = paragraph._p.get_or_add_pPr()
    old = pPr.find(qn("w:sectPr"))
    if old is not None:
        pPr.remove(old)
    pPr.append(sectPr)


doc = Document(SRC)

# ---------------------------------------------------------------- styles
styles = doc.styles

normal = styles["Normal"]
style_font(normal, size=11)
set_lang(normal)
normal.paragraph_format.line_spacing = 1.15
normal.paragraph_format.space_before = Pt(0)
normal.paragraph_format.space_after = Pt(6)
normal.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
normal.paragraph_format.widow_control = True

body = styles["Body Text"]
style_font(body, size=11)
body.paragraph_format.line_spacing = 1.15
body.paragraph_format.space_before = Pt(0)
body.paragraph_format.space_after = Pt(6)
body.paragraph_format.first_line_indent = Cm(0.75)
body.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

firstp = styles["First Paragraph"]
style_font(firstp, size=11)
firstp.paragraph_format.line_spacing = 1.15
firstp.paragraph_format.space_before = Pt(0)
firstp.paragraph_format.space_after = Pt(6)
firstp.paragraph_format.first_line_indent = Cm(0)
firstp.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

compact = styles["Compact"]
style_font(compact, size=11)
compact.paragraph_format.line_spacing = 1.15
compact.paragraph_format.space_before = Pt(0)
compact.paragraph_format.space_after = Pt(2)

h1 = styles["Heading 1"]
style_font(h1, size=14, bold=True, italic=False, color=ACCENT)
h1.paragraph_format.space_before = Pt(18)
h1.paragraph_format.space_after = Pt(8)
h1.paragraph_format.keep_with_next = True
h1.paragraph_format.line_spacing = 1.1

h2 = styles["Heading 2"]
style_font(h2, size=12, bold=True, italic=False, color=ACCENT)
h2.paragraph_format.space_before = Pt(14)
h2.paragraph_format.space_after = Pt(6)
h2.paragraph_format.keep_with_next = True
h2.paragraph_format.line_spacing = 1.1

h3 = styles["Heading 3"]
style_font(h3, size=11, bold=True, italic=False, color=ACCENT)
h3.paragraph_format.space_before = Pt(10)
h3.paragraph_format.space_after = Pt(4)
h3.paragraph_format.keep_with_next = True
h3.paragraph_format.line_spacing = 1.1

for name, size in (("Title", 22), ("Subtitle", 12.5)):
    st = styles[name]
    style_font(st, size=size, bold=(name == "Title"), italic=(name == "Subtitle"))
    st.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    st.paragraph_format.space_before = Pt(0)
    st.paragraph_format.space_after = Pt(0)
    st.paragraph_format.line_spacing = 1.15

for name, size, bold in (("Author", 12, True), ("Date", 11, False)):
    st = styles[name]
    style_font(st, size=size, bold=bold)
    st.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    st.paragraph_format.space_before = Pt(0)
    st.paragraph_format.space_after = Pt(0)

cap = styles["Table Caption"]
style_font(cap, size=9.5, bold=True, italic=False, color=BLACK)
cap.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
cap.paragraph_format.space_before = Pt(8)
cap.paragraph_format.space_after = Pt(3)
cap.paragraph_format.keep_with_next = True
cap.paragraph_format.line_spacing = 1.0

imgcap = styles["Image Caption"]
style_font(imgcap, size=9.5, bold=False, italic=False, color=BLACK)
imgcap.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
imgcap.paragraph_format.space_before = Pt(4)
imgcap.paragraph_format.space_after = Pt(12)
imgcap.paragraph_format.line_spacing = 1.0

fig = styles["Captioned Figure"]
fig.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
fig.paragraph_format.space_before = Pt(6)
fig.paragraph_format.space_after = Pt(0)
fig.paragraph_format.keep_with_next = True

bib = styles["Bibliography"]
style_font(bib, size=9, bold=False, italic=False, color=BLACK)
bib.paragraph_format.line_spacing = 1.0
bib.paragraph_format.space_before = Pt(0)
bib.paragraph_format.space_after = Pt(4)
bib.paragraph_format.left_indent = Cm(0.75)
bib.paragraph_format.first_line_indent = Cm(-0.75)
bib.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT

# ------------------------------------------------------------------ page setup
sec = doc.sections[0]
set_page(sec._sectPr, landscape=False, margin_cm=2.5)
sec.orientation = WD_ORIENT.PORTRAIT

# footer with page number
footer = sec.footer
footer.is_linked_to_previous = False
fp = footer.paragraphs[0]
fp.text = ""
fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
fp.paragraph_format.space_before = Pt(0)
fp.paragraph_format.space_after = Pt(0)
r = fp.add_run("Halaman ")
set_run_font(r, size=9)
add_field(fp, "PAGE", "1")
for run in fp.runs:
    set_run_font(run, size=9)

# ------------------------------------------------------------- title page
paras = doc.paragraphs
# locate title paragraph (style Title)
title_p = next(p for p in paras if p.style.name == "Title")
label_p = title_p.insert_paragraph_before()
label_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
label_p.paragraph_format.space_before = Pt(60)
label_p.paragraph_format.space_after = Pt(0)
lr = label_p.add_run("TUGAS LITERATURE REVIEW DAN CRITICAL SYNTHESIS")
set_run_font(lr, size=10.5, bold=True, color=ACCENT)

title_p.paragraph_format.space_before = Pt(20)
title_p.paragraph_format.space_after = Pt(10)
title_p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
for run in title_p.runs:
    set_run_font(run, size=22, bold=True, color=ACCENT)

sub_p = next(p for p in paras if p.style.name == "Subtitle")
sub_p.paragraph_format.space_before = Pt(0)
sub_p.paragraph_format.space_after = Pt(26)
for run in sub_p.runs:
    set_run_font(run, size=12.5, italic=True, color=BLACK)

author_p = next(p for p in paras if p.style.name == "Author")
author_p.paragraph_format.space_before = Pt(24)
author_p.paragraph_format.space_after = Pt(4)
for run in author_p.runs:
    set_run_font(run, size=12.5, bold=True)

date_p = next(p for p in paras if p.style.name == "Date")
for run in date_p.runs:
    set_run_font(run, size=11, color=BLACK)

# "Abstrak" should be a top-level heading
abstract = next(p for p in doc.paragraphs if p.text.strip() == "Abstrak")
abstract.style = styles["Heading 1"]
abstract.paragraph_format.space_before = Pt(0)

# References start on a new page
ref_heading = next(
    p for p in doc.paragraphs
    if p.text.strip() == "Referensi" and p.style.name == "Heading 1"
)
ref_heading.paragraph_format.page_break_before = True

# ------------------------------------------------------- landscape section
heading = next(p for p in doc.paragraphs if p.text.strip().startswith("3.6 Matriks sintesis"))
prev = heading._p.getprevious()
if prev is not None and prev.tag == qn("w:p"):
    from docx.text.paragraph import Paragraph
    prev_p = Paragraph(prev, heading._parent)
    portrait_sect = sect_copy(sec)
    add_sectpr_to_paragraph(prev_p, portrait_sect)
else:
    raise RuntimeError("Could not find paragraph before 3.6")

# Find the synthesis matrix by its header and six columns. Its row count
# changes whenever the paper is trimmed, so it must not be hard-coded.
matrix = next(
    t for t in doc.tables
    if len(t.columns) == 6
    and len(t.rows) > 1
    and t.cell(0, 0).text.strip().lower() == "no"
)

land_sect = sect_copy(sec)
set_page(land_sect, landscape=True, margin_cm=2.0)
break_p = OxmlElement("w:p")
pPr = OxmlElement("w:pPr")
pPr.append(land_sect)
break_p.append(pPr)
matrix._tbl.addnext(break_p)

# ------------------------------------------------------------ figure sizing
for shape in doc.inline_shapes:
    if shape.width > Cm(10):
        ratio = shape.height / shape.width
        shape.width = Cm(15.7)
        shape.height = int(shape.width * ratio)
        break

# --------------------------------------------------------------- tables
fmt_table(doc.tables[0], [0.20, 0.80], 16.0, 8.5)
fmt_table(doc.tables[1], [0.22, 0.08, 0.12, 0.28, 0.30], 16.0, 8.5)
fmt_table(doc.tables[2], [0.05, 0.13, 0.14, 0.09, 0.31, 0.28], 25.7, 7.5)
fmt_table(doc.tables[3], [0.16, 0.14, 0.34, 0.36], 16.0, 8.5)
fmt_table(doc.tables[4], [0.16, 0.33, 0.25, 0.26], 16.0, 8.5)
fmt_table(doc.tables[5], [0.14, 0.22, 0.64], 16.0, 8.5)

# ------------------------------------------------------------ core props
cp = doc.core_properties
cp.title = "Interoperabilitas dan Standardisasi dalam Informatika Biomedik"
cp.subject = "Literature Review and Critical Synthesis"
cp.author = "[Nama Mahasiswa]"
cp.keywords = (
    "interoperabilitas; HL7 FHIR; SNOMED CT; LOINC; ICD-10; DICOM; SATUSEHAT; "
    "rekam medis elektronik"
)
cp.comments = "Dokumen akademik; placeholder nama dan NIM perlu diisi."

doc.save(DST)
print("saved", DST)
print("sections:", len(doc.sections))
for i, s in enumerate(doc.sections):
    print(
        i,
        "orient=", s.orientation,
        "w_cm=", round(s.page_width.cm, 2),
        "h_cm=", round(s.page_height.cm, 2),
    )
