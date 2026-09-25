#!/usr/bin/env python3
"""Measure the entailment glyph the book prints at the ch02 and ch05 sites.

These sites decode as two ASCII chars `|=` while ch10's decoded as a single 'ð',
so they may be drawn differently (or by a different font).  For each site we
locate the spans, then measure the vertical-bar and foot structure of the glyph.
"""
import fitz, json, pathlib, collections

ROOT = pathlib.Path('/Users/ihor/atapl')
doc = fitz.open(next(ROOT.glob('*.pdf')))
UNITS = json.load(open(ROOT / 'src' / 'units.json'))

SITES = [('ch02', 93, 'DML-K-App'), ('ch02', 94, 'DML-QIA-App'), ('ch05', 214, '|=M')]


def profiles(pix, label):
    w, h, n, s = pix.width, pix.height, pix.n, pix.samples

    def dark(x, y):
        i = y * pix.stride + x * n
        return (s[i] + s[i + 1] + s[i + 2]) / 3 < 128

    cols = [sum(1 for y in range(h) if dark(x, y)) for x in range(w)]
    rows = [sum(1 for x in range(w) if dark(x, y)) for y in range(h)]
    mx, mw = max(cols), max(rows)
    vruns, cur, st = [], 0, 0
    for x, c in enumerate(cols):
        if c >= mx * 0.6:
            if not cur:
                st = x
            cur += 1
        elif cur:
            vruns.append((st, cur))
            cur = 0
    if cur:
        vruns.append((st, cur))
    hruns, cur, st = [], 0, 0
    for y, c in enumerate(rows):
        if c >= mw * 0.25:
            if not cur:
                st = y
            cur += 1
        elif cur:
            hruns.append((st, cur))
            cur = 0
    if cur:
        hruns.append((st, cur))
    print(f'    {label} ({w}x{h}px): {len(vruns)} bar(s) {vruns}, '
          f'{len(hruns)} foot(s) {hruns}')


for ch, page, needle in SITES:
    print(f'=== {ch} page {page} ({needle})')
    pg = doc[page]
    # find the spans forming this glyph
    for blk in pg.get_text('dict')['blocks']:
        for l in blk.get('lines', []):
            txt = ''.join(s['text'] for s in l['spans'])
            if needle not in txt and '|=' not in txt and 'ð' not in txt:
                continue
            for s in l['spans']:
                if s['text'].strip() in ('|', '=', '|=', 'ð'):
                    print(f'    span {s["text"]!r} font={s["font"]!r} '
                          f'bbox=({s["bbox"][0]:.1f},{s["bbox"][1]:.1f},{s["bbox"][2]:.1f},{s["bbox"][3]:.1f})')
                    bb = s['bbox']
                    if bb[2] > bb[0] and bb[3] > bb[1]:
                        profiles(pg.get_pixmap(dpi=1400, clip=fitz.Rect(*bb)),
                                 f'glyph {s["text"]!r}')
                    break
            break
