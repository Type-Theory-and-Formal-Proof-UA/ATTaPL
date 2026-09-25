#!/usr/bin/env python3
"""Split chapters into parts on real section boundaries and emit assignments.

Every part is a contiguous run of chapters' top-level sections (`## n.m Title`).
A part file carries ONLY its own slice of the source, so a child cannot drift
into a sibling's range.
"""
import pathlib, re, json, collections

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "src" / "clean"

# (child_slot, chapter, first_section, last_section inclusive, output part name)
# '' means the whole chapter; parent_slot marks the slice the parent translates.
PLAN = [
    ("parent", "ch06", "", "", "ch06p01"),
    ("child1", "ch01", "", "", "ch01p01"),
    ("child2", "ch02", "", "", "ch02p01"),
    ("child3", "ch03", "3.1", "3.4", "ch03p01"),
    ("child4", "ch03", "3.5", "3.8", "ch03p02"),
    ("child5", "ch04", "", "", "ch04p01"),
    ("child6", "ch05", "5.1", "5.4", "ch05p01"),
    ("child7", "ch05", "5.5", "5.8", "ch05p02"),
]


def mark_figures(text):
    """Wrap the paragraph just before each [Figure …]/[Table …] caption as that figure's body.

    In the PDF the caption sits under its box, so the box text precedes it.  Marking it
    explicitly keeps a child from having to guess where the box starts and ends.
    A caption is recognised by its "Figure N-M:" form, so prose that merely mentions a
    figure is never mistaken for one.
    """
    paras = text.split("\n\n")
    out = []
    for i, p in enumerate(paras):
        s = p.strip()
        if (re.match(r"^\[(Figure|Table)\s*\d+[-.]\d+\s*:", s) and out
                and out[-1].strip() and not out[-1].strip().startswith("[")):
            body = out.pop()
            out.append(f"<<<FIGURE-BODY: {s}>>>\n{body.strip()}\n<<<END-FIGURE-BODY>>>")
        out.append(p)
    return "\n\n".join(out)


def split_sections(text):
    """Return [(sec_num, sec_title, body_text, start_line)] for top-level sections."""
    lines = text.split("\n")
    idx = [i for i, l in enumerate(lines) if l.startswith("## ")]
    out = []
    for k, i in enumerate(idx):
        j = idx[k + 1] if k + 1 < len(idx) else len(lines)
        head = lines[i][3:].strip()
        m = re.match(r"^(\d{1,2}\.\d{1,2})\s+(.*)$", head)
        num, title = (m.group(1), m.group(2)) if m else ("", head)
        out.append((num, title, "\n".join(lines[i:j]), i))
    return out


def words(s):
    return len(re.findall(r"\S+", s))


manifest = {}
for slot, ch, first, last, part in PLAN:
    text = (SRC / f"{ch}.txt").read_text(encoding="utf-8")
    secs = split_sections(text)
    if not secs:
        secs = [("", ch, text, 0)]
    picked = [s for s in secs if (first == "" or first <= s[0] <= last)]
    if not picked:
        raise SystemExit(f"no sections selected for {part} ({ch} {first}-{last})")
    # slice: from the start of the first selected section to the start of the next
    # section after the last selected one (so trailing subsections are included)
    start_i = picked[0][3]
    after = [s for s in secs if s[3] > picked[-1][3]]
    end_i = after[0][3] if after else len(text.split("\n"))
    body = "\n".join(text.split("\n")[start_i:end_i]).strip() + "\n"

    # chapter header block: everything before the first section (title + intro)
    head = "\n".join(text.split("\n")[:secs[0][3]]).strip() + "\n"

    d = ROOT / "out" / part
    d.mkdir(parents=True, exist_ok=True)
    head, body = mark_figures(head), mark_figures(body)
    (d / "source.txt").write_text(
        f"<<< PART {part}: chapter {ch}"
        + (f", sections {first}..{last}" if first else ", whole chapter")
        + f" >>>\n\n=== CHAPTER HEADER (title, author, intro before first section) ===\n{head}\n"
        + "=== PART BODY ===\n" + body,
        encoding="utf-8")
    manifest[part] = {
        "slot": slot, "chapter": ch, "part": part,
        "sections": [f"{s[0]} {s[1]}" for s in picked],
        "words": words(head) + words(body),
        "source": f"out/{part}/source.txt",
        "output": f"out/{part}/uk.typ",
    }

(ROOT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"{'part':9s} {'slot':7s} {'ch':5s} {'words':>7s}  sections")
tot = 0
for p, m in manifest.items():
    tot += m["words"]
    print(f"{p:9s} {m['slot']:7s} {m['chapter']:5s} {m['words']:7d}  "
          + ", ".join(s.split()[0] for s in m["sections"]))
print("TOTAL words in wave:", tot)
