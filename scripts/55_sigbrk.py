#!/usr/bin/env python3
"""Module-signature delimiters in chapter 9 / appendix A.

The source PDF's subsetted math fonts (Fg, Fi, Fj, Fh) contain ONLY the glyphs
{L, M} — see `56_symsites.py`, which proves the whole character repertoire of
those fonts is those two glyphs, plus {J, K} in Fh.  J/K are chapter 10's
semantic brackets (⟦ ⟧, independently confirmed by pixel crop), so L/M must be
a delimiter pair too — and it is: the glyphs measure 165px tall with a 21%-of-
height bow and no serif foot, i.e. a stretchy PARENTHESIS, while a genuine
capital L in the same chapter (text font F1) is 108px with a wide 65px foot.
The font's ToUnicode table simply reports the glyph ids 0x4C/0x4D as the
letters 'L'/'M'.

So every bare `L` token inside a math span is an opening delimiter and its
matching `M` closes it.  In chapter 9 ALL 'L' glyphs come from those symbol
fonts (census: L/Fh=119, L/Fj=55, none from a text font), so converting bare
`L` is safe there; genuine module `M` (M/F1, M/Ga) is preserved because a
converted `M` must close a previously opened `L`.

Unbalanced input (a group split across two math spans) fails to compile, which
is the intended check.
"""
import pathlib
import re
import sys

# a bare token: not preceded/followed by identifier characters, not quoted
BARE = re.compile(r'(?<![A-Za-z0-9_"\\])([LM])(?![A-Za-z0-9_])')


def convert_span(seg):
    """Rewrite bare L/M delimiter pairs inside one math span."""
    out, stack, n = [], [], 0
    pos = 0
    for m in BARE.finditer(seg):
        out.append(seg[pos:m.start()])
        ch = m.group(1)
        if ch == 'L':
            stack.append(True)
            out.append('(')
        elif stack:
            stack.pop()
            out.append(')')
            n += 1
        else:
            out.append('M')          # genuine module M — keep
        pos = m.end()
    out.append(seg[pos:])
    return ''.join(out), n, len(stack)


def convert_file(path, dry=False):
    p = pathlib.Path(path)
    t = p.read_text()
    res, i, pairs = [], 0, 0
    while True:
        a = t.find('$', i)
        if a < 0:
            res.append(t[i:])
            break
        b = t.find('$', a + 1)
        if b < 0:
            res.append(t[i:])
            break
        res.append(t[i:a + 1])
        seg, n, unclosed = convert_span(t[a + 1:b])
        if unclosed:
            print(f'   !! unclosed group in {path}: {t[a + 1:b][:60]!r}')
        pairs += n
        res.append(seg)
        res.append('$')
        i = b + 1
    new = ''.join(res)
    if not dry:
        p.write_text(new)
    return pairs


if __name__ == '__main__':
    dry = '--dry' in sys.argv
    for arg in [a for a in sys.argv[1:] if not a.startswith('--')]:
        n = convert_file(arg, dry)
        print(f'{arg}: {n} delimiter pairs {"(dry run)" if dry else "converted"}')
