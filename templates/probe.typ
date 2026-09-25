// Probe: verify every symbol spelling renders the intended glyph.
#set page(width: 200mm, height: 260mm, margin: 12mm)
#set text(font: ("STIX Two Text", "DejaVu Serif"), size: 11pt, lang: "uk")

// --- math symbol candidates ---
#let syms = (
  ("turnstile", sym.turnstile),
  ("arrow.r", sym.arrow.r),
  ("arrow.r.double", sym.arrow.r.double),
  ("arrow.r.double.long", sym.arrow.r.double.long),
  ("arrow.r.long.double", sym.arrow.r.long.double),
  ("arrow.l.r.double", sym.arrow.l.r.double),
  ("arrow.r.long.double.above", sym.arrow.r.long.double),
  ("preceq", sym.preceq),
  ("prec.eq", sym.prec.eq),
  ("subset.eq", sym.subset.eq),
  ("subset.eq.sq", sym.subset.eq.sq),
  ("in", sym.in),
  ("emptyset", sym.emptyset),
  ("forall", sym.forall),
  ("exists", sym.exists),
  ("and", sym.and),
  ("not", sym.not),
  ("eq.not", sym.eq.not),
  ("lt.eq", sym.lt.eq),
  ("gt.eq", sym.gt.eq),
  ("bot", sym.bot),
  ("top", sym.top),
  ("ell", sym.ell),
  ("partial", sym.partial),
  ("models", sym.models),
  ("arrow.up", sym.arrow.up),
  ("arrow.down", sym.arrow.down),
  ("colon.eq", sym.colon.eq),
  ("arrow.r.bar", sym.arrow.r.bar),
  ("lambda", sym.lambda),
  ("Sigma", sym.Sigma),
  ("Pi", sym.Pi),
  ("Psi", sym.Psi),
  ("rho", sym.rho),
  ("phi", sym.phi),
  ("epsilon", sym.epsilon),
  ("epsilon.alt", sym.epsilon.alt),
  ("sigma", sym.sigma),
  ("tau", sym.tau),
  ("kappa", sym.kappa),
  ("gamma", sym.gamma),
  ("beta", sym.beta),
  ("alpha", sym.alpha),
  ("mu", sym.mu),
  ("nu", sym.nu),
  ("diamond", sym.diamond),
  ("diamond.suit", sym.diamond.suit),
  ("times.circle", sym.times.circle),
  ("otimes", sym.otimes),
  ("star", sym.star),
  ("parallel", sym.parallel),
  ("dot.op", sym.dot.op),
  ("compose", sym.compose),
  ("circle.small", sym.circle.small),
  ("bullet", sym.bullet),
  ("angle.l", sym.angle.l),
  ("angle.r", sym.angle.r),
  ("triangle.r", sym.triangle.r),
  ("arrow.r.triple", sym.arrow.r.triple),
  ("equiv", sym.equiv),
  ("arrow.r.squiggly", sym.arrow.r.squiggly),
  ("arrow.r.long", sym.arrow.r.long),
  ("plus.minus", sym.plus.minus),
  ("minus", sym.minus),
  ("without", sym.without),
  ("sect", sym.sect),
  ("circle.filled", sym.circle.filled),
  ("square", sym.square),
  ("checkmark", sym.checkmark),
  ("crossmark", sym.crossmark),
  ("bar.v", sym.bar.v),
  ("integral", sym.integral),
  ("sum", sym.sum),
  ("prop", sym.prop),
  ("subset", sym.subset),
  ("union", sym.union),
  ("sect", sym.sect),
)

#for (name, s) in syms [
  #name: $#s$
]

#pagebreak()

// --- Cyrillic + apostrophe + text-mode symbols ---
Український текст: об’єкт, зв’язування, підстановка, типізація, змінна, регіон,
ефект, доведення, наслідок, означення, лема, теорема, твердження, приклад.
Апостроф U+2019: об’єкт. Апостроф U+02BC: обʼєкт. Прямий: об'єкт.

Грецькі в тексті: Γ ⊢ t : T, λ-числення, ρ, ϕ, ϵ, ⪯, ⋄, ⊗, ⋆, ∥, ⊥, ⊤, ∅.

// --- math-mode Greek and relations ---
$ Gamma tack t : T quad lambda x : T . t quad rho quad phi quad epsilon quad
  preceq quad diamond quad times.circle quad star quad parallel quad
  bot quad top quad emptyset quad
  arrow.r quad arrow.r.double quad arrow.r.double.long quad
  forall x in D, exists y eq.not z quad
  lt.eq quad gt.eq quad and quad not quad in quad subset.eq quad
  colon.eq quad models quad ell quad partial quad times quad dot.op quad
  angle.l x , y angle.r quad bar.v quad without quad
  Sigma quad Pi quad Psi quad Delta quad mu quad nu quad kappa quad
  circle.stroked.tiny quad compose quad plus.minus quad minus quad
  equiv quad arrow.r.long quad arrow.l.r.double quad
  arrow.r.bar quad arrow.r.hook quad arrow.r.squiggly quad
  subset quad union quad sect quad prop quad
  arrow.up quad arrow.down quad triangle.r quad square quad
$

// --- heading + environment helpers the children must use ---
#heading(level: 2, numbering: none)[1.1 Структурні властивості]
#heading(level: 3, numbering: none)[Синтаксис]
