// ============================================================================
// Advanced Topics in Types and Programming Languages — український переклад
// Спільна преамбула. НЕ редагувати в межах перекладу глав: це спільний файл.
// ============================================================================
// codly оформлює блоки коду в PDF (book/attapl-uk-pdf.typ); дошки правил його не потребують.
#import "@preview/codly:1.3.0": no-codly
#set page(
  paper: "a4",
  margin: (x: 22mm, y: 20mm),
  numbering: "1",
  header: context {
    let pg = counter(page).get().first()
    if pg > 1 {
      set text(size: 8.5pt, fill: luma(90))
      grid(columns: (1fr, 1fr), align: (left, right),
        [#currentchapter.get()], [#pg])
    }
  },
)

#set text(
  font: ("STIX Two Text",),
  size: 10.5pt,
  lang: "uk",
  hyphenate: true,
)
#set par(leading: 0.72em, first-line-indent: 1.25em, spacing: 1.05em, justify: true)
#show raw: set text(font: ("DejaVu Sans Mono", "Menlo", "Courier New"), size: 9pt)

// --- змінні стану -----------------------------------------------------------
#let currentchapter = state("chapter", "")
#let currentauthor = state("author", "")
#let secprefix = state("secprefix", "0.0")
#let stmtnum = counter("stmt")

// --- HTML-експорт ------------------------------------------------------------
// Експорт у HTML (експериментальний) не має рушія верстки: сітки, позиціонування
// й блоки з рамкою верстаються через `html.frame` — вбудований SVG. Ширина рамки
// — це ширина текстового блоку PDF: без сторінки `1fr` згорнулось би в нуль.
#let html-width = 42em
#let html-frame(body) = html.elem("div", attrs: (class: "frame"), html.frame(body))

// --- структурні заголовки ---------------------------------------------------
// Глава: #chap("1", "Substructural Type Systems")[David Walker]
#let chap(num, title, author) = {
  currentchapter.update(if num == "" { title } else { num + " " + title })
  secprefix.update("0.0")
  stmtnum.update(0)
  context if target() == "html" {
    // Експорт у HTML: розділювач сторінок tools/split_html.py ріже за <h2 class="chapter">.
    html.elem("h2", attrs: (class: "chapter", id: "ch" + num),
      if num == "" { title } else { num + " " + title })
    if author != [] { html.elem("p", attrs: (class: "author"), emph(author)) }
  } else {
    pagebreak(weak: true)
    v(2em)
    text(size: 22pt, weight: "regular")[
      #if num != "" [#grid(columns: (2.2em, 1fr), column-gutter: 0.6em)[
        #text(fill: luma(120))[#num]
      ][#title]] else [#title]
    ]
    if author != [] {
      v(0.5em)
      align(right)[#emph(author)]
    }
    v(1.2em)
  }
}

// Розділ (section): сам задає нумерацію тверджень цього розділу.
#let sec(num, title) = {
  secprefix.update(num)
  stmtnum.update(0)
  heading(level: 2, outlined: false, bookmarked: true)[#num #title]
}
// Підрозділ (subsection)
#let subsec(title) = heading(level: 3, outlined: false, bookmarked: false)[#title]
#let subsubsec(title) = heading(level: 4, outlined: false, bookmarked: false)[#title]

// --- середовища тверджень ---------------------------------------------------
// Друкують «Lemma 1.2.3.» за схемою глава.розділ.№ — як в оригіналі.
#let _stmt(kind, it, extra: none) = {
  stmtnum.step()
  context {
    let p = secprefix.get()
    let n = stmtnum.get().first()
    let label = if p == "0.0" { str(n) } else { p + "." + str(n) }
    // ВАЖЛИВО: без `par` — обгортка в par() робить вміст рядковим, і будь-який
    // блоковий елемент усередині твердження (напр. #numbered-список) Typst
    // мовчки відкидає з попередженням «... may not occur inside of a paragraph».
    block[
      #strong[#kind #label]
      #if extra != none [#extra]
      . #h(0.35em) #it
    ]
  }
}
#let thm(it) = _stmt("Theorem", it)
#let lem(it) = _stmt("Lemma", it)
#let cor(it) = _stmt("Corollary", it)
#let defn(it) = _stmt("Definition", it)
#let prop_(it) = _stmt("Proposition", it)
#let claim(it) = _stmt("Claim", it)
#let notation(it) = _stmt("Notation", it)
#let convention(it) = _stmt("Convention", it)
#let fact(it) = _stmt("Fact", it)
#let axiom(it) = _stmt("Axiom", it)
#let example(it) = _stmt("Example", it)
#let remark(it) = _stmt("Remark", it)
#let principle(it) = _stmt("Principle", it)
#let note_(it) = _stmt("Note", it)
#let figure_(it) = _stmt("Figure", it)
#let table_(it) = _stmt("Table", it)
// Вправа: #exr[текст]  або #exr(diff: "««", sol: true, rec: true)[текст]
#let exr(it, diff: none, sol: false, rec: false) = {
  let bits = ()
  if rec { bits.push("Recommended") }
  if diff != none { bits.push(diff) }
  // The no-solution marker is a SLASHED RIGHT ARROW (↛) in the book, not a check
  // mark: the Preface defines "Exercise [↛]" as "solution not in Appendix A", and the
  // extractor decodes the glyph as a `3` (font F0).  A ✓ asserts the opposite.
  if sol { bits.push("↛") }
  let extra = if bits.len() > 0 { " [" + bits.join(", ") + "]" } else { none }
  _stmt("Exercise", it, extra: extra)
}

// --- додаток A: розв'язки вибраних вправ -----------------------------------
// Друкує номер вправи в лівому полі, як в оригіналі, і слово SOLUTION:.
#let soln(num, it) = block[
  #place(start + top, dx: -3.4em)[#text(size: 9.5pt)[#num]]
  #strong[#text(size: 10pt)[SOLUTION:]] #h(0.35em) #it
]
// Деякі вправи в книзі супроводжено не розв'язком, а вказівкою (HINT:).
#let hint(num, it) = block[
  #place(start + top, dx: -3.4em)[#text(size: 9.5pt)[#num]]
  #strong[#text(size: 10pt)[HINT:]] #h(0.35em) #it
]

// Твердження самого додатка A: номер (A.1, A.2, …) у лівому полі та заголовок
// малими капітелями («LEMMA:», «THEOREM [FUNDAMENTAL THEOREM]:»), як у книзі.
// Це окрема нумерація — вона не збігається з нумерацією тверджень у розділах.
#let astmt(num, head, it) = block[
  #place(start + top, dx: -3.4em)[#text(size: 9.5pt)[#num]]
  #strong[#smallcaps(head)] #h(0.35em) #it
]
// Курсивне «Proof:» у додатку (як і в розділах).
#let proof_(it) = block[#emph[Proof:] #h(0.35em) #it]
// Порожній квадрат у кінці доведення — у книзі це □ (U+25A1).
#let qed = $square$

// --- блоки правил / фігур ---------------------------------------------------
// Дошка для правил виведення, боксів синтаксису й таблиць: текст усередині
// зберігає розбиття на рядки (саме так воно надруковано в книзі).
#let rules(body, scale: 0.94) = context {
  let box = block(
    width: if target() == "html" { html-width } else { 100% }, inset: 7pt, radius: 0pt,
    stroke: (paint: luma(60), thickness: 0.5pt),
  )[
    #set text(size: 10.5pt * scale)
    #set par(justify: false, first-line-indent: 0em, leading: 0.60em)
    #set block(spacing: 0.45em)
    #no-codly(body)
  ]
  if target() == "html" { html-frame(box) } else { box }
}
// Правило виведення у два стовпці: посилки над рискою, висновок під нею.
#let rule(premises, name, conclusion) = block(breakable: false)[ // premises/conclusion positional
  #grid(columns: 2, column-gutter: 1.2em, align: (center + horizon, right + horizon),
    $#premises$, text(size: 8.5pt, fill: luma(70))[#name])
  #v(-0.35em)
  #line(length: 100%, stroke: 0.5pt)
  #v(-0.15em)
  #align(center)[$#conclusion$]
]
#let figure(caption, body) = block(width: 100%, breakable: false)[
  #body
  #v(0.25em)
  #align(center)[#text(size: 9.5pt)[#caption]]
]

// Номер виключної формули, окремим рядком праворуч — як в оригіналі.
#let eqnnum(num) = align(right)[#text(size: 9.5pt)[(#num)]]

// Номер рівняння всередині абзацу: текст вигляду «…, (7.32) де …»
#let eqnnum_inline(num) = text(size: 9.5pt)[(#num)]
// Нумерована виключна формула: #eqn($...$, "7.1") — номер у правому полі, як в оригіналі.
#let eqn(body, num) = context {
  let box = block(width: if target() == "html" { html-width } else { 100% }, breakable: false)[
    #place(right + horizon, text(size: 9.5pt)[(#num)])
    #align(center)[$#body$]
    #v(-0.35em)
  ]
  if target() == "html" { html-frame(box) } else { box }
}

// Нумерований список із довільним стилем нумерації: #numbered("(i)", [...], [...])
#let numbered(numbering, ..items) = enum(numbering: numbering, ..items.pos())

// --- дрібні позначки --------------------------------------------------------
#let todo = text(fill: rgb("#b00"), weight: "bold")[TODO]
#let q = $q$                       // кваліфікатор: lin / un
#let ukr(s) = text(lang: "uk")[#s]
