#!/usr/bin/env python3
"""Extract the true heading tree (font/size based) with word offsets per unit.

Heading styles found in this book:
  chapter opener : size >= 12 (title), plus number
  top section    : font 'Gd', size 10.5   e.g. '1.2  A Linear Type System'
  subsection     : font 'Gd', size 9.7    e.g. 'Syntax', 'Typing'
Body text is 'Gb' 9.0. Running heads/captions are smaller or other fonts.
"""
import fitz, pathlib, json, re, collections

ROOT = pathlib.Path(__file__).resolve().parent.parent
doc = fitz.open(next(ROOT.glob("*.pdf")))
UNITS = json.load(open(ROOT / "src" / "units.json"))

STYLE = {}  # (font,size) -> count of chars
for p in range(len(doc)):
    for b in doc[p].get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            for s in l["spans"]:
                STYLE[(s["font"], round(s["size"], 1))] = STYLE.get((s["font"], round(s["size"], 1)), 0) + len(s["text"])

print("-- most common (font,size) --")
for k, v in sorted(STYLE.items(), key=lambda kv: -kv[1])[:16]:
    print(f"   {k[0]:10s} {k[1]:5.1f} {v:8d}")

res = {}
for unit in ["front", "ch01", "ch02", "ch03", "ch04", "ch05", "ch06", "ch07", "ch08", "ch09",
             "ch10", "appa", "refs", "index"]:
    info = UNITS[unit]
    a, b = info["first"], info["last"]
    items = []
    for p in range(a, b + 1):
        d = doc[p].get_text("dict")
        for blk in d["blocks"]:
            for line in blk.get("lines", []):
                for s in line["spans"]:
                    t = s["text"]
                    if not t.strip():
                        continue
                    items.append({"page": p, "y": round(s["bbox"][1], 1), "x": round(s["bbox"][0], 1),
                                  "size": round(s["size"], 1), "font": s["font"], "text": t})
    # sort reading order: page, then y, then x
    items.sort(key=lambda it: (it["page"], it["y"], it["x"]))
    # count body words with a word counter over full text, then locate heading words by prefix
    heads = []
    for it in items:
        big = it["size"] >= 11.9 or (it["font"] == "Gd" and it["size"] >= 9.6)
        if big:
            heads.append(it)
    res[unit] = {"first": a, "last": b, "words": info["words"], "headings": heads}
    print(f"\n===== {unit} ({info['words']} words) : {len(heads)} heading spans")
    seen = set()
    for h in heads:
        key = (h["page"], h["y"], h["text"][:40])
        if key in seen:
            continue
        seen.add(key)
        print(f"   p{h['page']:3d} y{h['y']:6.1f} sz{h['size']:5.1f} {h['font']:4s} {h['text'][:70]!r}")

json.dump(res, open(ROOT / "src" / "headings.json", "w"), ensure_ascii=False, indent=1)
