#!/usr/bin/env python3
"""Find which Typst symbol reproduces the book's entailment glyph.

Measured facts: the book prints TWO vertical bars joined by a right-pointing
horizontal foot.  Typst's `models` (U+22A7) and `tack.double` (U+22A8) both render
with ONE vertical in this font, so we enumerate the turnstile family, render each
candidate, and measure its vertical-bar and horizontal-stroke counts, reporting
every symbol whose shape matches (2 verticals, >=1 horizontal).
"""
import fitz, pathlib, subprocess

ROOT = pathlib.Path('/Users/ihor/atapl')

CANDIDATES = [
    'tack', 'tack.r', 'tack.l', 'tack.t', 'tack.b', 'tack.r.long', 'tack.l.long',
    'tack.r.double', 'tack.rr', 'tack.ll', 'tack.rrr', 'tack.rrl', 'tack.r.double.long',
    'models', 'models.not', 'models.r', 'models.l',
    'bar.v', 'bar.v.double', 'bar.v.triple', 'bar.v.double.bar',
    'proves', 'entails', 'forces', 'satisfies', 'vDash', 'true',
    'tack.r.bar', 'tack.bar.r', 'tack.bar',
]


def measure(pix):
    """(n_vertical_bars, n_horizontal_strokes) of the glyph in a pixmap."""
    w, h, n, s = pix.width, pix.height, pix.n, pix.samples

    def dark(x, y):
        i = y * pix.stride + x * n
        return (s[i] + s[i + 1] + s[i + 2]) / 3 < 128

    cols = [sum(1 for y in range(h) if dark(x, y)) for x in range(w)]
    rows = [sum(1 for x in range(w) if dark(x, y)) for y in range(h)]
    # vertical bars: narrow columns that are nearly full height
    full = max(cols) if cols else 0
    vb, cur = 0, 0
    for c in cols:
        if c >= full * 0.75:
            cur += 1
        elif cur:
            vb += 1
            cur = 0
    if cur:
        vb += 1
    # horizontal strokes: rows that are much wider than a bar is thick
    barw = max((cols[i] for i in range(w)), default=0)
    wide = max(rows) if rows else 0
    hs, cur = 0, 0
    for r in rows:
        if r >= wide * 0.45:
            cur += 1
        elif cur:
            hs += 1
            cur = 0
    if cur:
        hs += 1
    return vb, hs


results = []
for name in CANDIDATES:
    p = ROOT / 'build' / '_psym.typ'
    p.write_text('#import "/templates/preamble.typ": *\n'
                 '#set page(width: 140pt, height: 70pt, margin: 6pt)\n'
                 '#set text(size: 30pt)\n'
                 f'${name}$\n')
    r = subprocess.run(['typst', 'compile', '--root', str(ROOT), str(p), '/tmp/ps.pdf'],
                       capture_output=True, text=True)
    if r.returncode:
        results.append((name, None, None, 'unknown'))
        continue
    d = fitz.open('/tmp/ps.pdf')
    pg = d[0]
    spans = [s for b in pg.get_text('dict')['blocks'] for l in b.get('lines', [])
             for s in l['spans'] if s['text'].strip()]
    if not spans:
        results.append((name, None, None, 'blank'))
        continue
    cp = ''.join(s['text'] for s in spans)
    x0 = min(s['bbox'][0] for s in spans); x1 = max(s['bbox'][2] for s in spans)
    y0 = min(s['bbox'][1] for s in spans); y1 = max(s['bbox'][3] for s in spans)
    pix = pg.get_pixmap(dpi=900, clip=fitz.Rect(x0, y0, x1, y1))
    vb, hs = measure(pix)
    results.append((name, vb, hs, cp))

print(f'{"symbol":22s} {"vbars":>5s} {"hstr":>4s}  codepoints')
for name, vb, hs, cp in results:
    cps = ' '.join(f'U+{ord(c):04X}' for c in cp)
    mark = '  <== MATCH' if (vb == 2 and (hs or 0) >= 1) else ''
    print(f'{name:22s} {str(vb):>5s} {str(hs):>4s}  {cps}{mark}')

print('\nbook glyph measured earlier: vbars=2, hstrokes=1')
