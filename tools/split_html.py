#!/usr/bin/env python3
"""Розрізати односторінковий HTML-експорт Typst на сторінки по розділах.

    typst compile --root . --features html --format html book/attapl-uk.typ build/book.html
    python3 tools/split_html.py build/book.html site/

Typst видає весь текст одним файлом. Розділ книги позначено в preamble.typ як
<h2 class="chapter">, секції — <h3>. Скрипт

  * вирізає титульну частину й будує з неї index.html зі змістом (розділи → секції),
  * кладе кожен розділ на окрему сторінку chNN.html,
  * переносить кожну виноску на сторінку, що на неї посилається, і виправляє
    внутрішні посилання на «сторінка.html#якір»,
  * додає навігацію «назад / зміст / далі» та таблицю стилів,
  * для кожної сторінки дублює SVG-<symbol> гліфів, на які вона посилається
    (Typst визначає їх один раз у першому SVG і далі лише <use>).
"""
import html
import re
import sys
from pathlib import Path

PDF_NAME = "attapl-uk.pdf"

CSS = """
body { max-width: 46rem; margin: 0 auto; padding: 1rem 1rem 4rem;
       font: 18px/1.6 "Latin Modern Roman", "New Computer Modern", Georgia, serif; }
h1.title { font-size: 2.3rem; line-height: 1.2; margin: 2rem 0 .3rem; }
p.subtitle, p.authors { font-size: 1.2rem; margin: 0 0 .5rem; }
h2 { font-size: 1.9rem; margin: 1.5rem 0 .4rem; }
p.author { margin: 0 0 1.2rem; }
h3 { font-size: 1.4rem; margin-top: 2rem; }
h4 { font-size: 1.15rem; }
h5 { font-size: 1rem; }
a { color: #1a5fb4; }
p { margin: .65em 0; padding: .35em 0; }
/* довгі формули не переносяться: прокручуємо їх, а не розтягуємо сторінку */
div.al, p { overflow-x: auto; overflow-y: hidden; }
math[display] { overflow-x: auto; max-width: 100%; }
div.frame { margin: 1.1em 0; overflow-x: auto; }
svg { max-width: 100%; height: auto; }
nav.pager { display: flex; justify-content: space-between; gap: 1rem;
            font-family: system-ui, sans-serif; font-size: .9rem; margin: 1rem 0; }
nav.pager span { flex: 1; }
nav.pager span:nth-child(2) { text-align: center; }
nav.pager span:last-child { text-align: right; }
section[role=doc-endnotes] { border-top: 1px solid #999; margin-top: 3rem; font-size: .9rem; }
nav.toc ol { list-style: none; padding-left: 0; }
nav.toc ol ol { padding-left: 1.6rem; }
nav.toc > ol > li { margin-top: .8rem; font-weight: bold; }
nav.toc > ol > li li { font-weight: normal; margin-top: 0; }
"""


def text_of(fragment):
    return html.unescape(re.sub(r"<[^>]+>", "", fragment)).strip()


def main(src, out):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    doc = Path(src).read_text(encoding="utf-8")

    head = doc[: doc.index("</head>")]
    head = head.replace('<html lang="en">', '<html lang="uk">', 1)
    head = head.replace("<style>", f"<style>{CSS}\n", 1)  # наші стилі першими, математичні Typst — після
    body = doc[doc.index("<body>") + 6 : doc.rindex("</body>")]

    # Виноски Typst збирає в одну <section role="doc-endnotes"> у кінці.
    notes = []
    endnotes = re.search(r'<section role="doc-endnotes">(.*?)</section>', body, re.S)
    if endnotes:
        body = body.replace(endnotes.group(0), "")
        for li in re.finditer(r'<li id="([^"]+)">(.*?)</li>', endnotes.group(1), re.S):
            back = re.search(r'href="#([^"]+)"', li.group(2))
            notes.append((li.group(1), back.group(1), li.group(0)))

    symbols = {m.group(1): m.group(0)
               for m in re.finditer(r'<symbol id="([^"]+)".*?</symbol>', body, re.S)}

    starts = [m.start() for m in re.finditer(r'<h2 class="chapter"', body)]
    front, chunks = body[: starts[0]], []
    for i, s in enumerate(starts):
        chunks.append(body[s : starts[i + 1] if i + 1 < len(starts) else len(body)])

    pages = []  # (slug, назва, html, [(id, назва секції)])
    for chunk in chunks:
        m = re.match(r'<h2 class="chapter" id="ch(\d+)">(.*?)</h2>', chunk, re.S)
        num, title = int(m.group(1)), text_of(m.group(2))
        slug = f"ch{num:02d}"
        sections = []

        def anchor(h):
            label = text_of(h.group(1))
            n = re.match(r"(\d+(?:\.\d+)+)", label)
            sid = "s" + n.group(1).replace(".", "-") if n else f"s{len(sections)}"
            sections.append((sid, label))
            return f'<h3 id="{sid}">{h.group(1)}</h3>'

        chunk = re.sub(r"<h3>(.*?)</h3>", anchor, chunk, flags=re.S)
        pages.append((slug, title, chunk, sections))
    assert len({p[0] for p in pages}) == len(pages), "повторюваний розділ: перевірте #chap"

    # id -> сторінка; виноска живе на сторінці свого посилання
    where = {}
    for slug, _, chunk, _ in pages:
        for m in re.finditer(r'\bid="([^"]+)"', chunk):
            where[m.group(1)] = f"{slug}.html"
    by_page = {}
    for note_id, back_id, li in notes:
        by_page.setdefault(where[back_id], []).append(li)
        where[note_id] = where[back_id]

    def rewrite(fragment, current):
        def sub(m):
            target = where.get(m.group(1))
            if target is None:
                print(f"warning: dangling link #{m.group(1)}", file=sys.stderr)
                return m.group(0)
            return f'href="{"" if target == current else target}#{m.group(1)}"'
        return re.sub(r'(?<=\s)href="#([^"]+)"', sub, fragment)

    def with_symbols(fragment):
        defined = set(re.findall(r'<symbol id="([^"]+)"', fragment))
        missing, todo = [], re.findall(r'xlink:href="#([^"]+)"', fragment)
        while todo:
            sid = todo.pop()
            if sid in defined or sid not in symbols:
                continue
            defined.add(sid)
            missing.append(symbols[sid])
            todo += re.findall(r'xlink:href="#([^"]+)"', symbols[sid])
        if not missing:
            return fragment
        return ('<svg width="0" height="0" style="position:absolute" aria-hidden="true">'
                f'<defs>{"".join(missing)}</defs></svg>{fragment}')

    def pager(i):
        def link(j, fmt):
            if not 0 <= j < len(pages):
                return "<span></span>"
            return f'<span><a href="{pages[j][0]}.html">{fmt.format(html.escape(pages[j][1]))}</a></span>'
        mid = '<span><a href="index.html">Зміст</a></span>'
        return f'<nav class="pager">{link(i - 1, "← {}")}{mid}{link(i + 1, "{} →")}</nav>'

    title = "Поглиблені теми з типів та мов програмування"
    def write(name, page_title, content):
        doc_head = re.sub(r"<title>.*?</title>", "", head, flags=re.S)
        (out / name).write_text(
            f"{doc_head}<title>{html.escape(page_title)}</title></head><body>{content}</body></html>",
            encoding="utf-8")

    for i, (slug, ch_title, chunk, _) in enumerate(pages):
        nav = pager(i)
        if f"{slug}.html" in by_page:
            chunk += ('<section role="doc-endnotes"><ol style="list-style-type: none">'
                      + "".join(by_page[f"{slug}.html"]) + "</ol></section>")
        chunk = with_symbols(rewrite(chunk, f"{slug}.html"))
        write(f"{slug}.html", f"{ch_title} — {title}", nav + chunk + nav)

    toc = "".join(
        f'<li><a href="{slug}.html">{html.escape(ch_title)}</a><ol>'
        + "".join(f'<li><a href="{slug}.html#{sid}">{html.escape(label)}</a></li>' for sid, label in secs)
        + "</ol></li>"
        for slug, ch_title, _, secs in pages)
    write("index.html", title,
          f'<h1 class="title">{html.escape(title)}</h1>'
          f'<p class="authors">за редакцією Benjamin C. Pierce</p>'
          f'<p><a href="{PDF_NAME}">PDF</a></p>'
          f'<p>Переклад українською: розділи 1–9 (розділ 10 та додатки ще не перекладено). '
          f'Перекладено з видання <em>Advanced Topics in Types and Programming Languages</em>, '
          f'Benjamin C. Pierce (editor), The MIT Press, 2004.</p>'
          f'<nav class="toc"><ol>{toc}</ol></nav>')
    print(f"wrote {len(pages) + 1} pages to {out}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(*sys.argv[1:])
