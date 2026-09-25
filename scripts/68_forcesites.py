#!/usr/bin/env python3
"""Find every site where the translation prints `tack` where the book prints the
entailed/forcing relation.

The extractor decoded the book's glyph (2 vertical bars + 1 foot, i.e. U+22A9
`forces`) as U+00F0 in ch10, so the source slices write `ð` there; the target
instead used `tack` (⊢, single bar), which is a DIFFERENT relation (the book uses
⊢ for typing judgments in the same formulas, e.g. `C, Γ ⊢ t : σ`).

For each source site, print the source fragment and the corresponding target
region so each substitution can be checked rather than guessed.
"""
import pathlib, re, json

ROOT = pathlib.Path('/Users/ihor/atapl')
MAN = json.load(open(ROOT / 'manifest.json'))

for part in sorted(p for p in MAN if p.startswith('ch10')):
    src_p = ROOT / 'out' / part / 'source.txt'
    uk_p = ROOT / 'out' / part / 'uk.typ'
    if not (src_p.exists() and uk_p.exists()):
        continue
    src = src_p.read_text(encoding='utf-8')
    n = src.count('\u00f0')
    if not n:
        continue
    print(f'=== {part}: {n} source site(s) with U+00F0')
    for m in re.finditer('\u00f0', src):
        a = max(0, m.start() - 90)
        print(f'    ...{src[a:m.start() + 45]!r}')
