#!/usr/bin/env python3
"""Split the back matter — appendix A (solutions), References, Index — into parts.

Appendix A is not divided into sections: it is a flat run of solutions keyed by
exercise number (e.g. `1.1.4`). So we slice it by CHAPTER: each part holds the
solutions for one or more chapters, and the boundary between chapters is found at
the first `NN.x.y` exercise number after the previous chapter's last one.

References and the Index are short enough to be single units.

Same output shape as scripts/31_split_rest.py so the parts are interchangeable.
"""
import pathlib, re, json, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "src" / "clean"

# appendix -> [(first_chapter, last_chapter inclusive, part name)]
APPA_PLAN = [(1, 4, "appap01"), (5, 7, "appap02"), (8, 10, "appap03")]
# back matter treated as whole units
WHOLE = {"refs": "refs01", "index": "index01"}

EXNUM = re.compile(r"(?<![\w.])(\d{1,2})\.\d{1,2}\.\d{1,2}(?![\d.])")


def words(s):
    return len(re.findall(r"\S+", s))


def chapter_offsets(text):
    """Return {chapter_number: char_offset_of_first_solution} for appendix A."""
    first = {}
    for m in EXNUM.finditer(text):
        ch = int(m.group(1))
        if ch not in first:
            first[ch] = m.start()
    return first


def build_appa():
    text = (SRC / "appa.txt").read_text(encoding="utf-8")
    lines = text.split("\n")
    # header: the title line(s) before the first solution
    offs = chapter_offsets(text)
    if not offs:
        raise SystemExit("appendix A: no exercise numbers found")
    head = text[:offs[min(offs)]].strip() + "\n"
    made = {}
    for first_ch, last_ch, part in APPA_PLAN:
        present = sorted(c for c in offs if first_ch <= c <= last_ch)
        if not present:
            raise SystemExit(f"appendix A: no solutions for {first_ch}..{last_ch}")
        start = offs[present[0]]
        after = sorted(offs[c] for c in offs if c > last_ch)
        end = after[0] if after else len(text)
        body = text[start:end].strip() + "\n"
        d = ROOT / "out" / part
        d.mkdir(parents=True, exist_ok=True)
        (d / "source.txt").write_text(
            f"<<< PART {part}: appendix A, solutions for chapters {first_ch}..{last_ch} >>>\n\n"
            f"=== UNIT HEADER ===\n{head}\n"
            f"=== PART BODY ===\n{body}", encoding="utf-8")
        made[part] = {
            "slot": "parent", "chapter": "appa", "part": part,
            "sections": [f"ch{first_ch}..ch{last_ch} solutions"],
            "words": words(body), "source": f"out/{part}/source.txt",
            "output": f"out/{part}/uk.typ",
        }
    return made


def build_whole(unit):
    part = WHOLE[unit]
    text = (SRC / f"{unit}.txt").read_text(encoding="utf-8")
    lines = text.split("\n")
    head = lines[0].strip() + "\n"          # the `# Title` line
    body = "\n".join(lines[1:]).strip() + "\n"
    d = ROOT / "out" / part
    d.mkdir(parents=True, exist_ok=True)
    (d / "source.txt").write_text(
        f"<<< PART {part}: {unit} (whole unit) >>>\n\n"
        f"=== UNIT HEADER ===\n{head}\n"
        f"=== PART BODY ===\n{body}", encoding="utf-8")
    return {part: {
        "slot": "parent", "chapter": unit, "part": part,
        "sections": [unit], "words": words(body),
        "source": f"out/{part}/source.txt", "output": f"out/{part}/uk.typ",
    }}


def main():
    want = sys.argv[1:] or ["appa"] + sorted(WHOLE)
    man_path = ROOT / "manifest.json"
    man = json.loads(man_path.read_text()) if man_path.exists() else {}
    for unit in want:
        if unit == "appa":
            made = build_appa()
        elif unit in WHOLE:
            made = build_whole(unit)
        else:
            raise SystemExit(f"unknown unit {unit}")
        man.update(made)
        for part, info in made.items():
            print(f"{unit:6s} {part:9s} {info['words']:6d} words  {info['sections'][0][:40]}")
    man_path.write_text(json.dumps(man, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nmanifest.json now holds {len(man)} parts")


if __name__ == "__main__":
    main()
