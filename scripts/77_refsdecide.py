"""Decide the ambiguous hyphen sites by MID-LINE occurrence, line by line.

A typeset hyphenation (invented by the typesetter at a line break) NEVER produces a
hyphenated spelling anywhere else — the word is otherwise always written solid.  An
AUTHORED compound like "control-flow" or "Springer-Verlag" is written with its hyphen
wherever it appears mid-line, so it shows up hyphenated somewhere inside a line.

So for a site splitting `left` / `right`:
  * if "left-right" is found MID-LINE anywhere  -> authored hyphen, KEEP it;
  * otherwise                                   -> typeset break, JOIN the halves.

Counting with a whole-document regex is not enough: a line-final hyphen also matches,
and a proper noun that appears exactly once in the whole book (at a break) is never
seen solid, so it would look hyphenated.  Measuring per line avoids both traps.
"""
import fitz, json, pathlib, re

ROOT = pathlib.Path('/Users/ihor/atapl')
doc = fitz.open(next(ROOT.glob('*.pdf')))
U = json.load(open(ROOT / 'src' / 'units.json'))['refs']
LIG = {'\ufb00': 'ff', '\ufb01': 'fi', '\ufb02': 'fl', '\ufb03': 'ffi', '\ufb04': 'ffl'}


def de_lig(s):
    for a, b in LIG.items():
        s = s.replace(a, b)
    return s


def all_lines(pages):
    out = []
    for p in pages:
        for blk in doc[p].get_text('dict')['blocks']:
            for l in blk.get('lines', []):
                t = ''.join(s['text'] for s in l['spans'])
                if t.strip():
                    out.append(de_lig(t))
    return out


LINES = all_lines(range(doc.page_count))
print('lines indexed:', len(LINES))

CAND = ['controlflow', 'semiunification', 'dexptimecomplete', 'communiation',
        'Rocquencourt', 'Troelstra', 'Willcock', 'Informazione', 'Matematicheskii',
        'ObjectOriented', 'Enregistrements', 'Programmation', 'Indiana',
        'SpringerVerlag', 'JavaTM2', 'arithmétique', 'Verlag']

print()
print(f'{"candidate":22s} {"split":28s} {"hyph_midline":>12s} {"solid_midline":>13s}  verdict')
for c in CAND:
    best = None
    for cut in range(2, len(c) - 1):
        left, right = c[:cut], c[cut:]
        h = left + '-' + right
        hm = sum(1 for ln in LINES if h.lower() in ln.lower()
                 and not ln.rstrip().lower().endswith(h.lower()))
        sm = sum(1 for ln in LINES if c.lower() in ln.lower()
                 and not ln.rstrip().lower().endswith(c.lower()))
        if hm or sm:
            best = (left, right, h, hm, sm)
            break
    if best:
        left, right, h, hm, sm = best
        verdict = 'KEEP hyphen' if hm else 'JOIN'
        print(f'{c:22s} {left!r}+{right!r:>12} {hm:12d} {sm:13d}  {verdict}')
    else:
        print(f'{c:22s} {"(no split found)":28s} {"-":>12s} {"-":>13s}  JOIN (default)')
