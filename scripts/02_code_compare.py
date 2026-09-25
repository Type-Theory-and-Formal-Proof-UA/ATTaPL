#!/usr/bin/env python3
"""Side-by-side: what pdftotext-layout produced vs what PyMuPDF produced."""
import fitz, pathlib, re, unicodedata

ROOT = pathlib.Path(__file__).resolve().parent.parent
doc = fitz.open(next(ROOT.glob("*.pdf")))
lay = (ROOT / "raw" / "layout.txt").read_text(encoding="utf-8", errors="replace").split("\f")

CODES = ["\x0f", "\x16", "\x05", "\x01", "\uf8f4"]
for code in CODES:
    pages = [i for i, p in enumerate(lay) if code in p]
    print("=" * 78)
    print(f"CODE U+{ord(code):04X}  count_in_layout={sum(p.count(code) for p in lay)}  pages={pages[:8]}")
    for pno in pages[:2]:
        m = re.search(re.escape(code), lay[pno])
        a, b = max(0, m.start() - 60), m.end() + 60
        win = lay[pno][a:b].replace("\n", " | ")
        print(f"  layout p{pno}: ...{win}...")
        # what does mupdf say around the same phrase?
        txt = doc[pno].get_text()
        key = re.sub(r"\s+", " ", win).strip()[:25]
        for probe in [key, key[:12], key.split("|")[0].strip()[:12]]:
            if probe and probe in re.sub(r"\s+", " ", txt):
                tt = re.sub(r"\s+", " ", txt)
                i = tt.index(probe)
                print(f"  mupdf  p{pno}: ...{tt[max(0,i-40):i+70]}...")
                break
        else:
            print(f"  mupdf  p{pno}: (phrase not found; snippet) {re.sub(chr(10),' | ',txt)[:160]}")
    # census of candidate replacements in mupdf for the pages involved
    cand = {}
    for pno in pages:
        for ch in doc[pno].get_text():
            if ord(ch) > 0x2000:
                cand[ch] = cand.get(ch, 0) + 1
    top = sorted(cand.items(), key=lambda kv: -kv[1])[:8]
    print("  mupdf candidates on those pages:",
          ", ".join(f"{c!r}(U+{ord(c):04X})={n}" for c, n in top))
