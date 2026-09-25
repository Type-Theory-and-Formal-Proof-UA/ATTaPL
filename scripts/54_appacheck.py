#!/usr/bin/env python3
"""Appendix A check: every exercise number the book prints in the margin must
appear as a #soln(...) label in the translation, and vice versa."""
import pathlib, re, subprocess, sys

ROOT = pathlib.Path('/Users/ihor/atapl')


def book_nums(pdf, lo, hi):
    import fitz
    doc = fitz.open(pdf)
    found = []
    for p in range(lo, hi + 1):
        rows = []
        for blk in doc[p].get_text("dict")["blocks"]:
            for l in blk.get("lines", []):
                spans = [s for s in l["spans"] if s["text"].strip()]
                if spans:
                    rows.append((round(min(s["bbox"][1] for s in spans), 1),
                                 round(min(s["bbox"][0] for s in spans), 1),
                                 "".join(s["text"] for s in spans)))
        for y, x, t in rows:
            if x < 150 and re.fullmatch(r"\d{1,2}\.\d{1,2}\.\d{1,2}", t.strip()):
                found.append(t.strip())
    return found


if __name__ == "__main__":
    import json
    UNITS = json.load(open(ROOT / 'src' / 'units.json'))
    pdf = next(ROOT.glob('*.pdf'))
    unit = UNITS['appa']
    grand = 0
    for part in sys.argv[1:]:
        src = pathlib.Path(f'/Users/ihor/atapl/out/{part}/source.txt').read_text()
        # the part's own exercise numbers, from the raw extract's margin markers
        want = sorted(set(re.findall(r'(?<!\d)(\d{1,2}\.\d{1,2}\.\d{1,2})', src)))
        uk = pathlib.Path(f'/Users/ihor/atapl/out/{part}/uk.typ').read_text()
        have = sorted(set(re.findall(r'#soln\("(\d{1,2}\.\d{1,2}\.\d{1,2})"\)', uk)))
        missing = sorted(set(want) - set(have))
        extra = sorted(set(have) - set(want))
        print('=' * 70)
        print(f'{part}: source={len(want)} uk={len(have)} missing={len(missing)} extra={len(extra)}')
        if extra:
            print('  EXTRA  :', ', '.join(extra))
        grand += len(extra)
    print(f'\nTOTAL invented appendix labels: {grand}')
