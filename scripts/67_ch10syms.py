#!/usr/bin/env python3
"""Separate the two ch10 symbols:

  (a) the constraint SATISFACTION predicate written `phi, psi |= C` in prose and
      in rules CM-And / CM-Exists  (ch10p02 sites)
  (b) the turnstile inside the ch10 TYPING JUDGMENTS `C, Gamma |- t : sigma`
      that the extractor decoded as U+00F0 (the Figure 10-7 / 10-8 rules)

They are different glyphs, so measure both from the source: which font draws each,
and how many vertical bars / feet each has.
"""
import fitz, json, pathlib, collections

ROOT = pathlib.Path('/Users/ihor/atapl')
doc = fitz.open(next(ROOT.glob('*.pdf')))
UNITS = json.load(open(ROOT / 'src' / 'units.json'))


def profiles(pix, label):
    w, h, n, s = pix.width, pix.height, pix.n, pix.samples

    def dark(x, y):
        i = y * pix.stride + x * n
        return (s[i] + s[i + 1] + s[i + 2]) / 3 < 128

    cols = [sum(1 for y in range(h) if dark(x, y)) for x in range(w)]
    rows = [sum(1 for x in range(w) if dark(x, y)) for y in range(h)]
    mx, mw = max(cols), max(rows)
    vr, cur, st = [], 0, 0
    for x, c in enumerate(cols):
        if c >= mx * 0.6:
            if not cur:
                st = x
            cur += 1
        elif cur:
            vr.append((st, cur)); cur = 0
    if cur:
        vr.append((st, cur))
    hr, cur, st = [], 0, 0
    for y, c in enumerate(rows):
        if c >= mw * 0.25:
            if not cur:
                st = y
            cur += 1
        elif cur:
            hr.append((st, cur)); cur = 0
    if cur:
        hr.append((st, cur))
    print(f'    {label} ({w}x{h}): {len(vr)} bar(s) {vr} | {len(hr)} foot(s) {hr}')


ch = 'ch10'
a, b = UNITS[ch]['first'], UNITS[ch]['last']
print('=== census of FZ spans containing "|=" or U+00F0 in ch10')
seen = collections.Counter()
for p in range(a, b + 1):
    pg = doc[p]
    for blk in pg.get_text('dict')['blocks']:
        for l in blk.get('lines', []):
            for s in l['spans']:
                t = s['text']
                if '|=' in t:
                    seen['|= spans'] += 1
                if '\u00f0' in t:
                    seen['ð spans'] += 1
print('   ', dict(seen))

# sample: one "|=" site in prose (the satisfaction predicate) on the page where
# it is DEFINED, and one "ð" site inside a ch10 typing judgment.
print('\n=== (a) satisfaction predicate sites ("|=" in prose)')
shown = 0
for p in range(a, b + 1):
    pg = doc[p]
    for blk in pg.get_text('dict')['blocks']:
        for l in blk.get('lines', []):
            txt = ''.join(s['text'] for s in l['spans'])
            if 'satisfaction' in txt.lower() or '|= C' in txt or '|=C' in txt:
                for s in l['spans']:
                    if s['text'].strip() == '|=':
                        bb = s['bbox']
                        profiles(pg.get_pixmap(dpi=1400, clip=fitz.Rect(*bb)),
                                 f'p{p} {s["text"]!r} font={s["font"]}')
                        shown += 1
                        break
            if shown >= 3:
                break
        if shown >= 3:
            break
    if shown >= 3:
        break

print('\n=== (b) typing-judgment glyph (U+00F0) sites')
shown = 0
for p in range(a, b + 1):
    pg = doc[p]
    for blk in pg.get_text('dict')['blocks']:
        for l in blk.get('lines', []):
            for s in l['spans']:
                if '\u00f0' in s['text'] and s['text'].strip() == 'ð':
                    bb = s['bbox']
                    profiles(pg.get_pixmap(dpi=1400, clip=fitz.Rect(*bb)),
                             f'p{p} {s["text"]!r} font={s["font"]}')
                    shown += 1
                    break
            if shown >= 3:
                break
        if shown >= 3:
            break
    if shown >= 3:
        break
