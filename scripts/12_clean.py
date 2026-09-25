#!/usr/bin/env python3
"""Build a clean, structure-marked plain-text source per unit.

Reads the PDF line-by-line (PyMuPDF dict), in reading order, and emits:

    # Chapter title                     <- level-1 (chapter/part opener)
    ## 1.2 A Linear Type System         <- level-2 (top section: Gd 10.5)
    ### Syntax                          <- level-3 (subsection: Gd 9.7)
    [Figure 1-3: caption]               <- captions kept, marked
    prose lines joined into paragraphs, hyphenation repaired

Running heads and page numbers are dropped by position. Nothing is deleted
otherwise: unknown lines are kept verbatim so no content can be lost.
"""
import fitz, pathlib, json, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
doc = fitz.open(next(ROOT.glob("*.pdf")))
UNITS = json.load(open(ROOT / "src" / "units.json"))

OUT = ROOT / "src" / "clean"
OUT.mkdir(parents=True, exist_ok=True)


def page_lines(p):
    """Lines of a page as [{'y','x','size','font','text'}], reading order."""
    items = []
    for blk in doc[p].get_text("dict")["blocks"]:
        for line in blk.get("lines", []):
            spans = [s for s in line["spans"] if s["text"].strip()]
            if not spans:
                continue
            items.append({
                "y": round(min(s["bbox"][1] for s in spans), 1),
                "x": round(min(s["bbox"][0] for s in spans), 1),
                "size": round(max(s["size"] for s in spans), 1),
                "font": spans[0]["font"],
                "text": " ".join(s["text"].strip() for s in spans).strip(),
            })
    items.sort(key=lambda i: (i["y"], i["x"]))
    # merge items that share a baseline (number + title on the same line)
    merged = []
    for it in items:
        if merged and abs(merged[-1]["y"] - it["y"]) < 1.0:
            merged[-1]["text"] = (merged[-1]["text"] + " " + it["text"]).strip()
            continue
        merged.append(dict(it))
    return merged


def is_running_head(it, page, unit_title_words):
    """Header/footer: near the top or bottom edge, and looks like a title or a number."""
    if it["y"] < 74 or it["y"] > 592:
        t = it["text"]
        if re.fullmatch(r"[\divxlIVXL]+", t):
            return True
        if any(w in t for w in unit_title_words if len(w) > 3):
            return True
        if re.match(r"^\d{1,2}\s", t) and it["size"] < 10.6:
            return True
        if it["size"] <= 8.3:
            return True
    return False


FIGCAP = re.compile(r"^(Figure|Table|Fig\.)\s*[0-9A-Z]")

report = []
for unit, info in UNITS.items():
    a, b = info["first"], info["last"]
    title_words = set()
    out_lines = []
    prev = None
    for p in range(a, b + 1):
        # learn the chapter title words from the unit's first page
        if p == a:
            for it in page_lines(p):
                if it["size"] >= 13 and it["font"].startswith("F8"):
                    title_words |= {w for w in re.findall(r"[A-Za-z]+", it["text"])}
        for it in page_lines(p):
            if is_running_head(it, p, title_words):
                continue
            t = it["text"]
            size, font = it["size"], it["font"]
            big = size >= 11.9 or (font == "Gd" and size >= 9.6)
            lvl = None
            if big:
                if p == a and size >= 13:
                    lvl = 1
                elif font == "Gd" and size >= 10.0:
                    lvl = 2
                else:
                    lvl = 3
            if lvl:
                out_lines.append(("break",))
                num = re.match(r"^((?:\d{1,2}\.){1,3}|[A-Z])\s*(.*)$", t)
                label = f"{num.group(1)} {num.group(2)}".strip() if num and num.group(2) else t
                out_lines.append(("head", lvl, label))
                prev = None
                continue
            if FIGCAP.match(t):
                out_lines.append(("break",))
                out_lines.append(("cap", t))
                prev = None
                continue
            # body text: join continuation lines
            if prev is not None and out_lines and out_lines[-1][0] == "body":
                last = out_lines[-1][1]
                if re.search(r"[A-Za-z]-$", last) and t[:1].islower():
                    out_lines[-1] = ("body", last[:-1] + t)          # de-hyphenate
                else:
                    out_lines[-1] = ("body", last + " " + t)
            else:
                out_lines.append(("body", t))
            prev = p
        out_lines.append(("break",))   # page boundary always breaks a paragraph

    buf = []
    for item in out_lines:
        if item[0] == "break":
            if buf and buf[-1] != "":
                buf.append("")
            continue
        if item[0] == "head":
            level = "#" * item[1]
            if buf and buf[-1] != "":
                buf.append("")
            buf.append(f"{level} {item[2]}")
            buf.append("")
        elif item[0] == "cap":
            if buf and buf[-1] != "":
                buf.append("")
            buf.append(f"[{item[1]}]")
            buf.append("")
        else:
            buf.append(item[1])
    text = re.sub(r"\n{3,}", "\n\n", "\n".join(buf)).strip() + "\n"
    (OUT / f"{unit}.txt").write_text(text, encoding="utf-8")
    words = len(re.findall(r"\S+", text))
    report.append((unit, info["words"], words, text.count("\n## "), text.count("\n### ")))

print(f"{'unit':7s} {'raw':>7s} {'clean':>7s} {'##':>4s} {'###':>4s}")
for u, r, c, h2, h3 in report:
    print(f"{u:7s} {r:7d} {c:7d} {h2:4d} {h3:4d}")
