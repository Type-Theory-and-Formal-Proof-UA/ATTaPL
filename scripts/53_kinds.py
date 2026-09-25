#!/usr/bin/env python3
"""Print the book's (number, kind) inventory for a section prefix."""
import fitz, pathlib, re, sys, json

ROOT = pathlib.Path('/Users/ihor/atapl')
doc = fitz.open(next(ROOT.glob("*.pdf")))
UNITS = json.load(open(ROOT / "src" / "units.json"))
KIND_WORDS = ["Theorem", "Lemma", "Corollary", "Definition", "Proposition", "Claim",
              "Notation", "Convention", "Fact", "Axiom", "Example", "Remark", "Exercise",
              "Principle", "Note"]


def pdf_statements(unit):
    a, b = UNITS[unit]["first"], UNITS[unit]["last"]
    found = {}
    for p in range(a, b + 1):
        rows = []
        for blk in doc[p].get_text("dict")["blocks"]:
            for l in blk.get("lines", []):
                spans = [s for s in l["spans"] if s["text"].strip()]
                if not spans:
                    continue
                rows.append((round(min(s["bbox"][1] for s in spans), 1),
                             round(min(s["bbox"][0] for s in spans), 1),
                             "".join(s["text"] for s in spans)))
        for i, (y, x, t) in enumerate(rows):
            if x < 150 and re.fullmatch(r"\d{1,2}\.\d{1,2}\.\d{1,2}", t.strip()):
                num = t.strip()
                line = " ".join(t2 for y2, x2, t2 in rows if abs(y2 - y) < 6 and x2 > 150)
                kind = next((k for k in KIND_WORDS if re.match(rf"\s*{k}\b", line)), "?")
                if num not in found:
                    found[num] = (kind, line[:70])
    return found


if __name__ == "__main__":
    unit, prefix = sys.argv[1], sys.argv[2]
    u = pdf_statements(unit)
    for n in sorted(u, key=lambda s: tuple(int(x) for x in s.split("."))):
        if n.startswith(prefix):
            print(f"{n:9s} {u[n][0]:12s} | {u[n][1]}")
