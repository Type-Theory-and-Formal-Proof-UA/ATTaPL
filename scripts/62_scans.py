#!/usr/bin/env python3
"""Decide the book's entailment glyph by SCANLINE runs, which is immune to the
downscaling that made the visual comparisons unreliable.

For a glyph box we take several horizontal scanlines through its vertical middle
(between/above the horizontals) and count the dark RUNS on each.  A single-bar
turnstile (⊧ / ⊨-style with one vertical) gives 1 run; a true double-bar turnstile
gives 2 runs.  We report the mode across scanlines for the book glyph and for each
Typst candidate.
"""
import fitz, pathlib, subprocess

ROOT = pathlib.Path('/Users/ihor/atapl')


def runs_at(pix, y):
    w, n, s = pix.width, pix.n, pix.samples
    row = y * pix.stride
    runs, cur = [], 0
    for x in range(w):
        i = row + x * n
        if (s[i] + s[i + 1] + s[i + 2]) / 3 < 128:
            cur += 1
        elif cur:
            runs.append(cur)
            cur = 0
    if cur:
        runs.append(cur)
    return runs


def profile(pix, label):
    w, h, n, s = pix.width, pix.height, pix.n, pix.samples
    # find the glyph's vertical extent
    rows_dark = []
    for y in range(h):
        c = 0
        for x in range(w):
            i = y * pix.stride + x * n
            if (s[i] + s[i + 1] + s[i + 2]) / 3 < 128:
                c += 1
        rows_dark.append(c)
    ys = [y for y, c in enumerate(rows_dark) if c]
    if not ys:
        print(f'{label}: blank')
        return
    y0, y1 = ys[0], ys[-1]
    # scan the upper 60% of the glyph (bars region, above the foot)
    outs = []
    for frac in (0.10, 0.20, 0.30, 0.40, 0.50):
        y = int(y0 + (y1 - y0) * frac)
        outs.append((frac, runs_at(pix, y)))
    print(f'{label}: glyph rows {y0}..{y1} (h={y1-y0+1})')
    for frac, r in outs:
        print(f'    y at {int(frac*100):3d}%: runs={r} -> {len(r)} stroke(s)')


# --- book glyph (page 437 Figure 10-7, "C ⊨ ∃σ")
doc = fitz.open(next(ROOT.glob('*.pdf')))
profile(doc[437].get_pixmap(dpi=1200, clip=fitz.Rect(178.0, 76, 186.0, 93.5)), 'BOOK')

# --- Typst candidates, each alone on a page
for nm, expr in (('models', 'models'), ('tack.double', 'tack.double'),
                 ('tack.rrr', 'tack.rrr'), ('bar.v.double', 'bar.v.double')):
    p = ROOT / 'build' / '_p1.typ'
    p.write_text('#import "/templates/preamble.typ": *\n'
                 '#set page(width: 120pt, height: 60pt, margin: 6pt)\n'
                 '#set text(size: 28pt)\n'
                 f'${expr}$\n')
    r = subprocess.run(['typst', 'compile', '--root', str(ROOT), str(p), '/tmp/p1.pdf'],
                       capture_output=True, text=True)
    if r.returncode:
        print(f'{nm}: FAILED')
        continue
    d = fitz.open('/tmp/p1.pdf')
    pg = d[0]
    bb = [s['bbox'] for b in pg.get_text('dict')['blocks'] for l in b.get('lines', [])
          for s in l['spans'] if s['text'].strip()]
    cp = ''.join(s['text'] for b in pg.get_text('dict')['blocks'] for l in b.get('lines', [])
                 for s in l['spans'] if s['text'].strip())
    x0 = min(b[0] for b in bb); x1 = max(b[2] for b in bb)
    y0 = min(b[1] for b in bb); y1 = max(b[3] for b in bb)
    pix = pg.get_pixmap(dpi=1200, clip=fitz.Rect(x0, y0, x1, y1))
    profile(pix, f'{nm:14s} [{cp} U+{ord(cp):04X}]' if len(cp) == 1 else f'{nm:14s} [{cp}]')
