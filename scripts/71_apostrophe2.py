#!/usr/bin/env python3
"""Catch the straight apostrophes the first pass left behind.

scripts/59_apostrophe.py required a Cyrillic letter on BOTH sides of the
apostrophe, so it skipped the ones sitting inside a section/chapter TITLE, where
the apostrophe is followed by a quote character:

    #sec("10.6", "Розв'язування обмежень")     ->  ... "Розв'язування ..."
    #chap("A", "Розв'язки вибраних вправ", "") ->  ... "Розв'язки ...

Here the apostrophe is followed by a Cyrillic letter and preceded by a Cyrillic
letter OR a word-initial position just after a quote/space.  We treat a straight '
as Ukrainian if it is immediately followed by a Cyrillic letter AND the character
before it is either Cyrillic or the opening quote/space that starts a word.

English names such as O'Keefe are protected by requiring that the PRECEDING word
char be Cyrillic (or an opening delimiter) — O'Keefe's preceding char is an ASCII
letter, so it is left alone.
"""
import pathlib, re, sys

ROOT = pathlib.Path('/Users/ihor/atapl')
# NOTE: this must be a REGEX character class. `c in "А-Яа-я..."` would test
# membership in that literal list of characters (А, -, Я, ...) and silently match
# almost nothing, which is why the first run of this script reported 0 sites.
CYR = 'А-Яа-яЇїІіЄєҐґ'
CYR_RE = re.compile(f'[{CYR}]')
APPLY = '--apply' in sys.argv


def strip_math_strings(t):
    """Blank $…$ spans only (quoted strings must stay readable: titles live there)."""
    out = list(t)
    i, n = 0, len(t)
    while i < n:
        if t[i] == '$':
            j = i + 1
            while j < n and t[j] != '$':
                if t[j] == '\\':
                    j += 1
                j += 1
            for k in range(i, min(j + 1, n)):
                if out[k] != '\n':
                    out[k] = ' '
            i = j + 1
        else:
            i += 1
    return ''.join(out)


def fix(text):
    prose = strip_math_strings(text)
    hits = []
    for i, c in enumerate(prose):
        if c != "'":
            continue
        nxt = prose[i + 1] if i + 1 < len(prose) else ''
        if not CYR_RE.match(nxt):
            continue                     # O'Keefe / don't / primes
        prev = prose[i - 1] if i else ''
        if CYR_RE.match(prev) or prev in '«“"([ \n—-':
            hits.append(i)
    if not hits:
        return text, 0
    chars = list(text)
    for i in hits:
        chars[i] = '\u2019'
    return ''.join(chars), len(hits)


total = 0
for p in sorted((ROOT / 'out').glob('*/uk.typ')):
    raw = p.read_text(encoding='utf-8')
    new, n = fix(raw)
    if n:
        print(f'{p.parent.name:9s} {n:3d} site(s){"  -> written" if APPLY else "  (dry)"}')
        if APPLY:
            p.write_text(new, encoding='utf-8')
        total += n
print(f'\n{"rewrote" if APPLY else "would rewrite"} {total} site(s)')
