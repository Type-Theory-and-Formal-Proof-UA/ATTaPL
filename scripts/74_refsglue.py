#!/usr/bin/env python3
"""Find glued entries in the already-written bibliography parts.

The parts were produced from the OLD extraction (374 entries), which glued
entries at page boundaries; the corrected extraction has 400.  A glued entry shows
two reference starts inside one #refentry: a "Surname." / "Surname," that is NOT at
the very beginning and is followed by a title-like capitalised phrase.
"""
import pathlib, re, sys

ROOT = pathlib.Path('/Users/ihor/atapl')
# a new reference start looks like: ". Name, X." or " Name, X and Y." mid-entry
START = re.compile(r"[.!?]\s+([A-Z][a-zA-ZÀ-ÿ’'\-]+),\s+([A-Z][a-zA-ZÀ-ÿ’'\-]*\.?)\s")

for n in sys.argv[1:] or ['1', '3', '4']:
    p = ROOT / 'out' / 'refs01' / f'_part{n}.typ'
    if not p.exists():
        print(f'part{n}: missing')
        continue
    t = p.read_text(encoding='utf-8')
    entries = re.findall(r'#refentry\[(.*?)\]\s*(?=#refentry|\Z)', t, re.S)
    print(f'=== part{n}: {len(entries)} #refentry blocks')
    sus = []
    for i, e in enumerate(entries):
        e1 = ' '.join(e.split())
        for m in START.finditer(e1):
            # ignore well-known in-title patterns
            tail = e1[m.end():m.end() + 60]
            if re.match(r'(editors?|In|and|volume|pages|PhD|Technical|Research)\b', tail):
                continue
            sus.append((i, m.start(), e1[max(0, m.start() - 60):m.end() + 70]))
            break
    print(f'   suspicious (two reference starts): {len(sus)}')
    for i, pos, frag in sus[:8]:
        print(f'     #{i}: ...{frag}')
