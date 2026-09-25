#!/usr/bin/env python3
"""Symbol census: every notation glyph in a part's source must survive into the
rendered PDF, and glyphs the source does NOT contain must not appear.

Motivated by three real defects: a hollow triangle for a filled one, an invented
`~` for ⇔, and a fabricated `_a` subscript on the turnstile.  Counting glyphs in
the RENDERED page is the only check that catches a wrong-but-compiling symbol.
"""
import pathlib, re, subprocess, sys, json, collections, unicodedata

ROOT = pathlib.Path(__file__).resolve().parent.parent
# source glyph -> (meaning, typst spellings that legitimately render it)
GLYPHS = {
    "\u25b6": ("filled right triangle", ["triangle.filled.r", "triangle.r.filled"]),
    "\u25b7": ("hollow right triangle", ["triangle.r", "triangle.stroked.r"]),
    "\u21d4": ("left-right double arrow", ["arrow.l.r.double", '" is "']),
    "\u2194": ("left-right arrow", ["arrow.l.r", '↔']),
    "\u2261": ("identical-to", ["equiv"]),
    "\u225f": ("questioned equal", ['\u225f']),
    "\u2205": ("empty set", ["emptyset"]),
    "\u22a2": ("turnstile", ["tack"]),
    "\u21d3": ("down double arrow", ["arrow.b.double"]),
    "\u03f5": ("lunate epsilon", ["epsilon.alt", "\u03f5"]),
    "\u2aaf": ("precedes-above-equal", ["prec.eq.slant", "preceq.slant"]),
    "\u22c4": ("diamond", ["diamond"]),
    "\u2202": ("partial", ["partial"]),
    "\u2297": ("circled times", ["otimes"]),
    "\u2113": ("script l", ["ell"]),
    "\u2191": ("upwards arrow", ["arrow.t"]),
    "\u21d4": ("left-right double arrow", ["arrow.l.r.double"]),
    "\u225f": ("questioned equal", ["\u225f"]),
}

# Typst's spelling is right in shape but a different codepoint than the PDF uses,
# so the rendered page can never contain the source codepoint.  Keyed by
# (source glyph, rendered codepoint that is an acceptable stand-in).
SHAPE_EQUIV = {
    # epsilon.alt draws the lunate epsilon the book uses, as U+1D716 not U+03F5
    "\u03f5": "\U0001D716",
}

# The extractor decoded these source glyphs to the wrong codepoint, so the source
# text cannot be used as evidence they are absent.  (part, glyph) -> why.
SOURCE_MANGLED = {
    # the book's ⇔ came out of PyMuPDF as the letter "a" on page 244
    ("ch06p01", "\u21d4"): "source decoded as 'a'",
    ("ch06p01", "\u225f"): "rare glyph dropped by the extractor",
    # ch09's algorithmic-equivalence relation is the same ⇔, and its font F0
    # span arrives as a bare "a" too (confirmed against the page image).
    ("ch09p01", "\u21d4"): "source decoded as 'a'",
    ("ch09p02", "\u21d4"): "source decoded as 'a'",
}


def readback(pdf):
    return subprocess.run(["pdftotext", "-layout", str(pdf), "-"],
                          capture_output=True, text=True).stdout


def main():
    man = json.load(open(ROOT / "manifest.json"))
    only = sys.argv[1:] or sorted(man)
    problems = 0
    for part in only:
        notes = []
        src = (ROOT / f"out/{part}/source.txt").read_text(encoding="utf-8")
        uk = (ROOT / f"out/{part}/uk.typ").read_text(encoding="utf-8")
        pdf = ROOT / "build" / f"_{part}.pdf"
        r = subprocess.run(["typst", "compile", "--root", str(ROOT),
                            str(ROOT / f"out/{part}/uk.typ"), str(pdf)],
                           capture_output=True, text=True)
        if r.returncode != 0:
            print(f"{part:9s} COMPILE FAILED"); problems += 1; continue
        got = collections.Counter(readback(pdf))
        rows = []
        for g, (name, spellings) in GLYPHS.items():
            n_src = src.count(g)
            # accept a glyph if the target spells it in typst, else it must be literal
            n_uk = sum(uk.count(s) for s in spellings) + (uk.count(g) if g not in "↔" else 0)
            n_out = got.get(g, 0)
            stand_in = SHAPE_EQUIV.get(g)
            if stand_in:
                n_out += got.get(stand_in, 0)
            mangled = SOURCE_MANGLED.get((part, g))
            if n_src and n_out == 0:
                rows.append(f"LOST {name} (src {n_src}, uk {n_uk}, rendered 0)")
            if n_src == 0 and n_out and not mangled:
                rows.append(f"INVENTED {name} rendered {n_out}x, absent from source")
            if n_src == 0 and n_out and mangled:
                notes.append(f"note: {name} rendered {n_out}x ({mangled}) - accepted")
        # wrong-triangle specifically: source has filled but we render hollow or vice versa
        if src.count("\u25b6") and not got.get("\u25b6"):
            rows.append("WRONG triangle: source is filled, render is not")
        if src.count("\u25b7") and not got.get("\u25b7"):
            rows.append("WRONG triangle: source is hollow, render is not")
        status = "ok" if not rows else "PROBLEMS"
        print(f"{part:9s} {status}" + ("" if not notes else f"  ({len(notes)} accepted note(s))"))
        for x in rows:
            print("            ", x); problems += 1
        for x in notes:
            print("            ", x)
    print(f"\n{problems} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
