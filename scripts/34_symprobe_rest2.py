#!/usr/bin/env python3
"""Second ch07 probe: the notations that were still unverified — the relation
arrow ↔, the frame-stack typing arrow ⊸, literal braces in math, the
definition/contextual-equality subscripts, and integer/boolean type names.
"""
import subprocess, pathlib, re, sys, unicodedata

ROOT = pathlib.Path(__file__).resolve().parent.parent
build = ROOT / "build"

CAND = [
    ("arrow.l.r", r"arrow.l.r"),
    ("arrow.l.r.long", r"arrow.l.r.long"),
    ("multimap", r"multimap"),
    ("arrow.r.long.bar", r"arrow.r.long.bar"),
    ("arrow.r.bar", r"arrow.r.bar"),
    ("bar.r", r"bar.r"),
    ("arrow.r.dashed", r"arrow.r.dashed"),
    ("braces", r"{exists X, T}"),
    ("braces2", r"lr({exists X, T})"),
    ("braces3", r"\\{exists X, T\\}"),
    ("eq-sub", r"eq_(\"ctx\")"),
    ("eq-def", r"eq_(\"def\")"),
    ("t-down", r"t arrow.b"),
    ("t-up", r"t arrow.t"),
    ("Int", r"\"Int\""),
    ("Bool", r"\"Bool\""),
    ("Nat", r"\"Nat\""),
    ("Z", r"ZZ"),
    ("lub", r"lub"),
    ("sem", r"⟨S, t⟩"),
    ("angles", r"angle.l S, t angle.r"),
    ("subst", r"[X, S]T"),
    ("ftv", r"ftv(Gamma)"),
    ("phi-sub", r"T_phi"),
    ("approx.eq3", r"T_1 approx.eq T_2"),
    ("circ-frame", r"S_1 compose S_2"),
    ("nil-id", r"\"Id\""),
]


def build_source(cands):
    lines = ["#set page(width: 300mm, height: 900mm, margin: 8mm)",
             '#set text(font: "STIX Two Text", size: 9pt, lang: "uk")',
             "#set par(leading: 0.6em)"]
    for i, (label, mk) in enumerate(cands):
        lines.append(f"[{i} {label}: ]$ {mk} $")
    return "\n".join(lines) + "\n"


dropped, cands = [], list(CAND)
while True:
    probe = build / "_symprobe_rest2.typ"
    probe.write_text(build_source(cands))
    r = subprocess.run(["typst", "compile", "--root", str(ROOT), str(probe),
                        str(build / "_symprobe_rest2.pdf")],
                       capture_output=True, text=True)
    if r.returncode == 0:
        break
    m = re.search(r"_symprobe_rest2\.typ:(\d+):", r.stderr)
    if not m:
        print("UNPARSED:\n", r.stderr[:600]); sys.exit(1)
    idx = int(m.group(1)) - 4
    if not (0 <= idx < len(cands)):
        print("cannot map", m.group(1), r.stderr[:300]); sys.exit(1)
    dropped.append(cands[idx][0] + "  <- " + r.stderr.strip().splitlines()[0][:70])
    cands.pop(idx)

print(f"compiled with {len(cands)}; {len(dropped)} rejected")
for d in dropped:
    print("  dropped:", d)
print()
txt = subprocess.run(["pdftotext", "-layout", str(build / "_symprobe_rest2.pdf"), "-"],
                     capture_output=True, text=True).stdout
for line in txt.splitlines():
    if not line.strip():
        continue
    keep = [c for c in line if ord(c) > 0x2000]
    print(f"{line[:30]!r:34s} -> " + " ".join(f"{c}=U+{ord(c):04X}" for c in keep))
