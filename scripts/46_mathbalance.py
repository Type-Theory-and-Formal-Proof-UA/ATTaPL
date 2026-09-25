#!/usr/bin/env python3
"""Report the first unmatched `$` in a Typst file.

Typst's own "unclosed delimiter" error points at the end of the file, which is
useless for finding the site. This walks the text tracking quoted strings and
reports the line where the math-delimiter parity first goes wrong, i.e. the last
line where a `$` opens a span that is never closed before the file ends.
"""
import pathlib, sys

path = pathlib.Path(sys.argv[1])
text = path.read_text(encoding="utf-8")
in_math = False
in_str = False
open_line = None
opens = []
for ln, line in enumerate(text.split("\n"), 1):
    i = 0
    while i < len(line):
        ch = line[i]
        if ch == "\\":
            i += 2
            continue
        if ch == '"':
            in_str = not in_str
        elif ch == "$" and not in_str:
            if not in_math:
                open_line = ln
                opens.append(ln)
            in_math = not in_math
        i += 1
    if in_str:
        # a quote left open at end of line is its own bug; report and reset
        print(f"line {ln}: unterminated string quote")
        in_str = False

if in_math:
    print(f"UNCLOSED math span opened on line {open_line} (parity flips there)")
    print("   context:")
    lines = text.split("\n")
    print("   ", lines[open_line - 1][:200])
else:
    print("all math spans balanced")
print(f"total '$' = {text.count('$')} (must be even: {text.count('$') % 2 == 0})")
