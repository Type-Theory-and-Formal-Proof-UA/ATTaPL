#!/usr/bin/env python3
"""Render the book's entailment glyph and the Typst candidates as ASCII maps.

Vision kept failing here because large images get downscaled and the bar detail
disappears.  An ASCII map is rendered from the pixels directly, so the shape is
settled by measurement and stays legible in a terminal.
"""
import fitz, pathlib, subprocess, sys

ROOT = pathlib.Path('/Users/ihor/atapl')


def ascii_map(png_or_pix, cols=54, aspect=0.5):
    pix = fitz.Pixmap(str(png_or_pix)) if isinstance(png_or_pix, pathlib.Path) else png_or_pix
    w, h, n, s = pix.width, pix.height, pix.n, pix.samples
    rows = max(3, int(cols * aspect * h / w))
    out = []
    for ry in range(rows):
        line = []
        for rx in range(cols):
            x0, x1 = int(rx * w / cols), max(int(rx * w / cols) + 1, int((rx + 1) * w / cols))
            y0, y1 = int(ry * h / rows), max(int(ry * h / rows) + 1, int((ry + 1) * h / rows))
            dark = tot = 0
            for y in range(y0, min(y1, h)):
                for x in range(x0, min(x1, w)):
                    i = y * pix.stride + x * n
                    tot += 1
                    if (s[i] + s[i + 1] + s[i + 2]) / 3 < 128:
                        dark += 1
            f = dark / tot if tot else 0
            line.append('#' if f > 0.5 else ('+' if f > 0.22 else ('.' if f > 0.06 else ' ')))
        out.append(''.join(line))
    return out


print('=' * 60)
print('BOOK: page 437, Figure 10-7 first rule  "C <sym> exists sigma"')
doc = fitz.open(next(ROOT.glob('*.pdf')))
# generous crop around the glyph only: C ends ~x=176, exists begins ~x=190
pix = doc[437].get_pixmap(dpi=1200, clip=fitz.Rect(177.0, 76.0, 190.0, 94.0))
pix.save(ROOT / 'raw' / 'crops' / 'ent_book_map.png')
for l in ascii_map(pix):
    print('   |' + l + '|')

for name, expr in (('models', 'models'), ('tack.double', 'tack.double'),
                   ('forces', 'forces'), ('bar.v.double', 'bar.v.double')):
    p = ROOT / 'build' / '_pmap.typ'
    p.write_text('#import "/templates/preamble.typ": *\n'
                 '#set page(width: 60pt, height: 40pt, margin: 4pt)\n'
                 '#set text(size: 22pt)\n'
                 f'${expr}$\n')
    r = subprocess.run(['typst', 'compile', '--root', str(ROOT), str(p), '/tmp/pmap.pdf'],
                       capture_output=True, text=True)
    if r.returncode:
        print(f'\n{name}: FAILED')
        continue
    d = fitz.open('/tmp/pmap.pdf')
    pg = d[0]
    spans = [s for b in pg.get_text('dict')['blocks'] for l in b.get('lines', [])
             for s in l['spans'] if s['text'].strip()]
    cp = ''.join(s['text'] for s in spans)
    x0 = min(s['bbox'][0] for s in spans); x1 = max(s['bbox'][2] for s in spans)
    y0 = min(s['bbox'][1] for s in spans); y1 = max(s['bbox'][3] for s in spans)
    p2 = pg.get_pixmap(dpi=1200, clip=fitz.Rect(x0, y0, x1, y1))
    print('=' * 60)
    print(f'TYPST {name}  ->  {cp!r}  ' + ' '.join(f'U+{ord(c):04X}' for c in cp))
    for l in ascii_map(p2):
        print('   |' + l + '|')
