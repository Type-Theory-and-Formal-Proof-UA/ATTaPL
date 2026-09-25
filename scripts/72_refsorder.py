#!/usr/bin/env python3
"""Re-extract the References in reading order, splitting entries correctly.

The first attempt (scripts/_refsorder.py) used one flush-left threshold and so
GLUED entries together at page boundaries: the last entry on a page and the first
on the next one were joined into a single line, producing text like

    ... In International Symposium on Garrigue, Jacques. Relaxing the value ...

Measured layout: entries begin flush at x=163/167 and continuation lines indent to
x=173/177.  So an entry boundary is "starts at x <= 170", and the very first line
of a page whose x sits in the indent band belongs to the PREVIOUS entry only if it
continues a sentence — otherwise it begins a new entry.

Rather than guessing, this uses the 4pt gap directly: a line at x<170 starts an
entry; x>=170 continues.  That is exactly the rule the earlier script claimed to
use, but its threshold (FIRST_X + 2 = 168.7) fell between 167 and 173, so lines at
x=173 (continuations) were sometimes treated as starts.  Here the split is 170.
"""
import fitz, json, pathlib, re

ROOT = pathlib.Path('/Users/ihor/atapl')
doc = fitz.open(next(ROOT.glob('*.pdf')))
U = json.load(open(ROOT / 'src' / 'units.json'))['refs']

START_MAX_X = 170.0          # flush-left entries: 163, 167; continuations: 173, 177


def page_lines(p):
    """Group spans into VISUAL LINES keyed by y, then take each line's minimum x.

    The bug in the earlier versions: within one visual line the spans arrive in
    stream order, which may list a mid-line segment (e.g. a continuation of the
    previous entry sharing the line) BEFORE the flush-left segment that actually
    starts the next entry.  Recording the FIRST span's x then mis-classifies the
    line and glues two references together (the "GNU. ... Goguen, Healfdene."
    case).  So the classification must use the line's MINIMUM x.
    """
    by_y = {}
    for blk in doc[p].get_text('dict')['blocks']:
        for l in blk.get('lines', []):
            sp = [s for s in l['spans'] if s['text'].strip()]
            if not sp:
                continue
            y = round(min(s['bbox'][1] for s in sp), 1)
            x = min(s['bbox'][0] for s in sp)
            # Running head ("References" + folio) sits at y=34.2 and must be
            # skipped; the BODY starts at y=67.5 and runs to 569.8 on a 648pt
            # page.  The window was (100, 620), which swallowed the HEAD LINE of
            # the first entry on every page (they all start at y=67.5) and lost
            # 5 whole entries whose heads landed there.  Measured bounds instead.
            if y < 50 or y > 600:
                continue
            # snap to a 5pt bucket so the same visual line merges
            key = round(y / 5)
            got = by_y.setdefault(key, [y, x, []])
            got[0] = min(got[0], y)
            got[1] = min(got[1], x)
            got[2].append((x, ''.join(s['text'] for s in sp).strip()))
    out = []
    for key in sorted(by_y):
        y, xmin, segs = by_y[key]
        segs.sort()                      # left-to-right within the line
        text = ' '.join(t for x, t in segs)
        out.append((y, xmin, text))
    return out


entries, cur = [], []
for p in range(U['first'], U['last'] + 1):
    for y, x, t in page_lines(p):
        if x <= START_MAX_X:
            if cur:
                entries.append(' '.join(cur))
            cur = [t]
        else:
            cur.append(t)
if cur:
    entries.append(' '.join(cur))

clean = []
for e in entries:
    e = re.sub(r'-\s+', '', e)                 # join hyphenated breaks
    e = re.sub(r'\s+', ' ', e).strip()
    clean.append(e)

# drop the section heading if present
if clean and clean[0].strip().lower() in ('references',):
    clean = clean[1:]

out = ROOT / 'out' / 'refs01' / 'ordered2.txt'
out.write_text('\n\n'.join(clean), encoding='utf-8')
print('entries:', len(clean))
# report the previously-glued cases
susp = [e for e in clean if re.search(r'\.\s+[A-Z][a-z]+,\s+[A-Z]', e) and e.count('. ') > 4]
print('entries that may still glue two references:', len(susp))
for e in susp[:6]:
    print('   ', e[:150])
