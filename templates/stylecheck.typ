// Перевірка всіх конструкцій, які вимагає STYLE.md — щоб діти не билися об них.
#import "/templates/preamble.typ": *

#chap("1", "Пробна глава")[David Walker]

#sec("1.1", "Структурні властивості")

Текст із символом $in.not$, $epsilon.alt$, $phi.alt$, $nabla$, $zeta$, $eta$, $xi$, $forces$.

#lem[Якщо $Gamma_1, x_1 : T_1, Gamma_2 tack t : T$, то $Gamma_1, x_2 : T_2, Gamma_2 tack t : T$.]
#defn[Терм $t$ є #emph{значенням}, якщо він не має кроків зведення.]
#prop_[Твердження.]
#claim[Твердження.]
#notation[Позначення.]
#convention[Угода.]
#fact[Факт.]
#axiom[Аксіома.]
#example[Приклад.]
#remark[Зауваження.]
#cor[Наслідок.]

#exr(diff: "«", rec: true)[Доведіть лему про послаблення.]
#exr(diff: "«««", sol: true)[Покажіть, що типізація розв’язна.]
#exr[Проста вправа.]

#figure([Рисунок 1-1: Simply-typed lambda calculus with booleans], rules([
  Syntax #h(1em) $Gamma tack t : T$
  #linebreak()
  #rule(
    $Gamma tack t_1 : T_11 -> T_12 quad Gamma tack t_2 : T_11$,
    "T-App",
    $Gamma tack t_1 t_2 : T_12$,
  )
]))

#rules([
  #set align(left)
  booleans: $b ::= "true" mid "false"$
  #linebreak()
  types: $T ::= "Bool" mid T times T mid T -> T$
])

#subsec("Синтаксис")
Підрозділ.
#subsubsec("Ще глибше")
Підпідрозділ.

Літеральні символи в математиці: $⊗$, $⋄$, $⋆$, $∥$, $▶$, $⪯$.
Інші: $arrow.r.double$, $arrow.l.r.double$, $arrow.l.r.double.long$, $arrow.r.bar$,
$arrow.t$, $arrow.b$, $prec.eq$, $prec.curly.eq$, $subset.eq.sq$, $subset.eq$, $supset.eq$,
$in$, $emptyset$, $models$, $forces$, $triangle.r$, $square$, $chevron.l x chevron.r$,
$infinity$, $ell$, $partial$, $equiv$, $approx$, $tilde$, $tilde.eq$, $compose$,
$dot.op$, $star$, $parallel$, $colon.eq$, $lt.eq$, $gt.eq$, $eq.not$, $and$, $or$, $not$,
$bot$, $top$, $lambda$, $Gamma$, $Delta$, $Pi$, $Sigma$, $Psi$, $Lambda$, $Omega$,
$alpha$, $beta$, $gamma$, $delta$, $epsilon$, $theta$, $kappa$, $mu$, $nu$, $rho$,
$sigma$, $tau$, $phi$, $chi$, $psi$, $omega$, $forall$, $exists$, $without$, $eq.not$.

Правило як окремий рядок: $arrow.r.double$ не плутати з $arrow.r.double.long$.
