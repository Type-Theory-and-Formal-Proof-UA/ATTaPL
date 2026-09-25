# Глосарій (ATTaPL → українська)

Єдине джерело істини для термінів. Діти-перекладачі читають його, але **не редагують** —
нові терміни вони повертають батьківському агентові у своєму звіті (поле `new_terms`).

Правило: один термін — один відповідник по всій книзі. Якщо терміна немає тут, беріть
найуживаніший український відповідник і **повідомте його**, а не вигадуйте варіант.

## Загальні поняття
| English | Українською |
|---|---|
| type system | система типів |
| typing (n.) | типізація |
| type checking / to typecheck | перевірка типів / перевіряти типи |
| type inference / reconstruction | виведення типів |
| well-typed | коректно типізований |
| term | терм |
| expression | вираз |
| value | значення |
| variable | змінна |
| binding | зв’язування |
| bound variable / free variable | зв’язана змінна / вільна змінна |
| substitution | підстановка |
| context | контекст |
| judgment | судження |
| derivation | виведення (derivation tree — дерево виведення) |
| inference rule | правило виведення |
| premise / conclusion | посилка / висновок |
| side condition | побічна умова |
| soundness / sound | коректність / коректний |
| completeness / complete | повнота / повний |
| preservation | збереження (типу) |
| progress | поступ |
| type safety | безпечність типів |
| semantics | семантика |
| operational semantics | операційна семантика |
| evaluation | обчислення |
| reduction | зведення (reduction step — крок зведення) |
| normal form | нормальна форма |
| stuck | застрягає (про стан обчислення) |
| small-step / big-step | дрібнокрокова / великокрокова |
| congruence | конгруентність |
| lemma | лема |
| theorem | теорема |
| corollary | наслідок |
| proposition | твердження |
| definition | означення |
| remark | зауваження |
| example | приклад |
| exercise | вправа |
| proof | доведення |
| induction | індукція |
| by induction on | індукцією за |
| case | випадок |
| hypothesis (IH) | гіпотеза (індукційна гіпотеза) |
| arbitrary | довільний |
| canonical form | канонічна форма |
| abstraction | абстракція |
| application | застосування |
| annotation | анотація |
| constructor | конструктор |
| projection | проєкція |
| pattern matching | зіставлення зі зразком |
| record | запис |
| tuple | кортеж |
| pair | пара |
| label | мітка |
| field | поле |
| recursive | рекурсивний |
| polymorphic / polymorphism | поліморфний / поліморфізм |
| universal / existential | універсальний / екзистенційний |
| monomorphic | моноформний |
| higher-order | вищого порядку |
| first-class / second-class | повноправний / неповноправний |
| syntax / syntactic | синтаксис / синтаксичний |
| free / bound occurrences | вільні / зв’язані входження |
| capture-avoiding | без захоплення (підстановка без захоплення змінних) |
| alpha-conversion | альфа-перетворення |
| alpha-equivalence | альфа-еквівалентність |
| eta | ета |

## Розділ 1 — субструктурні системи
| English | Українською |
|---|---|
| substructural type system | субструктурна система типів |
| structural property | структурна властивість |
| exchange | обмін |
| weakening | послаблення |
| contraction | скорочення |
| linear / linearity | лінійний / лінійність |
| affine | афінний |
| relevant | релевантний |
| ordered | упорядкований |
| unrestricted | необмежений |
| qualifier | кваліфікатор |
| pretype | прототип |
| context split | розщеплення контексту |
| alias | псевдонім |
| dangling reference | висяче посилання |
| reference counting | підрахунок посилань |
| garbage collection | збирання сміття |
| to deallocate | звільняти (пам’ять) |
| thunk | thunk (затримане обчислення) |
| resource | ресурс |
| lock | блокування |
| deadlock | взаємне блокування |
| state change | зміна стану |

## Розділ 2 — залежні типи
| English | Українською |
|---|---|
| dependent type(s) | залежні типи |
| index / indexed | індекс / індексований |
| family (of types) | сімейство (типів) |
| kind | рід (kind) |
| sort | сорт (sort) |
| type-valued function | функція зі значеннями-типами |
| Curry–Howard correspondence | відповідність Каррі–Говарда |
| proposition-as-types | «твердження як типи» |
| logical framework | логічна система (framework — фреймворк) |
| proof object / proof term | об’єкт доведення / терм доведення |
| normalization | нормалізація |
| strong normalization | сильна нормалізація |
| confluence | конфлюентність (не «збіжність»!) |
| subject reduction | збереження суб’єкта |
| erasure | стирання |
| definitional equality | дефініційна рівність |
| conversion rule | правило перетворення |
| pure type system | чиста система типів |
| calculus of constructions | числення конструкцій |
| canonical (form) | канонічний |
| algorithm / algorithmic | алгоритм / алгоритмічний |
| decidability / decidable | розв’язність / розв’язний |
| termination / terminating | завершуваність / той, що завершується |
| totality / total | тотальність / тотальний |
| vector | вектор |
| format string | рядок формату |
| quantified | квантифікований |
| telescope | телескоп |

## Розділ 3 — ефекти та регіони
| English | Українською |
|---|---|
| effect | ефект |
| effect variable | змінна ефектів |
| region | регіон |
| region variable | змінна регіонів |
| region inference | виведення регіонів |
| store | сховище |
| heap | купа |
| allocation / to allocate | виділення / виділяти |
| deallocation | звільнення |
| place | позиція (place) |
| value flow | потік значень |
| label | мітка |
| type-and-effect system | система типів та ефектів |
| let-polymorphism | let-поліморфізм |
| letregion | letregion |
| effect polymorphism | поліморфізм за ефектами |
| escape (of a region) | витікання (регіону) |
| store effect | ефект сховища |
| imperative | імперативний |
| monad / monadic | монада / монадний |
| inference algorithm | алгоритм виведення |
| constraint | обмеження |
| unification | уніфікація |
| stack / frame | стек / кадр |
| lifetime | час життя |
| liveness | живучість (liveness) |
| destructive update | деструктивне оновлення |
| tail call | хвостовий виклик |

## Розділ 4 — типізований асемблер
| English | Українською |
|---|---|
| typed assembly language (TAL) | типізована мова асемблера (TAL) |
| assembly (code) | асемблер (код асемблера) |
| instruction | інструкція |
| operand | операнд |
| register | регістр |
| word | слово (пам’яті) |
| to fetch | вибирати (інструкцію) |
| to jump | переходити |
| code pointer | вказівник на код |
| data pointer | вказівник на дані |
| shared / unique | спільний / унікальний |
| heap | купа |
| stack | стек |
| tuple | кортеж |
| allocation type | тип розміщення |
| control-flow safety | безпечність потоку керування |
| memory safety | безпечність пам’яті |
| compiler | компілятор |
| type-preserving compilation | компіляція зі збереженням типів |
| intermediate language | проміжна мова |
| target language | цільова мова |
| source language | вихідна мова |
| callee-save / caller-save | зберігає викликаний / зберігає той, хто викликає |
| calling convention | угода про виклики |
| primitive | примітив |
| stuck | застрягає |
| stack frame | кадр стека |
| closure | замикання |
| to inline / inlining | вбудовувати / вбудовування |
| tag / untag | тег / знімати тег |
| garbage collector | збирач сміття |

## Розділ 5 — код, що несе доведення
| English | Українською |
|---|---|
| proof-carrying code (PCC) | код, що несе доведення |
| safety policy | політика безпечності |
| verification condition (VC) | умова перевірки |
| verification-condition generator | генератор умов перевірки |
| symbolic evaluation / symbolic state | символічне обчислення / символічний стан |
| invariant | інваріант |
| loop invariant | інваріант циклу |
| annotation | анотація |
| assertion / to assert | твердження / стверджувати |
| precondition / postcondition | передумова / післяумова |
| agent | агент (мобільний код) |
| host | хост |
| untrusted code | недовірений код |
| mobile code | мобільний код |
| certificate | сертифікат |
| to check / checker | перевіряти / перевіряч |
| proof rules | правила доведення |
| soundness of the safety policy | коректність політики безпечності |
| Edinburgh Logical Framework (LF) | Единбурзька логічна система (LF) |
| representation | подання |
| adequacy | адекватність |
| encoding | кодування |
| first-order logic | логіка першого порядку |
| predicate | предикат |
| state predicate | предикат стану |
| memory safety | безпечність пам’яті |
| control-flow safety | безпечність потоку керування |
| abstraction (in proof) | абстракція |
| to discharge (a condition) | знімати (умову) |
| compiler | компілятор |
| proof generation | породження доведення |
| trustworthy / untrustworthy | надійний / ненадійний |
| bytecode | байт-код |
| JVML | JVML |
| type annotation | анотація типу |
| well-formed | правильно побудований |

## Розділ 6 — логічні відношення
| English | Українською |
|---|---|
| logical relation | логічне відношення |
| equivalence / equivalent | еквівалентність / еквівалентний |
| behavioral equivalence | поведінкова еквівалентність |
| observational equivalence | спостережна еквівалентність |
| congruence | конгруентність |
| compatible closure | сумісне замикання |
| compatible / compatibility | сумісний / сумісність |
| context | контекст |
| contextual equivalence | контекстна еквівалентність |
| type-directed | керований типами |
| non-type-directed | некерований типами |
| decision procedure | процедура розв’язування |
| to decide | розв’язувати |
| termination of the algorithm | завершуваність алгоритму |
| monotone | монотонний |
| fixed point | нерухома точка |
| fundamental theorem | фундаментальна теорема |
| main lemma | основна лема |
| to extend | продовжувати |
| closed term | замкнений терм |
| observable | спостережуваний |
| to distinguish | розрізняти |
| step index | індекс кроку |
| bisimulation | бісимуляція |
| evaluation function | функція обчислення |

## Службові слова (часті звороти)
| English | Українською |
|---|---|
| let us write / we write | записуємо / позначаємо |
| it follows that | з цього випливає, що |
| as required | що й треба було довести |
| without loss of generality | без втрати загальності |
| suppose / assume | припустімо |
| hence / thus / therefore | отже |
| moreover / furthermore | до того ж |
| however | проте |
| since / because | оскільки |
| in the case | у випадку |
| it suffices to show | достатньо показати |
| the proof proceeds by induction | доведення ведеться індукцією |
| the remaining cases are similar | решта випадків аналогічні |
| as usual | як звичайно |
| note that | зауважимо, що |
| we say that … is | кажемо, що … є |
| is given by | задається |
| is defined as | означається як |
| ranges over | набуває значень з |
| such that | такий, що |
| for all / for every | для всіх / для кожного |
| for some | для деякого |
| there exists | існує |
| respectively | відповідно |
| in particular | зокрема |
| on the one hand / on the other hand | з одного боку / з другого боку |
| at most / at least | щонайбільше / щонайменше |
| exactly once | рівно раз |
| up to | з точністю до |
| holds (of a property) | виконується |
| to hold | виконуватися |
| to correspond to | відповідає |
| straightforward | безпосередній |
| tedious | громіздкий |
| crucial | ключовий |
| to range over | пробігає |

## Додано під час перекладу розділів 1–6 (звіти перекладачів)
| English | Українською |
|---|---|
| algorithmic linear strengthening | алгоритмічне лінійне підсилення |
| admissible (rule) | допустиме (правило) |
| storage-mode analysis | аналіз режимів зберігання |
| letrec / fix | letrec / fix |
| simulated progress | симульований поступ |
| type soundness | безпечність типів |
| path (algorithmic) | шлях |
| weak head normalization | слабка головна нормалізація |
| weak head reduction | слабке головне зведення |
| definitional equivalence | дефініційна еквівалентність |
| logical relation | логічне відношення |
| Kripke logical relation | логічне відношення Кріпке |
| fundamental theorem | фундаментальна теорема |
| main lemma | основна лема |
| monotonicity / antitonicity | монотонність / антитонність |
| completeness (of an algorithm) | повнота |
| termination (of the algorithm) | завершуваність |
| identity substitution | тотожна підстановка |
| equivalence algorithm | алгоритм еквівалентності |
| symbolic evaluator | символічний обчислювач |
| verification condition | умова перевірки |
| safety policy | політика безпечності |
| agent (mobile code) | агент |
| array type constructor | конструктор типу масиву |
| stack-allocated ordered function | упорядкована функція, розміщена в стеку |
| effect-typed language (ETL) | мова з ефект-типізацією (ETL) |
| RAL / TT / RTL | RAL / TT / RTL |
| region inference | виведення регіонів |
| store (semantics) | сховище |
| ordered type system | упорядкована система типів |
| value restriction | обмеження на значення |
| Pi type (Pi types) | Pi-типи — друкуються латиницею «Pi», як у книзі (вказівник на «залежні типи») |
| phantom type | фантомний тип |
| singleton kind / singleton type | одиничний рід / одиничний тип |
| uniqueness type | тип унікальності |
| phase distinction | фазова відмінність |
| polymorphic variant | поліморфний варіант |
| sealing | запечатування |
| dot notation (signatures) | точкова нотація |
