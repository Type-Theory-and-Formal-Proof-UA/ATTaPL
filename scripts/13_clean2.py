#!/usr/bin/env python3
"""Cleaner v2: span-gap spacing (small caps), heading repair, figure delimiters.

Emits structure-marked text:
   # 1 Substructural Type Systems        (chapter opener, with level)
   **David Walker**                      (author line)
   ## 1.2 A Linear Type System
   ### Syntax
   <<<FIGURE Figure 1-3: ...>>>          (figure block opener)
   [Figure 1-3: ...]                     (caption)
   <<<END>>>
Everything not recognised is body text, joined into paragraphs.
"""
import fitz, pathlib, json, re, unicodedata

ROOT = pathlib.Path(__file__).resolve().parent.parent
doc = fitz.open(next(ROOT.glob("*.pdf")))
UNITS = json.load(open(ROOT / "src" / "units.json"))
OUT = ROOT / "src" / "clean"
OUT.mkdir(parents=True, exist_ok=True)

PUA_BIG = {0xF8F1: "⎧", 0xF8F2: "⎪", 0xF8F3: "⎩", 0xF8F4: "⎨",
           0xF8EB: "⎡", 0xF8EC: "⎢", 0xF8ED: "⎣", 0xF8EE: "⎤", 0xF8EF: "⎥", 0xF8F0: "⎦"}
LIG = {"\ufb00": "ff", "\ufb01": "fi", "\ufb02": "fl", "\ufb03": "ffi", "\ufb04": "ffl",
       "\u2018": "\u2019", "\u201b": "\u2019", "\u00ad": "", "\u200b": ""}
GLYPH_FIX = {"\x16": "\u2aaf", "\x0f": "\u03f5", "\x05": "\u22c4", "\x01": "", "\x02": "",
             "\x03": "", "\x04": ""}


def fix_text(s):
    for k, v in LIG.items():
        s = s.replace(k, v)
    for k, v in GLYPH_FIX.items():
        s = s.replace(k, v)
    for k, v in PUA_BIG.items():
        s = s.replace(chr(k), v)
    return re.sub(r"\s+", " ", s)


def line_text(line):
    """Join a line's spans, inserting a space where the horizontal gap demands one."""
    parts = []
    prev = None
    for s in line["spans"]:
        t = s["text"]
        if not t.strip() and prev is None:
            continue
        if prev is not None:
            gap = s["bbox"][0] - prev["bbox"][2]
            starts_word = t[:1].isalnum() or (t[:1] and ord(t[:1]) > 0x2000 and t[:1] not in ".,;:!?")
            ends_open = parts and parts[-1][-1:] in "([{\"“'’"
            if gap > 0.55 and starts_word and not ends_open:
                if not parts[-1].endswith(" ") and not t.startswith(" "):
                    parts.append(" ")
            elif gap < -0.2 and starts_word and not ends_open:
                if not parts[-1].endswith(" ") and not t.strip().startswith(" "):
                    parts.append(" ")
        parts.append(t)
        prev = s
    return fix_text("".join(parts)).strip()


def page_items(p):
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
                "text": line_text(line),
            })
    items.sort(key=lambda i: (i["y"], i["x"]))
    merged = []
    for it in items:
        if merged and abs(merged[-1]["y"] - it["y"]) < 1.0:
            merged[-1]["text"] = (merged[-1]["text"].rstrip() + " " + it["text"].lstrip()).strip()
            continue
        merged.append(dict(it))
    return merged


SMALLCAP = re.compile(r"^([A-Z]) ([a-z][a-z]+(?:-[a-z]+)*)\b")
NUMHEAD = re.compile(r"^((?:\d{1,2}\.\s?){1,3})(?=\S)")


def repair_heading(t):
    t = re.sub(r"^(\d{1,2})\.\s+(\d{1,2})", r"\1.\2", t)          # '1. 1' -> '1.1'
    m = SMALLCAP.match(t)
    if m:
        rest = t[m.end():].lstrip()
        if rest[:1].isupper() or rest == "":
            t = m.group(1) + m.group(2) + t[m.end():]
    t = NUMHEAD.sub(lambda m: m.group(1).replace(" ", ""), t)
    return t.strip()


def is_head_foot(it, title_words, p):
    """Header/footer band = outside the text block. Band membership, not content,
    decides — a merged header item ('243 6.10 Notes') must not survive as content,
    and a section heading that starts at the top of a page must."""
    t = it["text"]
    if not t:
        return True
    if it["y"] < 60 or it["y"] > 610:
        return True
    return False


FIGCAP = re.compile(r"^(Figure|Table)\s*[0-9]+[-.][0-9]+\s*:")
report = []
for unit, info in UNITS.items():
    a, b = info["first"], info["last"]
    title_words = set()
    for it in page_items(a):
        if it["size"] >= 13:
            title_words |= {w for w in re.findall(r"[A-Za-z]+", it["text"])}
    out = []
    for p in range(a, b + 1):
        for it in page_items(p):
            if is_head_foot(it, title_words, p):
                continue
            t, size, font = it["text"], it["size"], it["font"]
            t = repair_heading(t)
            big = size >= 11.9 or (font == "Gd" and size >= 9.6)
            if big:
                out.append(("break",))
                if p == a and size >= 13:
                    out.append(("head", 1, t))
                elif size >= 19:                      # part title
                    out.append(("head", 1, t))
                elif font == "Gd" and size >= 10.0:
                    out.append(("head", 2, t))
                else:
                    out.append(("head", 3, t))
                continue
            if p == a and size >= 9.8 and it["x"] > 250 and len(t) < 95:
                out.append(("author", t))
                continue
            if FIGCAP.match(t):
                out.append(("break",))
                out.append(("cap", t))
                continue
            if out and out[-1][0] == "body":
                last = out[-1][1]
                if re.search(r"[A-Za-z]-$", last) and t[:1].islower():
                    out[-1] = ("body", last[:-1] + t)
                else:
                    out[-1] = ("body", last + " " + t)
            else:
                out.append(("body", t))
        out.append(("break",))
    # merge level-1 heading pieces across a break (chapter titles wrap in the PDF)
    merged = []
    for item in out:
        if (item[0] == "head" and item[1] == 1 and merged
                and merged[-1] == ("break",) and len(merged) >= 2
                and merged[-2][0] == "head" and merged[-2][1] == 1):
            merged.pop()
            merged[-1] = ("head", 1, merged[-1][2] + " " + item[2])
            continue
        merged.append(item)
    out = merged
    buf = []
    for item in out:
        if item[0] == "break":
            if buf and buf[-1] != "":
                buf.append("")
        elif item[0] == "head":
            if buf and buf[-1] != "":
                buf.append("")
            buf.append("#" * item[1] + " " + item[2])
            buf.append("")
        elif item[0] == "author":
            buf.append("**" + item[1] + "**")
            buf.append("")
        elif item[0] == "cap":
            if buf and buf[-1] != "":
                buf.append("")
            buf.append("[" + item[1] + "]")
            buf.append("")
        else:
            buf.append(item[1])
    text = re.sub(r"\n{3,}", "\n\n", "\n".join(buf)).strip() + "\n"
    (OUT / f"{unit}.txt").write_text(text, encoding="utf-8")
    report.append((unit, info["words"], len(re.findall(r"\S+", text)),
                   text.count("\n## "), text.count("\n### ")))

print(f"{'unit':7s} {'raw':>7s} {'clean':>7s} {'##':>4s} {'###':>4s}")
for r in report:
    print(f"{r[0]:7s} {r[1]:7d} {r[2]:7d} {r[3]:4d} {r[4]:4d}")
