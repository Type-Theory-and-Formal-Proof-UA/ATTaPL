#!/usr/bin/env python3
"""Rewrite the entailment relation where it was mistranscribed as a plain turnstile.

Measured facts (scripts/65_entaildecide.py, 66_entailsites.py, 67_ch10syms.py):
the book prints TWO distinct relations.
  * typing judgment   : ONE bar + one foot  -> Typst `tack`  (U+22A2)
  * constraint entailment: TWO bars + one foot -> U+22A9, which Typst spells `forces`
The extractor decoded the entailment glyph as U+00F0 (ch10/appendix), and the
translation wrote it as a literal U+22A2 — the SAME character as the typing
turnstile written elsewhere as `tack`.  The count correspondence settles which is
which per file:

  appap03 : uk-tack 184  == source ⊢ 184      + 13 literal ⊢ == 13 source entailment
  ch10p02 : uk-tack   0  == source ⊢   0      +  6 literal ⊢ ==  6 source entailment
  ch10p03 : uk-tack  48, 10 literal ⊢  (source 13 entailment - 3 inside the two
            still-unrendered figures 10-7/10-8)
  ch10p04 : uk-tack   0  == source ⊢   0      +  3 literal ⊢ ==  3 source entailment

So in these four files every literal U+22A2 is the entailment relation and must
become `forces`.  The replacement is confined to math spans; a literal ⊢ outside
math is reported instead of rewritten.
"""
import pathlib, re, sys

ROOT = pathlib.Path('/Users/ihor/atapl')
TARGETS = ['ch10p02', 'ch10p03', 'ch10p04', 'appap03']
APPLY = '--apply' in sys.argv


def math_spans(text):
    """Yield (start, end) of each $…$ span, honouring backslash escapes."""
    i, n = 0, len(text)
    while i < n:
        if text[i] == '$':
            j = i + 1
            while j < n and text[j] != '$':
                if text[j] == '\\':
                    j += 1
                j += 1
            yield (i, min(j + 1, n))
            i = j + 1
        else:
            i += 1


total = 0
for part in TARGETS:
    p = ROOT / 'out' / part / 'uk.typ'
    if not p.exists():
        print(f'{part}: no uk.typ')
        continue
    text = p.read_text(encoding='utf-8')
    spans = list(math_spans(text))
    inside = set()
    for a, b in spans:
        for k in range(a, b):
            inside.add(k)
    hits = [i for i, c in enumerate(text) if c == '\u22a2']
    in_math = [i for i in hits if i in inside]
    outside = [i for i in hits if i not in inside]
    print(f'{part}: {len(hits)} literal ⊢, {len(in_math)} inside math, '
          f'{len(outside)} outside')
    for i in outside:
        print(f'    OUTSIDE MATH at {i}: ...{text[max(0, i-60):i+40]!r}')
    if APPLY and in_math:
        chars = list(text)
        for i in in_math:
            chars[i] = '\x00'          # placeholder, expanded below
        new = ''.join(chars).replace('\x00', 'forces')
        (p.parent / (p.name + '.bak-force')).write_text(text, encoding='utf-8')
        p.write_text(new, encoding='utf-8')
        print(f'    -> wrote {len(in_math)} replacements (backup *.bak-force)')
    total += len(in_math)

print(f'\n{"rewrote" if APPLY else "would rewrite"} {total} entailment sites')
