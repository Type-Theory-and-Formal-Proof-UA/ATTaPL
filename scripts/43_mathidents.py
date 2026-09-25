#!/usr/bin/env python3
"""Find bare multi-letter identifiers inside math spans.

Typst parses `$ {mk : X} $` as the unknown variable `mk`; math braces do NOT
protect identifiers. Every multi-letter name in math must be quoted, so scan each
`$…$` span and report words that are neither quoted nor a known Typst symbol.

Usage: 43_mathidents.py <file.typ> [...]
"""
import pathlib, re, sys

# Typst math vocabulary that legitimately appears unquoted.
KNOWN = set("""
exists forall lambda arrow tack multimap approx equiv compose union sect in not
emptyset subset supset without ZZ Int Bool true false if then else let fun op
angle chevron lr lr. bracket paren bar.v square star diamond bot top prec
gamma Gamma phi rho sigma tau theta alpha beta delta Delta epsilon kappa mu nu
chi psi omega Omega Pi Sigma Lambda Xi Upsilon Psi Theta dot.op circle.filled
partial nabla infinity sum integral hat macron tilde checkmark crossmark prime
prime.double plus.minus minus plus times slash dots times.eq circle.stroked
lt.eq gt.eq eq.not lt gt in.not subset.eq subset.eq.not supset.eq prop models
forces tack.rr tack.r tack.b tack.l tack.t arrow.r arrow.l arrow.t arrow.b
arrow.r.double arrow.r.double.long arrow.l.r arrow.l.r.double arrow.l.r.double.long
arrow.r.bar arrow.r.long.bar arrow.r.triple eq_ approx.eq eq.triple ast
op.limits limits underover sqrt frac binom vec mat cases
""".split())

WORD = re.compile(r"(?<![\"\w.])([A-Za-z][A-Za-z][A-Za-z0-9.]*)(?![\"\w])")
MATH = re.compile(r"\$([^$]*)\$", re.S)


def words_in_math(text):
    hits = {}
    for m in MATH.finditer(text):
        body = m.group(1)
        # drop quoted strings so their contents are not reported
        body = re.sub(r'"[^"]*"', " ", body)
        for w in WORD.finditer(body):
            tok = w.group(1)
            if tok in KNOWN:
                continue
            # a Typst command call or a dotted symbol path is fine
            if tok.split(".")[0] in KNOWN:
                continue
            line = text[:m.start()].count("\n") + 1
            hits.setdefault(tok, []).append(line)
    return hits


bad = 0
for path in sys.argv[1:]:
    t = pathlib.Path(path).read_text(encoding="utf-8")
    hits = words_in_math(t)
    if not hits:
        print(f"{path}: no bare identifiers inside math")
        continue
    print(f"{path}: {len(hits)} distinct bare identifier(s) inside math")
    for tok, lines in sorted(hits.items()):
        print(f"   {tok:22s} lines {lines[:8]}")
        bad += 1
print(f"\n{bad} to review")
