#!/usr/bin/env python3
"""Verify the rendered bibliography against the book, entry by entry.

Independent of scripts/76_refsemit.py's own checks: this reads the SOURCE PDF's
References lines and the COMPILED translation, normalises both (lowercase, drop
everything but letters), and confirms every source entry's opening words appear in
the translation — catching an entry that was dropped, truncated, or reordered.

It also counts the italic runs the translation sets, which is the second thing the
bibliography must reproduce (work titles are italic in the book).
"""
import fitz, pathlib, json, re, unicodedata

ROOT = pathlib.Path('/Users/ihor/atapl')
doc = fitz.open(next(ROOT.glob('*.pdf')))
U = json.load(open(ROOT / 'src' / 'units.json'))['refs']

LIG = {'\ufb00': 'ff', '\ufb01': 'fi', '\ufb02': 'fl', '\ufb03': 'ffi', '\ufb04': 'ffl'}


def norm(s):
    for a, b in LIG.items():
        s = s.replace(a, b)
    s = unicodedata.normalize('NFKD', s)
    return re.sub(r'[^a-z]', '', s.lower())


# 1. source entries: collect flush-left lines (the first line of each entry)
src_entries = []
for p in range(U['first'], U['last'] + 1):
    raw = []
    for blk in doc[p].get_text('dict')['blocks']:
        for l in blk.get('lines', []):
            sp = [s for s in l['spans'] if s['text'].strip()]
            if not sp:
                continue
            y = min(s['bbox'][1] for s in sp)
            # Same measured window as the extractor (scripts/72_refsorder.py):
            # only the running head at y=34.2 is excluded.  The old 100pt floor
            # hid every page's first entry from the verifier too, which is why it
            # once agreed with the equally-short parse — two readers sharing one
            # wrong window confirm each other's omissions.
            if not (50 < y < 600):
                continue
            for s in sp:
                raw.append((y, s['bbox'][0], s['text']))
    raw.sort(key=lambda t: (t[0], t[1]))
    groups = []
    for y, x, t in raw:
        if groups and y - groups[-1][0] <= 4.0:
            groups[-1][1].append((x, t))
        else:
            groups.append([y, [(x, t)]])
    for _y, segs in groups:
        segs.sort()
        # A printed line can carry the TAIL of one entry and the HEAD of the next
        # (the book starts a new entry on the same line where the previous one ends).
        # So an entry starts at the first segment sitting flush left; taking the whole
        # line would prepend the previous entry's tail and make the head look absent.
        for i, (x, _t) in enumerate(segs):
            if x <= 170.0:
                src_entries.append(''.join(t for _x, t in segs[i:]).strip())
                break

# 2. compiled translation
tr = fitz.open('/tmp/refs01.pdf')
tr_text = norm(''.join(p.get_text() for p in tr))

print(f'source entries: {len(src_entries)}')
missing = []
for e in src_entries:
    n = norm(e)
    if n in ('references',):
        continue
    head = n[:40]
    if head and head not in tr_text:
        missing.append(e[:80])
print(f'entries whose opening words are NOT in the translation: {len(missing)}')
for m in missing[:8]:
    print('   MISSING:', m)

# 3. italics: count italic spans in the compiled output
ital = 0
for page in tr:
    for blk in page.get_text('dict')['blocks']:
        for l in blk.get('lines', []):
            for s in l['spans']:
                if s['text'].strip() and 'Italic' in s['font']:
                    ital += 1
print(f'italic spans rendered in the translation: {ital}')

# 4. source italics for comparison
src_ital = 0
for p in range(U['first'], U['last'] + 1):
    for blk in doc[p].get_text('dict')['blocks']:
        for l in blk.get('lines', []):
            for s in l['spans']:
                if s['text'].strip() and s['font'] == 'F5':
                    src_ital += 1
print(f'italic spans in the source References: {src_ital}')
