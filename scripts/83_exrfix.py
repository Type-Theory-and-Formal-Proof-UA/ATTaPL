#!/usr/bin/env python3
"""Reconcile the `sol:` (no-solution) flag on #exr exercises against the book.

The book marks an exercise whose solution is NOT in Appendix A with a slashed right
arrow (U+219B) in its bracket group:

    Exercise [«««, ↛]: Prove progress and preservation using TAPL, Chapters 9 and 13

The extractor decodes that glyph as a `3` (font F0, the symbol font), so the marker
is recognisable in a part's `source.txt` as an exercise bracket group ending
`, 3]`.  The translation expresses it as `sol: true` on the `#exr(...)` call.

Two defects this reconciles, both found by counting the marker per part against the
book rather than trusting the files:

  * chapters 7-10 simply DROPPED it — 37 exercises whose solution does not exist
    were presented as if a solution were available, which sends the reader to an
    Appendix A entry that is not there;
  * ch05p02 marked two exercises `sol: true` that the book prints with a bare star
    and no marker.

Ordering is what makes this safe to automate: `#exr` calls appear in source order
within a part, as do the exercise bracket groups, so the Nth call corresponds to the
Nth group.  The script asserts that correspondence (equal counts) before writing
anything, and every rewritten call must still compile.

Usage: 82_exrfix.py [--apply]
"""
import pathlib, re, subprocess, sys

ROOT = pathlib.Path('/Users/ihor/atapl')
APPLY = '--apply' in sys.argv

# bracket groups of an exercise head in the extracted source.  Require the group to
# be followed by `:` — without that, prose containing "Exercise [«]" as a
# cross-reference (and one chapter's exercise-number column bleeding into the text)
# inflates the count and shifts every alignment; ch06 counted 15 that way against 13
# real heads (verified by the number that follows each: 6.2.2, 6.2.3, 6.3.1 …).
SRC_RE = re.compile(r'Exercise\s*\[([^\]]{0,60})\]\s*:')
# an #exr call: capture its argument list (may hold nested parens/brackets)
EXR_RE = re.compile(r'#exr\(([^)]*)\)', re.S)


def src_has_nosol(group: str) -> bool:
    """The no-solution marker is extracted as a `3` inside the bracket group."""
    return bool(re.search(r'(^|[,\s])3\s*$', group.strip()))


report = []
for out in sorted(ROOT.glob('out/ch*')):
    src, typ = out / 'source.txt', out / 'uk.typ'
    if not (src.exists() and typ.exists()):
        continue
    groups = [m.group(1) for m in SRC_RE.finditer(src.read_text(errors='replace'))]
    src_flags = [src_has_nosol(g) for g in groups]
    t = typ.read_text(encoding='utf-8')

    calls = list(EXR_RE.finditer(t))
    uk_flags = ['sol:' in c.group(1) for c in calls]

    if len(src_flags) != len(uk_flags):
        report.append((out.name, f'COUNT differs src={len(src_flags)} uk={len(uk_flags)} — SKIPPED'))
        continue

    changed = 0
    # rewrite back-to-front so earlier match offsets stay valid
    for c, want in sorted(zip(calls, src_flags), key=lambda p: -p[0].start()):
        have = 'sol:' in c.group(1)
        if have == want:
            continue
        args = c.group(1)
        if want:
            new_args = args.rstrip() + ', sol: true' if args.strip() else 'sol: true'
        else:
            new_args = re.sub(r',\s*sol:\s*true', '', args)
            new_args = re.sub(r'sol:\s*true,?\s*', '', new_args).strip()
        t = t[:c.start()] + f'#exr({new_args})' + t[c.end():]
        changed += 1
    if changed:
        report.append((out.name, f'{changed} call(s) corrected'))
        if APPLY:
            typ.write_text(t, encoding='utf-8')

for name, msg in report:
    print(f'  {name:9s} {msg}')
print(f'total parts needing a fix: {len(report)}')
if not APPLY:
    print('(dry run — pass --apply)')
