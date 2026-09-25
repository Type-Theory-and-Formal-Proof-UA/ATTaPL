#!/usr/bin/env python3
"""Ch07+ symbol probe: render candidates, drop the ones Typst rejects, then read
the rendered glyphs back so a name that compiles but prints the wrong symbol is
still caught.

Run: 33_symprobe_rest.py        -> build/_symprobe_rest.pdf + printed glyph table
"""
import subprocess, pathlib, re, sys, unicodedata

ROOT = pathlib.Path(__file__).resolve().parent.parent
build = ROOT / "build"
build.mkdir(exist_ok=True)

CAND = [
    ("exists", r"exists"),
    ("lr-brace", r"lr({exists X, T})"),
    ("pack", r"{*S, t} \"as\" {exists X, T}"),
    ("approx.eq", r"approx.eq"),
    ("approx", r"approx"),
    ("simeq", r"simeq"),
    ("tack.rr", r"tack.rr"),
    ("tack.r.double", r"tack.r.double"),
    ("tack.r", r"tack.r"),
    ("arrow.b", r"arrow.b"),
    ("arrow.t", r"arrow.t"),
    ("sect", r"sect"),
    ("inter", r"inter"),
    ("union", r"union"),
    ("subset.eq", r"subset.eq"),
    ("compose", r"compose"),
    ("circle.filled.small", r"circle.filled.small"),
    ("lt.eq", r"lt.eq"),
    ("gt.eq", r"gt.eq"),
    ("eq.not", r"eq.not"),
    ("in.not", r"in.not"),
    ("subset", r"subset"),
    ("supset", r"supset"),
    ("without", r"without"),
    ("arrow.r.double.long", r"arrow.r.double.long"),
    ("arrow.l.r.double", r"arrow.l.r.double"),
    ("square", r"square"),
    ("star.op", r"star.op"),
    ("diamond", r"diamond"),
    ("bot", r"bot"),
    ("top", r"top"),
    ("Z", r"ZZ"),
    ("forall", r"forall"),
    ("lambda", r"lambda"),
    ("lr", r"lr(]a])"),
    ("hat", r"hat(x)"),
    ("macron", r"macron(x)"),
    ("sub.def", r"a_(def)"),
]


def build_source(cands):
    lines = ["#set page(width: 300mm, height: 900mm, margin: 8mm)",
             '#set text(font: "STIX Two Text", size: 9pt, lang: "uk")',
             "#set par(leading: 0.6em)"]
    for i, (label, mk) in enumerate(cands):
        lines.append(f"[{i} {label}: ]$ {mk} $")
    return "\n".join(lines) + "\n"


dropped = []
cands = list(CAND)
while True:
    probe = build / "_symprobe_rest.typ"
    probe.write_text(build_source(cands))
    r = subprocess.run(["typst", "compile", "--root", str(ROOT), str(probe),
                        str(build / "_symprobe_rest.pdf")],
                       capture_output=True, text=True)
    if r.returncode == 0:
        break
    m = re.search(r"_symprobe_rest\.typ:(\d+):", r.stderr)
    if not m:
        print("UNPARSED ERROR:\n", r.stderr[:800]); sys.exit(1)
    idx = int(m.group(1)) - 4
    if not (0 <= idx < len(cands)):
        print("cannot map error line", m.group(1), r.stderr[:400]); sys.exit(1)
    dropped.append(cands[idx][0] + "  <- " + r.stderr.strip().splitlines()[0][:70])
    cands.pop(idx)

print(f"compiled with {len(cands)} candidates; {len(dropped)} rejected")
for d in dropped:
    print("  dropped:", d)
print()
txt = subprocess.run(["pdftotext", "-layout", str(build / "_symprobe_rest.pdf"), "-"],
                     capture_output=True, text=True).stdout
for line in txt.splitlines():
    if not line.strip():
        continue
    keep = [c for c in line if ord(c) > 0x2000]
    glyphs = " ".join(f"{c}=U+{ord(c):04X}" for c in keep)
    print(f"{line[:26]!r:30s} -> {glyphs}")
