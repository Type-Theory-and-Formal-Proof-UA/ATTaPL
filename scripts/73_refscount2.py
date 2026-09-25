#!/usr/bin/env python3
"""Independently count the references by their flush-left lines.

Each entry begins with a SURNAME, so an entry boundary is a line that starts at
x<=170 whose first word is followed by a comma or period.  This is a different
signal from scripts/72_refsorder.py (which uses x only), so agreement between the
two counts is real evidence the split is right.
"""
import fitz, json, pathlib, re

ROOT = pathlib.Path('/Users/ihor/atapl')
doc = fitz.open(next(ROOT.glob('*.pdf')))
U = json.load(open(ROOT / 'src' / 'units.json'))['refs']

flush = 0
names = 0
for p in range(U['first'], U['last'] + 1):
    by_y = {}
    for blk in doc[p].get_text('dict')['blocks']:
        for l in blk.get('lines', []):
            sp = [s for s in l['spans'] if s['text'].strip()]
            if not sp:
                continue
            y = min(s['bbox'][1] for s in sp)
            x = min(s['bbox'][0] for s in sp)
            if not (100 < y < 620):
                continue
            key = round(y / 5)
            got = by_y.setdefault(key, [y, x, []])
            got[1] = min(got[1], x)
            got[2].append((x, ''.join(s['text'] for s in sp).strip()))
    for key in sorted(by_y):
        y, xmin, segs = by_y[key]
        segs.sort()
        text = ' '.join(t for x, t in segs)
        if xmin <= 170:
            flush += 1
            if re.match(r"^[A-Za-zÀ-ÿ’'\-]+[,. ]", text):
                names += 1

print(f'flush-left lines (x<=170): {flush}')
print(f'  of which begin "Name," or "Name.": {names}')
E = [e for e in (ROOT / 'out' / 'refs01' / 'ordered2.txt').read_text().split('\n\n') if e.strip()]
print(f'scripts/72_refsorder.py entries: {len(E)}')
