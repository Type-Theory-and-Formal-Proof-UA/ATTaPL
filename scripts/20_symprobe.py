#!/usr/bin/env python3
"""Render candidate symbols, then read the PDF back to see which glyph each prints.

The point: a symbol NAME that compiles can still print the wrong relation.
We print  <index> <symbol>  and check the glyph after the index.
"""
import subprocess, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
build = ROOT / "build"
build.mkdir(exist_ok=True)

CAND = [
    # (label, typst markup for math mode)
    ("tack", r"tack"), ("tack.r", r"tack.r"), ("tack.b", r"tack.b"),
    ("tack.r.long", r"tack.r.long"), ("tack.l.long", r"tack.l.long"),
    ("tack.t", r"tack.t"), ("tack.r.short", r"tack.r.short"),
    ("models", r"models"), ("forces", r"forces"),
    ("arrow.r", r"arrow.r"), ("arrow.r.double", r"arrow.r.double"),
    ("arrow.r.double.long", r"arrow.r.double.long"),
    ("arrow.r.long.double", r"arrow.r.long.double"),
    ("arrow.l.r.double", r"arrow.l.r.double"),
    ("arrow.l.r.double.long", r"arrow.l.r.double.long"),
    ("arrow.r.triple", r"arrow.r.triple"),
    ("arrow.r.bar", r"arrow.r.bar"), ("arrow.r.hook", r"arrow.r.hook"),
    ("arrow.r.squiggly", r"arrow.r.squiggly"),
    ("arrow.r.tail", r"arrow.r.tail"), ("arrow.r.loop", r"arrow.r.loop"),
    ("arrow.r.curve", r"arrow.r.curve"),
    ("arrow.t", r"arrow.t"), ("arrow.b", r"arrow.b"),
    ("arrow.twohead", r"arrow.twohead"),
    ("prec.eq", r"prec.eq"), ("prec.curly.eq", r"prec.curly.eq"),
    ("prec.napprox", r"prec.napprox"), ("prec", r"prec"),
    ("subset.eq", r"subset.eq"), ("subset.eq.sq", r"subset.eq.sq"),
    ("subset.eq.not", r"subset.eq.not"), ("supset.eq", r"supset.eq"),
    ("in", r"in"), ("emptyset", r"emptyset"),
    ("forall", r"forall"), ("exists", r"exists"),
    ("and", r"and"), ("or", r"or"), ("not", r"not"),
    ("eq.not", r"eq.not"), ("lt.eq", r"lt.eq"), ("lt.eq.slant", r"lt.eq.slant"),
    ("gt.eq", r"gt.eq"), ("bot", r"bot"), ("top", r"top"),
    ("ell", r"ell"), ("partial", r"partial"), ("nabla", r"nabla"),
    ("colon.eq", r"colon.eq"), ("equiv", r"equiv"), ("approx", r"approx"),
    ("tilde", r"tilde"), ("tilde.eq", r"tilde.eq"),
    ("circle.stroked.tiny", r"circle.stroked.tiny"), ("circle.small", r"circle.small"),
    ("compose", r"compose"), ("circle.filled", r"circle.filled"),
    ("bullet", r"bullet"), ("dot.op", r"dot.op"),
    ("diamond", r"diamond"), ("diamond.stroked", r"diamond.stroked"),
    ("star", r"star"), ("star.op", r"star.op"),
    ("parallel", r"parallel"), ("perp", r"perp"),
      
     
    ("plus.minus", r"plus.minus"), ("minus", r"minus"), ("plus", r"plus"),
    ("without", r"without"), ("union", r"union"), 
    ("sect?", "§"),
    ("triangle.r", r"triangle.r"), ("triangle.stroked", r"triangle.stroked"),
    ("square", r"square"), ("square.stroked", r"square.stroked"),
    ("chevron.l", r"chevron.l"), ("chevron.r", r"chevron.r"),
    ("angle", r"angle"), ("bracket.l", r"bracket.l"), ("bracket.r", r"bracket.r"),
    ("paren.l", r"paren.l"), ("paren.r", r"paren.r"),
    ("bar.v", r"bar.v"), ("bar.v.bar", r"bar.v.bar"),
    ("infinity", r"infinity"), ("checkmark", r"checkmark"), ("crossmark", r"crossmark"),
    ("prime", r"prime"), ("prime.double", r"prime.double"),
    ("Gamma", r"Gamma"), ("Delta", r"Delta"), ("Lambda", r"Lambda"),
    ("Sigma", r"Sigma"), ("Pi", r"Pi"), ("Psi", r"Psi"), ("Omega", r"Omega"),
    ("epsilon", r"epsilon"), ("epsilon.alt", r"epsilon.alt"),
    ("phi", r"phi"), ("phi.alt", r"phi.alt"), ("rho", r"rho"), ("sigma", r"sigma"),
    ("tau", r"tau"), ("kappa", r"kappa"), ("gamma", r"gamma"), ("beta", r"beta"),
    ("alpha", r"alpha"), ("mu", r"mu"), ("nu", r"nu"), ("theta", r"theta"),
    ("chi", r"chi"), ("psi", r"psi"), ("omega", r"omega"), ("lambda", r"lambda"),
    ("sum", r"sum"), ("integral", r"integral"),
    # literal Unicode in math mode
    ("U+22A2", "⊢"), ("U+22A4", "⊤"), ("U+22A5", "⊥"), ("U+2AAF", "⪯"),
    ("U+22C4", "⋄"), ("U+2297", "⊗"), ("U+22C6", "⋆"), ("U+2225", "∥"),
    ("U+03F5", "ϵ"), ("U+27E8", "⟨"), ("U+27E9", "⟩"), ("U+25B7", "▷"),
    ("U+25B6", "▶"), ("U+21D2", "⇒"), ("U+21D4", "⇔"), ("U+2192", "→"),
    ("U+2192txt", "→"),
]

lines = ["#set page(width: 260mm, height: 400mm, margin: 10mm)",
         '#set text(font: "STIX Two Text", size: 10pt, lang: "uk")',
         "#set par(leading: 0.8em)"]
for i, (label, mk) in enumerate(CAND):
    if label.endswith("txt"):
        lines.append(f"[{i} {label}: {mk}]")
    else:
        lines.append(f"[{i} {label}: ]$ {mk} $")
probe = build / "_symprobe.typ"
probe.write_text("\n".join(lines) + "\n")
r = subprocess.run(["typst", "compile", "--root", str(ROOT), str(probe), str(build / "_symprobe.pdf")],
                   capture_output=True, text=True)
print("compile rc", r.returncode, r.stderr[:1500])
if r.returncode:
    sys.exit(1)
