#!/usr/bin/env python3
"""Repair the equation-number placeholders in out/ch07p01/uk.typ.

An earlier regex substitution wrote the literal text `#(m.group(1))` where the
equation number belonged; the numbers themselves are known from the source, and
each placeholder sits in a fixed line whose preceding display formula identifies
it, so they are restored by line number.
"""
import pathlib

NUM = {
    104: "7.1", 108: "7.2",
    161: "7.3.2",
    201: "7.3.3", 228: "7.3.4",
    274: "7.4", 308: "7.3.6", 329: "7.3.7",
    365: "7.5", 434: "7.6", 459: "7.4.1",
    595: "7.7", 603: "7.4.2", 613: "7.8", 634: "7.9", 651: "7.4.3",
    686: "7.4.4", 695: "7.10", 704: "7.11", 712: "7.12", 720: "7.13",
}

path = pathlib.Path(__file__).resolve().parent.parent / "out/ch07p01/uk.typ"
lines = path.read_text(encoding="utf-8").split("\n")
for ln, num in sorted(NUM.items()):
    assert "m.group(1)" in lines[ln - 1], f"line {ln} is not a placeholder: {lines[ln-1][:70]!r}"
    lines[ln - 1] = f'#eqnnum("{num}")'
    print(f"line {ln:4d} -> ({num})")
path.write_text("\n".join(lines), encoding="utf-8")
print(f"\n{len(NUM)} equation numbers restored")
