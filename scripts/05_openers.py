#!/usr/bin/env python3
"""Structural detection of chapter/part opener pages: first line is the chapter number/letter."""
import fitz, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
doc = fitz.open(next(ROOT.glob("*.pdf")))
N = len(doc)

for p in range(N):
    lines = [l.strip() for l in doc[p].get_text().splitlines() if l.strip()]
    if not lines:
        continue
    first = lines[0]
    nxt = " / ".join(lines[1:3])[:70]
    if re.fullmatch(r"(\d{1,2}|[A-Z]|I{1,3}V?|IV|V)", first) and len(lines) > 2:
        # exclude contents pages (they have many '....' leaders) and index
        body = doc[p].get_text()
        if body.count("....") > 2:
            continue
        if "Index" == lines[0]:
            continue
        print(f"p{p:3d} (printed {p-13:3d})  #{first:3s}  {nxt}")
