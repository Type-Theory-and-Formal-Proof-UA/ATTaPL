#!/usr/bin/env python3
"""Derive unit boundaries (physical pages) and print their opening lines for review."""
import fitz, pathlib, json, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
doc = fitz.open(next(ROOT.glob("*.pdf")))
N = len(doc)
print("pages:", N)

TITLES = [
    ("front", "Preface"),
    ("ch01", "Substructural Type Systems"),
    ("ch02", "Dependent Types"),
    ("ch03", "Effect Types and Region-Based Memory Management"),
    ("ch04", "Typed Assembly Language"),
    ("ch05", "Proof-Carrying Code"),
    ("ch06", "Logical Relations and a Case Study in Equivalence Checking"),
    ("ch07", "Typed Operational Reasoning"),
    ("ch08", "Design Considerations for ML-Style Module Systems"),
    ("ch09", "Type Definitions"),
    ("ch10", "The Essence of ML Type Inference"),
    ("appa", "Solutions to Selected Exercises"),
    ("refs", "References"),
    ("index", "Index"),
]

print("\n-- candidate pages containing each title (first 6) --")
cand = {}
for key, title in TITLES:
    hits = []
    for p in range(N):
        t = doc[p].get_text()
        if title in t:
            hits.append(p)
    cand[key] = hits
    print(f"{key:6s} {title[:45]:47s} -> {hits[:6]}")

# chapter opener: title appears on a page whose text starts near it and page has the
# chapter number line right before; print heads of likely openers
print("\n-- opener heads --")
for key, title in TITLES:
    for p in cand[key][:8]:
        t = doc[p].get_text()
        # opener pages: title within first 120 chars
        idx = t.find(title)
        if 0 <= idx < 160:
            head = " / ".join(x.strip() for x in t[:240].splitlines() if x.strip())[:170]
            print(f"{key:6s} p{p:3d} (printed {p-13}) :: {head}")
            break
    else:
        print(f"{key:6s} NO CLEAN OPENER")
