#!/usr/bin/env python3
"""Settle the ch10 entailment glyph: which font draws it, and its exact structure.

Two independent facts are needed:
  A) the FONT the symbol is drawn with, its glyph inventory, and how many spans
     use it (so a single measurement covers every site);
  B) its exact row/column dark-pixel profile at high resolution, compared with
     Typst's `forces` (U+22A9), `models` (U+22A7) and `tack.double` (U+22A8).
"""
import fitz, json, pathlib, subprocess, collections

ROOT = pathlib.Path('/Users/ihor/atapl')
doc = fitz.open(next(ROOT.glob('*.pdf')))
UNITS = json.load(open(ROOT / 'src' / 'units.json'))

# ---------- A) which font draws the 'ð' spans in ch10?
ch = 'ch10'
a, b = UNITS[ch]['first'], UNITS[ch]['last']
perfont = collections.defaultdict(collections.Counter)
spans = []
for p in range(a, b + 1):
    for blk in doc[p].get_text('dict')['blocks']:
        for l in blk.get('lines', []):
            for s in l['spans']:
                if '\u00f0' in s['text']:
                    perfont[s['font']].update(s['text'])
                    spans.append((p, round(s['bbox'][0], 1), round(s['bbox'][1], 1), s['font']))
print('=== A) fonts used for the U+00F0 span:')
for f, c in perfont.items():
    print(f'   font={f!r} chars={dict(c)}')
print(f'   spans found: {len(spans)}; first few: {spans[:5]}')
# glyph inventory of those fonts
fonts_used = set(perfont)
inv = collections.defaultdict(set)
for p in range(a, b + 1):
    for blk in doc[p].get_text('dict')['blocks']:
        for l in blk.get('lines', []):
            for s in l['spans']:
                if s['font'] in fonts_used:
                    inv[s['font']].update(s['text'])
for f, chars in inv.items():
    print(f'   INV font={f!r} distinct={len(chars)} -> {sorted(chars)[:20]}')


# ---------- B) structure: column profile and row profile
def profiles(pix, label):
    w, h, n, s = pix.width, pix.height, pix.n, pix.samples

    def dark(x, y):
        i = y * pix.stride + x * n
        return (s[i] + s[i + 1] + s[i + 2]) / 3 < 128

    cols = [sum(1 for y in range(h) if dark(x, y)) for x in range(w)]
    rows = [sum(1 for x in range(w) if dark(x, y)) for y in range(h)]
    print(f'--- {label}  ({w}x{h}px)')
    # vertical stroke columns: >= 60% of the glyph height
    mx = max(cols)
    print('    COLUMN profile (bars):')
    runs, cur, start = [], 0, 0
    for x, c in enumerate(cols):
        if c >= mx * 0.6:
            if not cur:
                start = x
            cur += 1
        elif cur:
            runs.append((start, cur))
            cur = 0
    if cur:
        runs.append((start, cur))
    print(f'      {len(runs)} tall column run(s): {runs}')
    # horizontal stroke rows: >= 25% of the glyph width
    mw = max(rows)
    hruns, cur, start = [], 0, 0
    for y, c in enumerate(rows):
        if c >= mw * 0.25:
            if not cur:
                start = y
            cur += 1
        elif cur:
            hruns.append((start, cur))
            cur = 0
    if cur:
        hruns.append((start, cur))
    print(f'      {len(hruns)} wide row run(s) (feet): {hruns}')


# the book glyph (page 437, tight around the symbol: x 180.5..187, y 82.5..90)
profiles(doc[437].get_pixmap(dpi=1400, clip=fitz.Rect(180.5, 82.5, 187.0, 90.0)), 'BOOK ch10 p437')

for name, expr in (('forces', 'forces'), ('models', 'models'), ('tack.double', 'tack.double')):
    p = ROOT / 'build' / '_pprof.typ'
    p.write_text('#import "/templates/preamble.typ": *\n'
                 '#set page(width: 60pt, height: 40pt, margin: 5pt)\n'
                 '#set text(size: 24pt)\n'
                 f'${expr}$\n')
    r = subprocess.run(['typst', 'compile', '--root', str(ROOT), str(p), '/tmp/pp.pdf'],
                       capture_output=True, text=True)
    if r.returncode:
        print(f'{name}: FAILED')
        continue
    d = fitz.open('/tmp/pp.pdf')
    pg = d[0]
    ss = [s for bl in pg.get_text('dict')['blocks'] for l in bl.get('lines', [])
          for s in l['spans'] if s['text'].strip()]
    cp = ''.join(s['text'] for s in ss)
    bbox = fitz.Rect(min(s['bbox'][0] for s in ss), min(s['bbox'][1] for s in ss),
                     max(s['bbox'][2] for s in ss), max(s['bbox'][3] for s in ss))
    profiles(pg.get_pixmap(dpi=1400, clip=bbox), f'TYPST {name} {cp!r} U+{ord(cp):04X}')
