// Вхід для PDF: та сама книжка, але блоки коду оформлює codly.
// HTML збирається з book/attapl-uk.typ: сітки codly Typst не вміє експортувати в HTML.
#import "@preview/codly:1.3.0": codly, codly-init
#show: codly-init.with()
#codly(number-format: none, display-icon: false, display-name: false,
  zebra-fill: none, fill: luma(96%), stroke: 0.4pt + luma(30%), radius: 2pt,
  inset: 0.45em, lang-inset: 0pt)
#include "/book/attapl-uk.typ"
