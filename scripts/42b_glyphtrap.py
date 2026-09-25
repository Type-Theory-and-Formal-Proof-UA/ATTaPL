#!/usr/bin/env python3
"""Glyph census for the uk translation: flags Typst spellings whose RENDERED glyph
is known to differ from what the book prints, plus leaked source syntax.

Usage: python3 scripts/42b_glyphtrap.py [part ...]   (default: all out/*/uk.typ)
"""
import pathlib, re, sys

# spelling -> (expected rendered glyph, note)
TRAPS = {
    'bar(':        ('|X| absolute bars', 'book overline is `macron(` (X̄) — NEVER `bar(`'),
    'prec.eq.slant': ('unknown modifier / error', 'use prec.eq for ⪯'),
    'otimes':      ('unknown variable', 'use the literal ⊗ character'),
    'circ':        ('unknown variable', 'white bullet ◦ is `bullet.stroked`'),
    'sect':        ('unknown variable', 'intersection is `inter`'),
    'arrow.u':     ('unknown modifier', 'up arrow is `arrow.t`'),
    'circumflex':  ('unknown', 'circle op ∘ is `compose`'),
    'hash':        ('#\\ufe0e artifact', 'OK but adds a variation selector; prefer macron(X) hash ... only inside math'),
    'prec.eq.double': ('unknown modifier', 'use prec.eq'),
}

LEAKS = [r'\$[^$]*\$', r'#[a-zA-Z]+\(', r'\braw\(', r'\bfigure\(', r'\brule\(']

def main(parts):
    root = pathlib.Path('/Users/ihor/atapl')
    files = [root / f'out/{p}/uk.typ' for p in parts] if parts else sorted(root.glob('out/*/uk.typ'))
    bad = 0
    for f in files:
        if not f.exists():
            print(f"MISSING {f}")
            continue
        t = f.read_text()
        hits = []
        for spelling, (rendered, note) in TRAPS.items():
            if spelling == 'hash':
                continue  # informational only
            # Skip occurrences inside a quoted string ("circ") — those are literal text.
            # Require a WORD BOUNDARY: a bare substring match fires on ordinary words
            # ("Inter+sect+ion" looked like a stray `sect` symbol), so the pattern is
            # anchored on a non-letter before and after.
            pat = r'(?<![A-Za-z])' + re.escape(spelling) + r'(?![A-Za-z])'
            n = len(re.findall(pat, t))
            n -= len(re.findall(r'"' + re.escape(spelling.rstrip('(')), t))
            if n > 0:
                hits.append(f"    {spelling!r} x{n}: renders {rendered} — {note}")
        if hits:
            bad += 1
            print(f"== {f.parent.name}")
            print('\n'.join(hits))
    print(f"--- files with glyph traps: {bad}/{len(files)}")

if __name__ == '__main__':
    main(sys.argv[1:])
