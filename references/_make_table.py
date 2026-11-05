# -*- coding: utf-8 -*-
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent
rows = list(csv.DictReader((ROOT / "synthesis_matrix.csv").open(encoding="utf-8-sig")))

def clean(s):
    return " ".join((s or "").replace("|", "/").split())

lines = [
    "| No | Paper | Standar | Level | Temuan Utama | Limitasi / Gap |",
    "|---|---|---|---|---|---|",
]
for r in rows:
    paper = f"{r['Authors']} ({r['Year']})"
    lines.append(
        "| {no} | {paper} | {std} | {lvl} | {find} | {lim} |".format(
            no=r["ID"],
            paper=clean(paper),
            std=clean(r["Standards"]),
            lvl=clean(r["Interoperability_Level"]),
            find=clean(r["Main_Findings"]),
            lim=clean(r["Limitations_Gap"]),
        )
    )

out = ROOT / "_matrix_table.md"
out.write_text("\n".join(lines) + "\n", encoding="utf-8")
print("Wrote", out, len(lines) - 2, "rows")
