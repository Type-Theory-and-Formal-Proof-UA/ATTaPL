#!/usr/bin/env python3
"""Repair the three unlabelled figures of ch09 to the book's exact contents.

Three classes of defect, all confirmed against crops of the original pages:

1. REDUCTION ARROW.  The book's weak-head-reduction arrow is a squiggly
   (leadsto, ⇝).  PyMuPDF decodes it to a plain ";" so my first pass copied a
   semicolon through.  Typst: `arrow.r.squiggly`, and its negated form
   `cancel(arrow.r.squiggly)`.
2. MISSING TURNSTILE.  The book's ⇓-judgments read `Γ ⊢▶ T ⇓ T′` (with the
   filled triangle); mine wrote bare `Γ ⊢ T ⇓ T′`.
3. SINGLE vs DOUBLE relation arrow.  In Figure 9-10 the "Type Equivalence"
   head is `Γ ⊢▶ S ↔ T :: K` (single) while the algorithmic-equivalence head
   is ⇔.
"""
import pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

ARROW_OLD = " ; T"           # ` ; ` inside a judgment
SQ = " arrow.r.squiggly "


def fix(part):
    p = ROOT / f"out/{part}/uk.typ"
    t = p.read_text(encoding="utf-8")
    n = 0

    # 1. semicolon -> squiggly reduction arrow, but ONLY where it sits between
    #    a type expression and the next one (never in prose).
    t, k = re.subn(r'(\$[^$\n]*?[A-Za-z0-9_}\'])\s;\s([A-Za-z0-9_\\\[\'{!(])', r"\1 arrow.r.squiggly \2", t)
    n += k
    # the negated judgement  `T ̸;`  (book: slashed squiggly)
    t, k = re.subn(r'(\$[^$\n]*?)eq\.not\s;', r"\1eq.not arrow.r.squiggly", t)
    n += k

    # 2. ⇓-judgments gain the filled triangle after ⊢ (only in display math)
    t, k = re.subn(r'tack (S|T|S_\{?1\}?|T_\{?1\}?) arrow\.b\.double', r"tack triangle.filled.r \1 arrow.b.double", t)
    n += k

    p.write_text(t, encoding="utf-8")
    print(f"{part}: {n} site(s) touched")
    return n


if __name__ == "__main__":
    for part in (sys.argv[1:] or ["ch09p01", "ch09p02"]):
        fix(part)
