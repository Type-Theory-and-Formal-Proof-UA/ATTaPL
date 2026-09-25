#!/usr/bin/env python3
"""Split the layout dump into physical pages and locate chapter openings."""
import re, json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
raw = (ROOT / "raw" / "layout.txt").read_text(encoding="utf-8", errors="replace")
pages = raw.split("\f")
print("physical pages:", len(pages))

# chapter opening titles as printed on their first page
starts = [
    ("preface", "Preface"),
    ("ch01", "Substructural Type Systems"),
    ("ch02", "Dependent Types"),
    ("ch03", "Effect Types and Region-Based Memory Management"),
    ("ch04", "Typed Assembly Language"),
    ("ch05", "Proof-Carrying Code"),
    ("ch06", "Logical Relations and a Case Study in Equivalence Checking"),
    ("ch07", "Typed Operational Reasoning"),
    ("ch08", "Design Considerations for ML-Style Module Systems"),
    ("ch09", "Type Definitions"),
    ("ch10", "The Essence of ML Type Inference"),
    ("appa", "Solutions to Selected Exercises"),
    ("refs", "References"),
    ("index", "Index"),
]
found = {}
for i, p in enumerate(pages):
    lines = [l.strip() for l in p.splitlines() if l.strip()]
    if not lines:
        continue
    head = " ".join(lines[:6])
    for key, title in starts:
        if key in found:
            continue
        # chapter openers put the title in the first few lines, alone on its line
        if any(l == title for l in lines[:4]):
            found[key] = {"page": i, "line0": lines[0][:70], "nlines": len(lines)}
json.dump(found, open(ROOT / "raw" / "starts.json", "w"), indent=1)
for k, v in found.items():
    print(k, v["page"], "|", v["line0"])
