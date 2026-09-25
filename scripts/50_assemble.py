#!/usr/bin/env python3
"""Assemble one Typst file per chapter from its part files, then compile each.

ch03 and ch05 have two parts each; everything else has one.  The assembled file is
a generated artifact: a fix in a part is not in the chapter until this runs again.
"""
import pathlib, json, subprocess, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
MAN = json.load(open(ROOT / "manifest.json"))
BOOK = ROOT / "book"
BOOK.mkdir(exist_ok=True)

chapters = {}
for part, info in MAN.items():
    chapters.setdefault(info["chapter"], []).append(part)
def sec_key(part):
    """Сортувати частини ЧИСЛОВО за номером першого розділу.

    Рядкове порівняння ставить "8.10" перед "8.2", через що глава склеюється
    в неправильному порядку (той самий ґандж, що був у 31_split_rest/41_numcheck).
    """
    s = MAN[part]["sections"][0].split()[0]
    try:
        # Абетковий манифестний номер збивав би бібліографію/покажчик, тому для
        # них номер розділу беремо з реального діапазону сторінок-джерел.
        m = re.match(r"^(\d+)\.(\d+)", s)
        if m:
            return (int(m.group(1)), int(m.group(2)), part)
    except Exception:
        pass
    return (0, 0, part)


# Порядок як у книзі: передмова, глави 1..10, тоді додаток A, тоді бібліографія
# і покажчик.  Сама лише абетка поставила б "appa"/"index"/"refs" ПЕРЕД "ch01",
# а "preface" — після "ch10".
BACK = {"preface": 0, "appa": 11, "refs": 12, "index": 13}


def book_key(ch):
    if ch in BACK:
        return BACK[ch], 0
    m = re.match(r"^ch(\d+)$", ch)
    return (int(m.group(1)), 0) if m else (99, 0)


for ch in chapters:
    chapters[ch] = sorted(chapters[ch], key=sec_key)

rows = []
translated = []
for ch in sorted(chapters):
    parts = chapters[ch]
    # Главу включаємо лише коли ВСІ її частини вже перекладено: інакше згенерований
    # book/<ch>.typ посилався б на неіснуючий out/<part>/uk.typ і валив збірку.
    if not all((ROOT / "out" / p / "uk.typ").exists() for p in parts):
        print(f"{ch:6s} {'+'.join(parts):22s} skip  (not translated yet)")
        continue
    translated.append(ch)
    out = BOOK / f"{ch}.typ"
    body = [f'// Згенеровано scripts/50_assemble.py — не редагувати вручну.\n']
    for p in parts:
        body.append(f'#include "/out/{p}/uk.typ"\n')
    out.write_text("".join(body), encoding="utf-8")
    r = subprocess.run(["typst", "compile", "--root", str(ROOT), str(out), str(ROOT / "build" / f"{ch}.pdf")],
                       capture_output=True, text=True)
    label = "+".join(parts)
    status = "ok" if r.returncode == 0 else "FAIL"
    pages = "-"
    pdf = ROOT / "build" / f"{ch}.pdf"
    if pdf.exists():
        import fitz
        pages = len(fitz.open(pdf))
    rows.append((ch, label, status, pages, r.stderr.strip().splitlines()[:2]))
    print(f"{ch:6s} {label:22s} {status:5s} pages={pages}")

bad = [r for r in rows if r[2] != "ok"]
print(f"\n{len(rows) - len(bad)}/{len(rows)} chapters compile")
for r in bad:
    print("  ", r[0], r[4])

# Головний файл книги — теж генерований: складаємо його з наявних глав, щоб
# додавання глави не вимагало правки руками (і не лишалося застарілим).
master = BOOK / "attapl-uk.typ"
body = ["// Згенеровано scripts/50_assemble.py — не редагувати вручну.\n",
        '// Усі перекладені розділи в одному документі.\n',
        '#import "/templates/html.typ": html-support\n',
        '#show: html-support\n',
        '#include "/templates/frontmatter.typ"\n']
for ch in sorted(chapters, key=book_key):
    if ch in translated:
        body.append(f'#include "/book/{ch}.typ"\n')
master.write_text("".join(body), encoding="utf-8")
r = subprocess.run(["typst", "compile", "--root", str(ROOT), str(master),
                    str(ROOT / "build" / "attapl-uk.pdf")], capture_output=True, text=True)
print("master book:", "ok" if r.returncode == 0 else "FAIL")
if r.returncode != 0:
    print("  ", r.stderr.strip().splitlines()[:3])
