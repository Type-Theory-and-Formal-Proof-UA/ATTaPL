import fitz, json, pathlib, collections
ROOT = pathlib.Path('/Users/ihor/atapl')
doc = fitz.open(next(ROOT.glob('*.pdf')))
UNITS = json.load(open(ROOT / 'src' / 'units.json'))

# fonts whose ENTIRE repertoire is drawn from the symbol glyph pool used for
# stretchy delimiters: J/K (⟦⟧ in ch10) and L/M (parens in ch09).
SYMSET = set('JKLM')
rep = collections.defaultdict(set)
for name, u in UNITS.items():
    if 'first' not in u:
        continue
    for p in range(u['first'], u['last'] + 1):
        for blk in doc[p].get_text("dict")["blocks"]:
            for l in blk.get("lines", []):
                for s in l["spans"]:
                    rep[s["font"]].update(s["text"])

symbol_fonts = {f for f, cs in rep.items()
                if cs and set(cs) - {' '} and (set(cs) - {' '}) <= SYMSET}
print('pure symbol fonts:', sorted(symbol_fonts))
for f in sorted(symbol_fonts):
    print(f'   {f}: {sorted(rep[f])}')

print()
print('=== per-unit count of symbol-font glyphs (delimiter sites):')
for name in sorted(UNITS):
    u = UNITS[name]
    if 'first' not in u:
        continue
    cnt = collections.Counter()
    for p in range(u['first'], u['last'] + 1):
        for blk in doc[p].get_text("dict")["blocks"]:
            for l in blk.get("lines", []):
                for s in l["spans"]:
                    if s["font"] in symbol_fonts:
                        for ch in s["text"]:
                            if ch.strip():
                                cnt[ch] += 1
    if cnt:
        print(f'  {name:8s} {dict(cnt)}')
