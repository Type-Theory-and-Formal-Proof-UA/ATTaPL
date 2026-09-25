#!/usr/bin/env python3
"""Quote bare multi-letter identifiers in Typst math, driven by the compiler.

Typst reports `unknown variable: mk` for an unquoted identifier inside `$…$`.
This loops: compile, take the line/name from the error, quote that name on that
line (only where it sits inside a math span and is not already quoted), repeat.
Bounded, and it reports every change so the diff can be reviewed.

Usage: 44_quotemath.py <file.typ> [max_iterations]
"""
import pathlib, re, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
path = pathlib.Path(sys.argv[1])
limit = int(sys.argv[2]) if len(sys.argv) > 2 else 200
changes = []


def quote_on_line(line, name):
    """Quote `name` inside math spans on this one line, skipping quoted text."""
    out, i, in_math, in_str = [], 0, False, False
    while i < len(line):
        ch = line[i]
        if ch == '"':
            in_str = not in_str
            out.append(ch)
            i += 1
            continue
        if ch == "$" and not in_str:
            in_math = not in_math
            out.append(ch)
            i += 1
            continue
        if (in_math and not in_str and line.startswith(name, i)
                and (i == 0 or not (line[i - 1].isalnum() or line[i - 1] in '._"'))
                and (i + len(name) >= len(line) or not (line[i + len(name)].isalnum() or line[i + len(name)] == '.'))):
            out.append(f'"{name}"')
            i += len(name)
            continue
        out.append(ch)
        i += 1
    return "".join(out)


for it in range(limit):
    r = subprocess.run(["typst", "compile", "--root", str(ROOT), str(path), "/tmp/_q.pdf"],
                       capture_output=True, text=True)
    if r.returncode == 0:
        print(f"compiles after {it} fix(es)")
        break
    m = re.search(r'unknown variable: (\S+)', r.stderr)
    lm = re.search(re.escape(str(path)) + r":(\d+):", r.stderr)
    if not m or not lm:
        print("no more auto-fixable errors; remaining stderr:\n", r.stderr[:1200])
        break
    name, ln = m.group(1), int(lm.group(1))
    lines = path.read_text(encoding="utf-8").split("\n")
    new = quote_on_line(lines[ln - 1], name)
    if new == lines[ln - 1]:
        print(f"cannot quote {name!r} on line {ln}; stopping\n", r.stderr[:600])
        break
    lines[ln - 1] = new
    path.write_text("\n".join(lines), encoding="utf-8")
    changes.append((ln, name))
    print(f"line {ln}: quoted {name!r}")

print(f"\n{len(changes)} change(s):")
for ln, name in changes:
    print(f"   line {ln}: {name}")
