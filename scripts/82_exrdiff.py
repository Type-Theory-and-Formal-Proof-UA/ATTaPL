#!/usr/bin/env python3
"""Fix the exercise-difficulty marker: the book prints FILLED STARS, not guillemets.

The difficulty scale is defined in the Preface (book p. xii):

    ★    quick check        30 seconds to 5 minutes
    ★★   easy               <=1 hour
    ★★★  moderate           <=3 hours
    ★★★★ challenging        > 3 hours
    ↛    (in the index) exercise without solution

The extractor decoded the star as `«` (font F0, the symbol font) and the slashed
arrow as `†` — confirmed by rendering crops of the Preface scale, an index row and
a chapter exercise line (raw/crops/preface_scale4.png, index_star_rows.png,
exr_marker_p20.png): every one shows a solid five-pointed star.

Two very different things therefore look identical in the sources:
  * `diff: "«"` inside `#exr(...)` — the DIFFICULTY MARKER, a star: must be fixed;
  * `«щось»` in Ukrainian prose — legitimate quotation marks: must NOT be touched.
So the sweep is scoped to the `diff:` arguments, never to a bare `«` in text.

`star.filled` renders ★ (U+2605) and `star` alone renders ⋆ (U+22C6, hollow) —
probed in build/_ppref.typ. The literal ★ is used here; it is what several
translated chapters already print for other starred notation.
"""
import pathlib, re, subprocess, sys

ROOT = pathlib.Path('/Users/ihor/atapl')
APPLY = '--apply' in sys.argv

# a `diff:` argument is a quoted string of one-or-more marker glyphs (possibly
# followed by an ellipsis in one chapter); map each `«` to a star and keep length.
DIFF = re.compile(r'diff:\s*"([«]*(?:\s*\.\.\.)?)"')

total, files = 0, 0
for f in sorted(ROOT.glob('out/*/uk.typ')):
    t = f.read_text(encoding='utf-8')
    def repl(m):
        global total
        inner = m.group(1)
        new = inner.replace('«', '★')
        if new != inner:
            total += 1
        return f'diff: "{new}"'
    nt = DIFF.sub(repl, t)
    if nt != t:
        files += 1
        if APPLY:
            f.write_text(nt, encoding='utf-8')

print(f'diff: arguments carrying the marker glyph: {total} in {files} files')
if not APPLY:
    print('(dry run — pass --apply)')
    sys.exit(0)

# also fix the index's no-solution dagger, if any survived
idx = ROOT / 'out' / 'index01' / 'uk.typ'
it = idx.read_text(encoding='utf-8')
if '†' in it:
    print('index: replacing † -> ↛ (no-solution marker)')
    idx.write_text(it.replace('†', '↛'), encoding='utf-8')

# report any remaining marker glyph NOT inside a diff argument (should be prose quotes)
for f in sorted(ROOT.glob('out/*/uk.typ')):
    t = f.read_text(encoding='utf-8')
    leftover = DIFF.findall(t)
    if leftover:
        print(f'  STILL MARKED {f.parent.name}: {leftover[:3]}')
print('done')
