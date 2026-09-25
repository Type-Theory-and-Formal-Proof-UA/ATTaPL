#!/usr/bin/env python3
"""Report, per ch10 part, every `tack` site and whether the source at that place
prints the ENTAILMENT glyph (U+00F0 in the extractor, really U+22A9) or a genuine
typing turnstile (⊢ U+22A2, extracted correctly).

Pairing source and target site-by-site is unreliable after translation, so we
count instead: the source has N entailment glyphs, and a correct translation must
contain N occurrences of the `forces` spelling, with `tack` reserved for typing.
"""
import pathlib, re, json

ROOT = pathlib.Path('/Users/ihor/atapl')
MAN = json.load(open(ROOT / 'manifest.json'))

tot_src = tot_uk = 0
for part in sorted(p for p in MAN if p.startswith('ch10') or p.startswith('appap03')):
    src_p = ROOT / 'out' / part / 'source.txt'
    uk_p = ROOT / 'out' / part / 'uk.typ'
    if not uk_p.exists():
        continue
    src = src_p.read_text(encoding='utf-8') if src_p.exists() else ''
    uk = uk_p.read_text(encoding='utf-8')
    n_src = src.count('\u00f0')
    n_forces = len(re.findall(r'\bforces\b', uk))
    n_tack = len(re.findall(r'\btack\b', uk))
    tot_src += n_src
    tot_uk += n_forces
    flag = 'OK' if n_src == n_forces else 'MISMATCH'
    print(f'{part:9s} src-entail={n_src:3d}  uk-forces={n_forces:3d}  '
          f'uk-tack={n_tack:3d}  {flag}')
print(f'\nTOTAL src-entail={tot_src}  uk-forces={tot_uk}')
