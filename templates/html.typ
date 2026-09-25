// Правила показу для HTML-експорту (typst compile --features html --format html).
// У PDF нічого не змінюють: кожне правило спрацьовує лише коли target() == "html".
#import "/templates/preamble.typ": html-width, html-frame

#let html-support(body) = {
  // Сітки й стеки — через SVG-рамку (див. preamble.typ).
  show grid: it => context if target() == "html" { html-frame(block(width: html-width, it)) } else { it }
  show stack: it => context if target() == "html" { html-frame(block(width: html-width, it)) } else { it }
  // Вирівнювання — через CSS.
  show align: it => context if target() == "html" {
    let x = it.alignment.x
    let css = if x == center { "center" } else if x == right or x == end { "right" } else { "left" }
    html.elem("div", attrs: (class: "al", style: "text-align: " + css), it.body)
  } else { it }
  show line: it => context if target() == "html" {
    html.elem("div", attrs: (style: "border-top: 0.5pt solid currentColor; margin: 0.2em auto; width: calc(" + repr(it.length.ratio) + " + " + repr(it.length.length) + ")"))
  } else { it }
  // Горизонтальні проміжки: HTML-експорт їх ігнорує, тож ставимо звичайний пропуск.
  show h: it => context if target() == "html" and it.amount != 1fr { sym.space } else { it }
  // Поля (номер вправи в розв'язках додатка A) у HTML не мають сенсу — друкуємо в потоці.
  show place: it => context if target() == "html" { [#it.body ] } else { it }
  body
}
