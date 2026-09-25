#!/usr/bin/env python3
"""Authoritative statement check: the book's margin numbers vs the translation's labels.

The book prints every statement's number in the LEFT margin (x≈110-148) with the
statement text to its right on the same baseline, e.g.
    6.2.1   LEMMA: Suppose ...
That is the only reliable inventory: the running text also says "by Lemma 6.2.1",
which inflates any text-side count.

For each chapter we build the multiset {(number, kind)} from the PDF and the
multiset from the translated PDF's rendered labels ("Lemma 6.2.1 ."), then diff
them per kind.  A kind whose counts differ names a dropped or invented statement.
"""
import fitz, pathlib, re, sys, json, collections

ROOT = pathlib.Path(__file__).resolve().parent.parent
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
                # the same visual line, right of the margin
                line = " ".join(t2 for y2, x2, t2 in rows if abs(y2 - y) < 6 and x2 > 150)
                kind = next((k for k in KIND_WORDS if re.match(rf"\s*{k}\b", line)), "?")
                if num not in found:
                    found[num] = (kind, line[:60])
    return found


def translated_statements(pdf_path):
    """Read the rendered labels + kinds out of the translated PDF."""
    import subprocess
    txt = subprocess.run(["pdftotext", "-layout", str(pdf_path), "-"],
                         capture_output=True, text=True).stdout.replace("\f", "\n")
    out = {}
    pat = r"(?<![\w.])(" + "|".join(KIND_WORDS) + r")\s+(\d{1,2}\.\d{1,2}\.\d{1,2})(?![\d.])"
    for m in re.finditer(pat, txt):
        out[m.group(2)] = m.group(1)
    return out


if __name__ == "__main__":
    manifest = json.load(open(ROOT / "manifest.json"))
    args = sys.argv[1:] or sorted(manifest)
    grand = 0
    for part in args:
        info = manifest[part]
        unit = info["chapter"]
        src = pdf_statements(unit)
        uk_pdf = pathlib.Path(f"/tmp/num_{part}.pdf")
        import subprocess
        subprocess.run(["typst", "compile", "--root", str(ROOT), str(ROOT / info["output"]), str(uk_pdf)],
                       capture_output=True, text=True)
        if not uk_pdf.exists():
            print(f"{part:9s} SKIP (does not compile)")
            continue
        uk = translated_statements(uk_pdf)
        # split the chapter's statements by the section ranges the part owns
        secs = [s.split()[0] for s in info["sections"]]
        def snum(s):
            return tuple(int(x) for x in s.split("."))
        lo, hi = snum(secs[0]), snum(secs[-1])
        mine = {n: k for n, k in src.items() if lo <= snum(n.rsplit(".", 1)[0]) <= hi}
        missing = sorted(set(mine) - set(uk))
        extra = sorted(set(uk) - set(mine))
        kindbad = sorted(n for n in set(mine) & set(uk) if mine[n][0] != uk[n] and mine[n][0] != "?")
        print("=" * 74)
        print(f"{part:9s} book={len(mine):3d} translated={len(uk):3d}  "
              f"missing={len(missing)} extra={len(extra)} kind-mismatch={len(kindbad)}")
        if missing:
            print("   MISSING:", ", ".join(f"{n}({mine[n][0]})" for n in missing))
        if extra:
            print("   EXTRA  :", ", ".join(f"{n}({uk[n]})" for n in extra))
        if kindbad:
            print("   KIND   :", ", ".join(f"{n}: book={mine[n][0]} uk={uk[n]}" for n in kindbad))
        grand += len(missing) + len(extra)
    print(f"\nTOTAL statement-level differences across the wave: {grand}")
