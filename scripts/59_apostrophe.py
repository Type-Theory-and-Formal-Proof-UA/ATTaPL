#!/usr/bin/env python3
"""Rewrite straight apostrophes INSIDE Ukrainian words to ’ (U+2019).

STYLE.md §181 requires U+2019 in Ukrainian prose.  A blanket replace is wrong:
the straight apostrophe is legitimate as an OCaml identifier prime (tm1'), in
rule names (hmx-Inst'), and in English surnames (O'Keefe), and inside $…$ math or
"…" strings it may be meaningful.  So we rewrite only where a straight ' sits
between two Cyrillic letters in content-mode prose — outside math spans and
outside quoted strings.

  python3 scripts/59_apostrophe.py --apply      (dry run without --apply)
"""
import pathlib, re, sys

ROOT = pathlib.Path('/Users/ihor/atapl')
CYR = 'А-Яа-яЇїІіЄєҐґ'
APPLY = '--apply' in sys.argv


def strip_math_strings(t):
    """Blank out $…$ and "…" spans (keep newlines) so only prose is matched."""
    out = list(t)
    i, n = 0, len(t)
    while i < n:
        c = t[i]
        if c in '$"':
            q, j = c, i + 1
            while j < n and t[j] != q:
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
    for m in re.finditer(r"'", prose):
        i = m.start()
        if re.search(f'[{CYR}]', prose[max(0, i - 2):i]) and \
           re.search(f'[{CYR}]', prose[i + 1:i + 3]):
            hits.append(i)
    if not hits:
        return text, 0
    chars = list(text)
    for i in hits:
        chars[i] = '\u2019'
    return ''.join(chars), len(hits)


total = 0
for part in sorted(p.name for p in (ROOT / 'out').iterdir() if p.is_dir()):
    p = ROOT / 'out' / part / 'uk.typ'
    if not p.exists():
        continue
    raw = p.read_text(encoding='utf-8')
    new, n = fix(raw)
    if n:
        print(f'{part:9s} {n:4d} sites{"  -> written" if APPLY else "  (dry)"}')
        if APPLY:
            (ROOT / 'out' / part / 'uk.typ.bak-apo').write_text(raw, encoding='utf-8')
            p.write_text(new, encoding='utf-8')
        total += n
print(f'\n{"rewrote" if APPLY else "would rewrite"} {total} apostrophes')
