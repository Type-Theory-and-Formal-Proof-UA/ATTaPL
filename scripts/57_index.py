#!/usr/bin/env python3
"""Structured extractor for the book's Index (two columns, three indent levels).

Measured on the source PDF:
  level 0  x ~ 162.7/166.7 (left)  347.5/351.5 (right)  -> top-level entry
  level 1  x ~ 174.8/178.9 (left)  359.8/363.7 (right)  -> sub-entry
  level 2  x ~ 183.0/187.1 (left)  367.9/371.9 (right)  -> continuation line

The 4pt spread inside each level is a font side-bearing artefact (roman vs
italic); classify by nearest base offset.  A continuation whose predecessor
ends with '-' is de-hyphenated ("mod-" + "ules, 454" -> "modules, 454").
"""
import fitz, json, pathlib, re, sys

ROOT = pathlib.Path('/Users/ihor/atapl')
OUT = ROOT / 'out' / 'index01'


def rows_for_page(pg):
    raw = []
    for blk in pg.get_text("dict")["blocks"]:
        for l in blk.get("lines", []):
            spans = [s for s in l["spans"] if s["text"].strip()]
            if not spans:
                continue
            y = min(s["bbox"][1] for s in spans)
            x = min(s["bbox"][0] for s in spans)
            if y < 100 or y > 620:
                continue
            raw.append((round(x, 1), round(y, 1), "".join(s["text"] for s in spans).strip()))
    out = []
    for side in (0, 1):                        # left column, then right column
        col = [r for r in raw if (r[0] < 340.0) == (side == 0)]
        col.sort(key=lambda r: r[1])
        merged = []
        for x, y, t in col:
            if merged and abs(merged[-1][1] - y) < 5:
                merged[-1] = (merged[-1][0], merged[-1][1], merged[-1][2] + ' ' + t)
            else:
                merged.append((x, y, t))
        out.extend(merged)
    return out


def level_of(x):
    side = 0 if x < 340 else 1
    bases = (162.7, 174.8, 183.0) if side == 0 else (347.5, 359.8, 368.0)
    d = [abs(x - b) for b in bases]
    return d.index(min(d))


def build():
    doc = fitz.open(next(ROOT.glob('*.pdf')))
    U = json.load(open(ROOT / 'src' / 'units.json'))['index']
    entries = []          # (level, text)
    for p in range(U['first'], U['last'] + 1):
        for x, y, t in rows_for_page(doc[p]):
            lv = level_of(x)
            if lv == 2 and entries:
                prev = entries[-1][1]
                if prev.endswith('-'):
                    entries[-1] = (entries[-1][0], prev[:-1] + t)
                else:
                    entries[-1] = (entries[-1][0], prev + ' ' + t)
            else:
                entries.append((lv, t))
    return entries


if __name__ == '__main__':
    E = build()
    print('entries:', len(E))
    lv = {}
    for l, t in E:
        lv[l] = lv.get(l, 0) + 1
    print('by level:', lv)
    OUT.joinpath('structured.txt').write_text(
        "\n".join(f'{l}\t{t}' for l, t in E))
    for l, t in E[:24]:
        print(f'  L{l} {t[:88]}')
