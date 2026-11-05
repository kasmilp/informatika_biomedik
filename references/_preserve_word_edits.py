# -*- coding: utf-8 -*-
"""Carry the user's visible Word formatting and document metadata into the rebuild."""
from pathlib import Path
import docx
from docx.enum.text import WD_ALIGN_PARAGRAPH

NEW = Path("Literature Review and Critical Synthesis.docx")
OLD = Path("references/_backup_before_15.docx")

old = docx.Document(OLD)
new = docx.Document(NEW)

# The two visible paragraph-level changes Word made in the user's copy.
for p in new.paragraphs:
    text = p.text.strip()
    if p.style.name == "Title" and text.startswith("Interoperabilitas dan Standardisasi"):
        p.paragraph_format.alignment = None
    elif p.style.name == "Subtitle" and text.startswith("Literature Review and Critical Synthesis"):
        p.paragraph_format.space_before = None

# Preserve document properties so the file keeps the user's authorship metadata.
src = old.core_properties
dst = new.core_properties
for attr in (
    "author",
    "category",
    "comments",
    "content_status",
    "created",
    "identifier",
    "keywords",
    "language",
    "last_modified_by",
    "last_printed",
    "modified",
    "revision",
    "subject",
    "title",
    "version",
):
    try:
        value = getattr(src, attr)
        setattr(dst, attr, value)
    except Exception:
        pass

new.save(NEW)
print("Preserved title/subtitle formatting and core properties")
print("author:", new.core_properties.author)
print("last_modified_by:", new.core_properties.last_modified_by)
print("revision:", new.core_properties.revision)
