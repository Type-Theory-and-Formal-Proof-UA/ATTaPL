// Пробний файл: перевіряє преамбулу, середовища тверджень і кирилицю.
#import "/templates/preamble.typ": *

#chap("1", "Substructural Type Systems")[David Walker]

\#\# TODO: переклад

#sec("1.1", "Структурні властивості")

Розглянемо систему типів з контекстом #$Gamma$. Кажуть, що #emph{обмін}
дозволяє переставляти припущення. Апостроф: об’єкт, зв’язування, підстановка.

#lem[Якщо $Gamma_1, x_1 : T_1, x_2 : T_2, Gamma_2 tack t : T$, то
  $Gamma_1, x_2 : T_2, x_1 : T_1, Gamma_2 tack t : T$.]

#defn[Тип $T$ є #emph{лінійним}, якщо кожна змінна використовується рівно раз.]

#exr(diff: "«", rec: true, sol: true)[Доведіть лему про обмін.]

#rules[
  #rule(
    $Gamma tack t_1 : T_11 -> T_12 quad Gamma tack t_2 : T_11$,
    "T-App",
    $Gamma tack t_1 t_2 : T_12$,
  )
]

#figure([Figure 1-3: Linear lambda calculus: Syntax], rules[
  #set align(left)
  pretypes: $P ::= "Bool" mid T times T mid T -> T$
  #linebreak()
  types: $T ::= q P$
])

#subsec("Синтаксис")
Текст підрозділу з формулами: $forall x in D, exists y eq.not z$, $A subset.eq B$,
$arrow.r.double$, $prec.eq$, $diamond$, $star$, $parallel$, $bot$, $top$,
$emptyset$, $chevron.l x , y chevron.r$, $ell$, $partial$.
Літеральні символи: $⊗$, $⪯$, $⋄$, $⋆$, $∥$, $▶$ і $▷$.

#remark[Зауваження з посиланням на розділ 1.2.]
