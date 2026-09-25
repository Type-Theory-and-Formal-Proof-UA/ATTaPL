#!/usr/bin/env python3
"""Locate the mangled code points and render zoomed crops for visual ID."""
import fitz, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
pdf = next(ROOT.glob("*.pdf"))
doc = fitz.open(pdf)

TARGETS = ["\x16", "\x0f", "\x05", "\x01", "\uf8f4"]
outdir = ROOT / "raw" / "crops"
outdir.mkdir(parents=True, exist_ok=True)
found = {t: [] for t in TARGETS}

for pno in range(len(doc)):
    page = doc[pno]
    d = page.get_text("rawdict")
    for blk in d["blocks"]:
        for line in blk.get("lines", []):
            for span in line.get("spans", []):
                for ch in span["chars"]:
                    c = ch["c"]
                    if c in found and len(found[c]) < 12:
                        found[c].append((pno, ch["bbox"], span["font"]))
for t in TARGETS:
    print("=" * 60)
    print("code", hex(ord(t)), "hits captured:", len(found[t]))
    for pno, bbox, font in found[t][:4]:
        print(f"  page {pno} bbox {[round(x,1) for x in bbox]} font {font}")

# render one crop per code
for t in TARGETS:
    if not found[t]:
        continue
    pno, bbox, font = found[t][0]
    x0, y0, x1, y1 = bbox
    pad = 60
    clip = fitz.Rect(max(0, x0 - pad), max(0, y0 - 12), min(576, x1 + pad), min(648, y1 + 12))
    pix = doc[pno].get_pixmap(matrix=fitz.Matrix(6, 6), clip=clip)
    p = outdir / f"{ord(t):04x}.png"
    pix.save(p)
    print("saved", p, "clip", clip, "font", font)
