#!/usr/bin/env python3
"""Find the first place a Typst file's bracket nesting goes negative.

Typst reports "unexpected closing bracket" at the stray `]`, but the real defect
is normally an earlier `[` that never closed (or a `$` that swallowed it). This
walks the file tracking math mode and strings, ignoring brackets inside `$…$`
(Typst math has its own delimiters) and inside quoted strings, and prints the
line where the content-mode depth first goes below zero.
"""
import sys
import pathlib

path = pathlib.Path(sys.argv[1])
depth = 0
in_math = False
in_str = False
esc = False
for lineno, line in enumerate(path.read_text(encoding="utf-8").split("\n"), 1):
    i = 0
    while i < len(line):
        ch = line[i]
        if esc:
            esc = False
        elif ch == "\\":
            esc = True
        elif in_str:
            if ch == '"':
                in_str = False
        elif ch == '"':
            in_str = True
        elif ch == "$":
            in_math = not in_math
        elif not in_math:
            if ch == "[":
                depth += 1
            elif ch == "]":
                depth -= 1
                if depth < 0:
                    print(f"FIRST NEGATIVE at line {lineno} col {i+1}: {line[:100]}")
                    sys.exit(0)
        i += 1
    if in_math:
        # math spans may cross lines, that is fine; just note it
        pass
print(f"final depth={depth} in_math={in_math} (0/False = balanced)")
