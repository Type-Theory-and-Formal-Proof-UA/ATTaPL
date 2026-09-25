#!/usr/bin/env python3
"""Split the remaining units (ch07..ch10, appendix A) into parts and merge them
into manifest.json without disturbing the ch01..ch06 entries.

Same slicing rules as scripts/30_split.py: a part is a contiguous run of
top-level sections, its source.txt carries only its own slice, and the paragraph
before each figure caption is wrapped in <<<FIGURE-BODY: …>>> markers.

Usage: 31_split_rest.py [chapter ...]      (default: every planned chapter)
"""
import pathlib, re, json, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "src" / "clean"

# chapter -> [(first_section, last_section inclusive, part name)]
PLAN = {
    "ch07": [("7.1", "7.4", "ch07p01"),
             ("7.5", "7.6", "ch07p02"),
             ("7.7", "7.8", "ch07p03")],
    "ch08": [("8.1", "8.4", "ch08p01"),
             ("8.5", "8.6", "ch08p02"),
             ("8.7", "8.9", "ch08p03"),
             ("8.10", "8.11", "ch08p04")],
    "ch09": [("9.1", "9.2", "ch09p01"),
             ("9.3", "9.4", "ch09p02")],
    "ch10": [("10.1", "10.1", "ch10p01"),
             ("10.2", "10.2", "ch10p02"),
             ("10.3", "10.5", "ch10p03"),
             ("10.6", "10.7", "ch10p04"),
             ("10.8", "10.8", "ch10p05")],
}


def mark_figures(text):
    """Wrap the paragraph just before each [Figure …]/[Table …] caption."""
    paras = text.split("\n\n")
    out = []
    for p in paras:
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
        # Зазвичай «8.1 Basic Modularity», але трапляється й «HM(X) 10.3» —
        # номер у кінці заголовка. Беремо номер з будь-якого місця рядка.
        m = re.search(r"(?<![\w.])(\d{1,2}\.\d{1,2})(?![\d.])", head)
        if m:
            num = m.group(1)
            title = (head[:m.start()] + head[m.end():]).strip()
        else:
            num, title = "", head
        out.append((num, title, "\n".join(lines[i:j]), i))
    return out


def words(s):
    return len(re.findall(r"\S+", s))


def build(ch):
    text = (SRC / f"{ch}.txt").read_text(encoding="utf-8")
    secs = split_sections(text)
    if not secs:
        raise SystemExit(f"no sections found in {ch}")
    lines = text.split("\n")
    head = "\n".join(lines[:secs[0][3]]).strip() + "\n"
    made = {}
    for first, last, part in PLAN[ch]:
        # Порівнюємо номери ЧИСЛОВО: рядкове "8.10" <= "8.4" хибне й зіпсувало б
        # діапазон у ch08/ch10 (той самий ґандж, що був у scripts/41_numcheck.py).
        vk = lambda s: tuple(int(x) for x in s.split("."))
        picked = [s for s in secs if vk(first) <= vk(s[0]) <= vk(last)]
        if not picked:
            raise SystemExit(f"no sections selected for {part} ({first}-{last})")
        after = [s for s in secs if s[3] > picked[-1][3]]
        end_i = after[0][3] if after else len(lines)
        body = "\n".join(lines[picked[0][3]:end_i]).strip() + "\n"
        d = ROOT / "out" / part
        d.mkdir(parents=True, exist_ok=True)
        h, b = mark_figures(head), mark_figures(body)
        (d / "source.txt").write_text(
            f"<<< PART {part}: chapter {ch}, sections {first}..{last} >>>\n\n"
            f"=== CHAPTER HEADER (title, author, intro before first section) ===\n{h}\n"
            f"=== PART BODY ===\n{b}", encoding="utf-8")
        made[part] = {
            "slot": "parent", "chapter": ch, "part": part,
            "sections": [f"{s[0]} {s[1]}" for s in picked],
            "words": words(b), "source": f"out/{part}/source.txt",
            "output": f"out/{part}/uk.typ",
        }
    return made


def main():
    want = sys.argv[1:] or sorted(PLAN)
    man_path = ROOT / "manifest.json"
    man = json.loads(man_path.read_text()) if man_path.exists() else {}
    for ch in want:
        if ch not in PLAN:
            raise SystemExit(f"no plan for {ch}")
        made = build(ch)
        man.update(made)
        for part, info in made.items():
            print(f"{ch:5s} {part:8s} {len(info['sections']):2d} sections  {info['words']:6d} words  "
                  f"[{info['sections'][0].split()[0]}..{info['sections'][-1].split()[0]}]")
    man_path.write_text(json.dumps(man, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nmanifest.json now holds {len(man)} parts")


if __name__ == "__main__":
    main()
