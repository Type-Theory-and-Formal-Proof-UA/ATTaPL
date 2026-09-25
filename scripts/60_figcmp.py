#!/usr/bin/env python3
"""Compare the FIGURE NUMBERS the book prints in a chapter against those the
translation renders.

40_verify compares FIGURE-BODY markers inside a single part's source slice, which
is a split-boundary artefact: a figure whose caption lands in part 2 while its
body marker sits in part 1 looks like a mismatch in both.  What actually matters
is the set of figure numbers printed per CHAPTER, so compare that:

  book  : "Figure <ch>-<n>" occurrences on the chapter's source pages
  uk    : "Рисунок <ch>-<n>" rendered in the compiled chapter PDF
"""
import fitz, json, pathlib, re, sys

ROOT = pathlib.Path('/Users/ihor/atapl')
doc = fitz.open(next(ROOT.glob('*.pdf')))
UNITS = json.load(open(ROOT / 'src' / 'units.json'))
MAN = json.load(open(ROOT / 'manifest.json'))

ch = sys.argv[1] if len(sys.argv) > 1 else 'ch09'
parts = sorted(p for p, i in MAN.items() if i['chapter'] == ch)

# --- book side: figure numbers on the chapter's source pages
# units.json is keyed BY CHAPTER (ch09), not by part (ch09p01).
# NOTE: the chapter key carries a zero pad (ch03) but the book prints "Figure 3-1",
# so the number must be de-padded before matching.
first, last = UNITS[ch]['first'], UNITS[ch]['last']
num = str(int(ch[2:]))
book_text = "".join(doc[p].get_text() for p in range(first, last + 1))
book = sorted(set(re.findall(rf'Figure\s+{num}\s*[-‑–—]\s*(\d+)', book_text)), key=int)

# --- uk side: figure numbers rendered in the compiled chapter PDF
pdf = ROOT / 'build' / f'{ch}.pdf'
uk = []
if pdf.exists():
    t = "".join(pg.get_text() for pg in fitz.open(pdf))
    uk = sorted(set(re.findall(rf'Рисунок\s+{num}\s*[-‑–—]\s*(\d+)', t)), key=int)

print(f'{ch}: book figures {book}')
print(f'{ch}: uk   figures {uk}')
print(f'{ch}: missing in uk: {sorted(set(book) - set(uk), key=int)}')
print(f'{ch}: extra in uk  : {sorted(set(uk) - set(book), key=int)}')
