#!/usr/bin/env python3
"""Remove INVENTED rule labels from figures whose inference rules the book
prints unlabelled.

Figures 9-5, 9-7 (ch09p01) and 9-10 (ch09p02) carry no rule names in the
original: the rules appear as bare premises/conclusion pairs.  Shipping
names like "SHR-Beta" or "STE-Var" therefore invents content that is not in
the book.  This blanks the 2nd positional argument of every #rule(...) inside
the named #figure blocks, leaving the labels that are genuinely printed
(Figures 9-1..9-4, 9-6, 9-8, 9-9) untouched.
"""
import pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

# (part, figure caption prefix) pairs whose rules are unlabelled in the book
TARGETS = [
    ("ch09p01", "Рисунок 9-5"),
    ("ch09p01", "Рисунок 9-7"),
    ("ch09p02", "Рисунок 9-10"),
]


def blank_labels(block):
    """Inside a figure block, replace #rule(premises, "Name", concl) -> ""."""
    def fix(m):
        pre, name, concl = m.group(1), m.group(2), m.group(3)
        return f'#rule({pre}, "", {concl})'
    return re.sub(r'#rule\(((?:[^()]|\([^()]*\))*?),\s*"([^"]+)",\s*((?:[^()]|\([^()]*\))*?)\)',
                  fix, block)


def main():
    total = 0
    for part, cap in TARGETS:
        p = ROOT / f"out/{part}/uk.typ"
        t = p.read_text(encoding="utf-8")
        i = t.find(f"#figure([{cap}")
        if i < 0:
            print(f"!! {part}: figure {cap!r} not found"); continue
        j = t.find("\n]))", i)
        if j < 0:
            print(f"!! {part}: closing of {cap!r} not found"); continue
        block = t[i:j]
        new = blank_labels(block)
        n = len(re.findall(r'#rule\([^\n]*?,\s*""', new)) - len(re.findall(r'#rule\([^\n]*?,\s*""', block))
        t = t[:i] + new + t[j:]
        p.write_text(t, encoding="utf-8")
        print(f"{part}: {cap} -> {n} label(s) removed")
        total += n
    print(f"total {total}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
