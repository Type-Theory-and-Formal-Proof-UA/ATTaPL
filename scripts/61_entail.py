#!/usr/bin/env python3
"""Decide the book's entailment symbol by MEASURING it, not guessing.

The extractor decodes it as a stray letter ('ð'), so we locate the span, crop its
bbox at high dpi, and count vertical dark strokes: a single-bar turnstile gives
one dark column cluster in the middle rows, a double-bar one gives two.

Prints the stroke count next to the same measurement for Typst's `models` (U+22A7)
and `tack.double` (U+22A8) so the match is unambiguous.
"""
import fitz, pathlib, subprocess

ROOT = pathlib.Path('/Users/ihor/atapl')
doc = fitz.open(next(ROOT.glob('*.pdf')))


def strokes(pix):
    """Dark-pixel count per column in the middle band (skips the horizontal foot)."""
    w, h, n = pix.width, pix.height, pix.n
    s = pix.samples
    lo, hi = int(h * 0.30), int(h * 0.75)
    cols = [0] * w
    for y in range(lo, hi):
        row = y * pix.stride
        for x in range(w):
            i = row + x * n
            g = (s[i] + s[i + 1] + s[i + 2]) / 3
            if g < 128:
                cols[x] += 1
    return cols


def clusters(cols, thresh):
    runs, n = [], 0
    for v in cols:
        if v >= thresh:
            n += 1
        elif n:
            runs.append(n)
            n = 0
    if n:
        runs.append(n)
    return runs


# --- the book's symbol: find the span the extractor turned into 'ð' on the
#     Figure 10-7 page (437), left column, first rule.
best = None
for blk in doc[437].get_text("dict")["blocks"]:
    for l in blk.get("lines", []):
        for s in l["spans"]:
            if s["text"].strip() in ('ð', '⊨', '⊧', '=', '⊢') and s["bbox"][0] < 260 and s["bbox"][1] < 100:
                print(f'candidate span {s["text"]!r} bbox={s["bbox"]} font={s["font"]}')
                if s["text"].strip() == 'ð':
                    best = s["bbox"]
print('chosen bbox:', best)


def measure(rect, dpi=600):
    pix = doc[437].get_pixmap(dpi=dpi, clip=fitz.Rect(*rect))
    cols = strokes(pix)
    th = max(2, int(pix.height / dpi * 2))
    return clusters(cols, th) or clusters(cols, 1), pix


if best:
    x0, y0, x1, y1 = best
    runs, pix = measure((x0 - 1, y0 - 1, x1 + 1, y1 + 1))
    print(f'BOOK glyph strokes (dark column runs): {runs}')
    print(f'BOOK glyph size: {pix.width}x{pix.height}')
    pix.save(ROOT / 'raw' / 'crops' / 'entail_book.png')

# --- Typst candidates, same pipeline
probe = ROOT / 'build' / '_pentail2.typ'
probe.write_text('#import "/templates/preamble.typ": *\n'
                 '$C models sigma$ \\ $C tack.double sigma$\n')
subprocess.run(['typst', 'compile', '--root', str(ROOT), str(probe), '/tmp/pe2.pdf'],
               capture_output=True, text=True)
d2 = fitz.open('/tmp/pe2.pdf')
for pg in d2:
    for blk in pg.get_text("dict")["blocks"]:
        for l in blk.get("lines", []):
            for s in l["spans"]:
                t = s["text"].strip()
                if t in ('⊧', '⊨'):
                    runs, pix = measure(s["bbox"])
                    print(f'TYPST {t} U+{ord(t):04X} strokes: {runs}  size {pix.width}x{pix.height}')
