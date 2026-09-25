#!/usr/bin/env python3
"""Extract the book with PyMuPDF into per-unit text files with page markers.

Output: src/<unit>.txt with lines  <<<P <physical-page> (printed <n>)>>>
Ligatures are normalised (ﬁ→fi), soft hyphen dropped, and PUA big-brace glyphs
kept as their own code points so the cleaner can see them.
"""
import fitz, pathlib, unicodedata, json, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
doc = fitz.open(next(ROOT.glob("*.pdf")))

# unit -> (first physical page, last physical page inclusive)
UNITS = [
    ("front", 0, 16),
    ("ch01", 17, 58),
    ("ch02", 59, 100),
    ("ch03", 101, 154),
    ("ch04", 155, 190),
    ("ch05", 191, 236),
    ("ch06", 237, 258),
    ("ch07", 259, 306),
    ("ch08", 307, 360),
    ("ch09", 361, 402),
    ("ch10", 403, 504),
    ("appa", 505, 548),
    ("refs", 549, 580),
    ("index", 581, len(doc) - 1),
]

NORM = {
    "\ufb00": "ff", "\ufb01": "fi", "\ufb02": "fl", "\ufb03": "ffi", "\ufb04": "ffl",
    "\u00ad": "", "\u200b": "", "\u0000": "",
    "\u2018": "\u2019", "\u201B": "\u2019",   # left single quote in words -> right
}

out = ROOT / "src"
out.mkdir(exist_ok=True)
report = []
for unit, a, b in UNITS:
    buf = []
    for p in range(a, b + 1):
        t = doc[p].get_text()
        for k, v in NORM.items():
            t = t.replace(k, v)
        printed = p - 13
        buf.append(f"<<<P {p} (printed {printed})>>>\n" + t)
    txt = "\n".join(buf)
    (out / f"{unit}.txt").write_text(txt, encoding="utf-8")
    words = len(re.findall(r"[^\s]+", re.sub(r"<<<P[^>]*>>>", " ", txt)))
    report.append((unit, a, b, b - a + 1, words))

print(f"{'unit':7s} {'pages':>10s} {'phys':>10s} {'words':>8s}")
tot = 0
for unit, a, b, n, w in report:
    tot += w
    print(f"{unit:7s} {f'{a}-{b}':>10s} {n:10d} {w:8d}")
print(f"{'TOTAL':7s} {'':>10s} {'':>10s} {tot:8d}")
json.dump({u: {"first": a, "last": b, "pages": n, "words": w} for u, a, b, n, w in report},
          open(ROOT / "src" / "units.json", "w"), indent=2)
