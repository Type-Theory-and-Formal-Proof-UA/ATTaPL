#!/usr/bin/env python3
"""Per-page census: layout dump vs PyMuPDF text, to derive a complete mapping."""
import fitz, pathlib, collections, unicodedata, json, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
doc = fitz.open(next(ROOT.glob("*.pdf")))
lay = (ROOT / "raw" / "layout.txt").read_text(encoding="utf-8", errors="replace").split("\f")


def interesting(s):
    c = collections.Counter()
    for ch in s:
        o = ord(ch)
        if ch in "\n\r\t":
            continue
        if o < 32 or o >= 0x2000:
            c[ch] += 1
    return c


LIG = {"\ufb00": "ff", "\ufb01": "fi", "\ufb02": "fl", "\ufb03": "ffi", "\ufb04": "ffl"}

pages_bad = []
for pno in range(1, len(lay)):
    m = interesting(doc[pno - 1].get_text())          # mupdf page pno-1 == layout page pno
    l = interesting(lay[pno])
    # normalise ligatures away in mupdf side for comparison of *symbols*
    mm = collections.Counter()
    for ch, n in m.items():
        if ch in LIG:
            continue
        mm[ch] += n
    ll = collections.Counter({ch: n for ch, n in l.items() if ch not in LIG})
    extra_m = mm - ll
    # collapse layout control codes into one bucket keyed by code
    extra_m_syms = {ch: n for ch, n in extra_m.items() if ord(ch) > 0x2000}
    if extra_m_syms and sum(extra_m_syms.values()) > 3:
        pages_bad.append((pno, extra_m_syms, {k: v for k, v in extra_m.items() if ord(k) < 32}))

print("pages where mupdf has symbols layout lacks (top 25):")
for pno, sym, ctl in sorted(pages_bad, key=lambda t: -sum(t[1].values()))[:25]:
    s = ", ".join(f"{c!r}(U+{ord(c):04X})={n}" for c, n in sorted(sym.items(), key=lambda kv: -kv[1])[:6])
    print(f"  layout-page {pno}:  {s}")

print()
print("all control codes used by layout, with mupdf-side candidate on same page:")
codes = collections.Counter(ch for p in lay for ch in p if ord(ch) < 32 and ch not in "\n\t\f\r")
for code, n in codes.most_common():
    pages = [i for i, p in enumerate(lay) if code in p]
    cand = collections.Counter()
    for pno in pages:
        for ch in doc[pno - 1].get_text():
            if ord(ch) > 0x2000 and ch not in LIG:
                cand[ch] += 1
    print(f"  U+{ord(code):04X} n={n:4d} layout-pages={pages[:6]}  mupdf page symbols: "
          + ", ".join(f"{c!r}={v}" for c, v in cand.most_common(5)))
