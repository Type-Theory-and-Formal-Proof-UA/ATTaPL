#!/usr/bin/env python3
"""Reconstruct a book figure's inference rules from the original PDF page.

The printed page gives us text lines (in reading order per column) plus the
short horizontal "fraction bars" that separate a rule's premises from its
conclusion.  This prints, per figure, every rule as PREMISES -> CONCLUSION so
the Typst figure can be rebuilt faithfully instead of invented.
"""
import fitz, glob, sys, collections


def bars(pg):
    """Short horizontal line segments = the bars under rule premises."""
    out = []
    for d in pg.get_drawings():
        for item in d["items"]:
            if item[0] == "l":
                p, q = item[1], item[2]
                if abs(p.y - q.y) < 0.6 and 8 < abs(q.x - p.x) < 260:
                    out.append((round(p.y, 1), round(min(p.x, q.x), 1), round(abs(q.x - p.x), 1)))
    return sorted(set(out))


def lines(pg, y0=0, y1=10_000):
    out = []
    for blk in pg.get_text("dict")["blocks"]:
        for ln in blk.get("lines", []):
            x0, yy0, x1, yy1 = ln["bbox"]
            if yy0 < y0 or yy1 > y1:
                continue
            txt = "".join(sp["text"] for sp in ln["spans"]).strip()
            if txt:
                out.append((round(yy0, 1), round(x0, 1), round(x1, 1), txt))
    return sorted(out)


def main():
    page_idx = int(sys.argv[1])
    y0 = float(sys.argv[2]) if len(sys.argv) > 2 else 0
    y1 = float(sys.argv[3]) if len(sys.argv) > 3 else 10_000
    d = fitz.open(glob.glob("*.pdf")[0])
    pg = d[page_idx]
    ls = lines(pg, y0, y1)
    bs = [b for b in bars(pg) if y0 <= b[0] <= y1]
    print(f"=== page {page_idx + 1}  y {y0}..{y1}   {len(ls)} lines, {len(bs)} bars")
    for y, x0, x1, t in ls:
        tag = ""
        for by, bx, bw in bs:
            if abs(by - (y + 9)) < 6 and bx - 6 <= x0 <= bx + bw + 6:
                tag = "  <<< BAR BELOW (this is a premise)"
        print(f"  y={y:7.1f} x={x0:6.1f}-{x1:6.1f} {t}{tag}")


if __name__ == "__main__":
    main()
