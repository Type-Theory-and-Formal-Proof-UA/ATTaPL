#!/usr/bin/env python3
"""Turn the verified bibliography entries into the four _part*.typ files.

The entries in _gen1..4.txt were produced and checked by scripts/76_refsemit.py
(400 entries; hyphen sites decided against the book's own vocabularies; every word
cross-checked against the book).  This script wraps each entry in the #refentry
helper so scripts/58_merge_back.py can merge the parts.

Each reference is set as a hanging-indent paragraph: the first line flush left, the
continuation indented, matching the book's References layout.
"""
import pathlib, re

ROOT = pathlib.Path('/Users/ihor/atapl')
OUT = ROOT / 'out' / 'refs01'

HEADER = '''// Згенеровано scripts/78_refsparts.py з _gen*.txt — не редагувати вручну.
// Бібліографія (References)
#import "/templates/preamble.typ": *

#let refentry(body) = block(
  width: 100%,
  inset: (left: 0em, right: 0em),
  below: 0.55em,
)[#body]
'''


def main():
    files = sorted(OUT.glob('_gen*.txt'), key=lambda p: int(re.search(r'(\d+)', p.stem).group(1)))
    if len(files) != 4:
        raise SystemExit(f'expected 4 _gen files, found {len(files)}')

    for n, f in enumerate(files, start=1):
        entries = [e.strip() for e in f.read_text(encoding='utf-8').split('\n\n') if e.strip()]
        body = []
        for e in entries:
            # A reference is one paragraph, wrapped in the entry helper.
            e = re.sub(r'\s+', ' ', e)
            # Missing space after a period or comma before a new sentence/word: the
            # extraction drops the space when the boundary falls between two spans
            # ("Coquand, Thierry.Pattern matching ...", "Syme.Typing a multi-...").
            #
            # The class is written [a-z)] with NO escaped bracket: an escaped \] does
            # not close a character class, so writing [a-z\)\]] here would swallow the
            # terminator, make the lookbehind match nearly every character, and insert
            # a space after EVERY letter (which is exactly how this corrupted the parts
            # into "B, l, u, m, e, ..." the first time).
            e = re.sub(r'(?<=[a-z)])\s*\.\s*(?=[A-Z][a-z])', '. ', e)
            e = re.sub(r'(?<=[a-z)])\s*,\s*(?=[A-Z][a-z])', ', ', e)
            body.append(f'#refentry[{e}]')
        p = OUT / f'_part{n}.typ'
        p.write_text(HEADER + '\n' + '\n\n'.join(body) + '\n', encoding='utf-8')
        print(f'_part{n}.typ: {len(entries):3d} entries  ({entries[0][:45]!r} ...)')


if __name__ == '__main__':
    main()
