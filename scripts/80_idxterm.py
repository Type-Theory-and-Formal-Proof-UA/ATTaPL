#!/usr/bin/env python3
"""Unify the term for *value restriction* with the chapters' rendering.

scripts/59_apostrophe.py-style one-off: the index (out/index01/uk.typ) renders the
term as "обмеження значень" while ch07p03 and ch10p03 — the chapters that DEFINE it —
render "обмеження на значення" (ch10p03 line 572 introduces it: "синтаксичного
обмеження, відомого як обмеження на значення (Wright, 1995)").  The index entry is
the key a reader follows to that definition, so it must carry the same wording; the
minority spelling is also the one that drops the preposition the term needs.

Only the exact index phrasings are rewritten, and the file is recompiled after.
"""
import pathlib, re, subprocess, sys

ROOT = pathlib.Path('/Users/ihor/atapl')
APPLY = '--apply' in sys.argv
TARGET = ROOT / 'out' / 'index01' / 'uk.typ'

# exact phrasings used in the index (main entry and its sub-entry)
SUBS = [
    ('обмеження значень і поліморфізм', 'обмеження на значення і поліморфізм'),
    ('обмеження значень', 'обмеження на значення'),
]

t = TARGET.read_text(encoding='utf-8')
total = 0
for old, new in SUBS:
    n = t.count(old)
    if n:
        print(f'  {old!r} -> {new!r}   x{n}')
        total += n
        t = t.replace(old, new)

if not total:
    print('nothing to change')
    sys.exit(0)
print(f'would rewrite {total} site(s)' + ('' if not APPLY else ' — applying'))

if APPLY:
    TARGET.write_text(t, encoding='utf-8')
    r = subprocess.run(['typst', 'compile', '--root', str(ROOT), str(TARGET), '/tmp/idxterm.pdf'],
                       capture_output=True, text=True)
    print('compile:', 'ok' if r.returncode == 0 else 'FAIL')
    if r.returncode != 0:
        print(r.stderr[:400])
    # read the rendered text back
    import fitz
    txt = ''.join(p.get_text() for p in fitz.open('/tmp/idxterm.pdf'))
    print('renders "обмеження на значення":', txt.count('обмеження на значення'))
    print('renders stray "обмеження значень":', txt.count('обмеження значень'))
