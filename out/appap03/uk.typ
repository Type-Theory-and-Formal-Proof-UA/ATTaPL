// ============================================================================
// Додаток A «Розв’язки вибраних вправ», частина 3 (глави 8–10)
// ============================================================================
#import "/templates/preamble.typ": *

#soln("8.2.1")[Станом на час написання питання про те, як далеко можна просунути
номінальні модульні системи, цілком відкрите. Нещодавній крок у цьому напрямку зробили
Одерський, Креме, Рокл і Ценгер (Odersky, Cremet, Rockl, and Zenger, 2003).]

#soln("8.5.3")[Означмо $m_1$ як модуль

#raw("module m1 = mod { type X = Int val c = 0 val f = succ }", block: true)

а $m_2$ — як модуль

#raw("module m2 = mod { type X = Bool val c = true val f = not }", block: true)

Означмо $M$ як вираз $"if" "flip"() "then" m_1 "else" m_2$, де функція
$"flip" : "unit" arrow.r "bool"$ чергує $"true"$ і $"false"$ при кожному виклику. Тепер
розгляньмо терм $t = M . f (M . c)$. Він добре типізований, бо $M . f : M . X arrow.r M . X$
і $M . c : M . X$. Але обчислення $t$ йде не так, як треба, бо застосовує або $"succ"$ до
значення типу $"Bool"$, або $"not"$ до значення типу $"Int"$.]

#soln("8.5.4")[У контексті виклику за іменем змінні вже не можна вважати детермінованими,
бо вони позначають необчислені модульні вирази. Тому ми не можемо «детермінізувати»
недетермінований модульний вираз, зв’язавши його зі змінною, і внаслідок цього немає
способу скористатися його типовими компонентами.]

#soln("8.5.5")[Розгляньмо такі оголошення:

#raw("signature I = sig {\n  type X\n  val x : X\n}\n\nmodule m = mod {\n  type X = Int\n  val x = 5\n}\n\nmodule n = mod {\n  type X = Bool\n  val x = true\n}", block: true)

Тоді терм $(lambda x : (m :> I) . X dots)((m :> I) . x)$ добре типізований, а терм
$(lambda x : (n :> I) . X dots)((m :> I) . x)$ — ні.]

#soln("8.5.6")[Наприклад, ми могли б гешувати те саме значення в двох різних геш-таблицях,
отримуючи два геш-коди, які, маючи той самий тип, можна було б порівняти й (несподівано)
виявити, що вони різні. І навпаки, нам могло б не пощастити й ми могли б загешувати два
різні значення в один геш-код.]

#soln("8.5.7")[Розгляньмо сигнатуру

#raw("signature INTDICT = sig {\n  type T\n  val insert : T × Int → T\n  val lookup : T × Int → Bool\n}", block: true)

Якщо $M$ і $N$ обидва реалізують $"INTDICT"$ як список цілих, але $M$ вимагає, щоб список
був відсортований, а $N$ — ні, то обмін $N . "lookup"$ на $M . "lookup"$ міг би призвести до
того, що вставлений ключ не буде знайдено.]

#soln("8.5.9")[Сигнатура

#raw("signature J = sig {\n  type X : *→*\n  type Y : *\n}", block: true)

є надсигнатурою $I$, яка уникає $m$. Для кожного типу $A$ сигнатура

#raw("signature KA = sig {\n  type X : *→*\n  type Y = X(A)\n}", block: true)

також є надсигнатурою $I$, яка уникає $m$. Але сигнатура $J$ — це власна надсигнатура
кожної сигнатури $K A$, тож вона не може бути головною, і при цьому сигнатури $K A$ і
$K B$ непорівнювані, коли $A$ і $B$ — нееквівалентні типи. Приклад у системі $F_(<=)$
див. у Ґеллі та Пірса (Ghelli and Pierce, 1992).]

#soln("8.7.1")[Бо не було б способу отримати примірники цілком абстрактного типу
$("dict"_1 :> "Dict") . X$, а отже, й способу будь-коли покласти щось у словник.]

#soln("8.7.2")[
#align(center)[$"sig" \{C D_1, dots, C D_n\} "is" M = "sig" \{C D_1 "is" M, dots, C D_n "is" M\}$]

#align(center)[$"type" X "is" M = M . X$]

#align(center)[$"type" X "=" T "is" M = "type" X "=" T$]

#align(center)[$"val" x : T "is" M = "val" x : T$]

#align(center)[$"module" m : I "is" M = "module" m : (I "is" M . m)$]]

#soln("8.8.1")[Сигнатура функтора — це сигнатура, що описує функції модульного рівня;
сімейство сигнатур саме є функцією з модулів у сигнатури. Тіло сигнатури функтора — це
сімейство сигнатур, індексоване параметром функтора. Або, кажучи гаслом, яке викарбували
Санелла, Соколовський і Тарлецький (Sannella, Sokolowski, and Tarlecki, 1992): параметризована
(специфікація програми) $eq.not$ (параметризована програма) — специфікація.]

#soln("8.8.2")[Так, але треба подбати, щоб функтор $"dictFun"$ включав свій параметр як
підмодуль свого результату:

#raw("module dictFun = λk:ordered.\n  mod {\n    module key = k\n    ... (as before) ...\n  }\n\nsignature DictFun =\n  Πk:Ordered.\n    sig {\n      module key = k\n      type Dict : *→*\n      val new    : ∀V. Dict V\n      val add    : ∀V. Dict V → key.X → V → Dict V\n      val member : ∀V. Dict V → key.X → Bool\n      val lookup : ∀V. Dict V → key.X → V\n    }", block: true)

Або, стисліше, $"DictFun" = Pi m : K . (D "where" k = m)$.]

#soln("8.8.4")[Функтор $"compose8"$ вимагатиме 9 типових параметрів; $"compose16"$ —
17. Зауважте, що в цій серії прикладів частина кожного функтора, яка робить корисну роботу,
має той самий розмір, що й у попередника, тоді як обсяг «параметризації-завади» зростає
експоненційно.]

#soln("8.8.5")[Нехай $"HashFun"$ — генеративний функтор геш-таблиці. Якби через
підсумовування $"HashFun"$ можна було вважати аплікативним, то два примірники визначали б
той самий абстрактний тип, дозволяючи сплутати різні геш-таблиці.]

#soln("8.10.1")[Модуль у нашому розумінні відповідає файлу «$.c$», який містить означення
процедур і функцій, означення типів і оголошення глобальних змінних. Процедури, функції та
змінні можна зробити приватними, оголосивши їх статичними ($"static"$); інакше вважають, що
їх експортовано. Сигнатура в нашому розумінні відповідає файлу «$.h$», який містить
заголовки процедур і функцій, означення типів і оголошення глобальних змінних.
Скомпільовані версії модулів відповідають файлам «$.o$», які компонують (наприклад, командою
$"ld"$ у Unix) у повні виконувані програми.]

#soln("8.10.2")[Строге порівняння модульних можливостей Java з описаними в цьому розділі
насправді досить складне. Ось, утім, кілька спостережень. Клас у Java — це
середньомасштабний засіб структурування програм, і він часто є одиницею абстракції, що
підтримує цікаві інваріанти між своїми полями й дозволяє доступ до полів лише через власні
методи. У цих відношеннях клас подібний до модуля. Однак класи Java не мають типових
компонентів. І навпаки, примірникування класу (у розумінні сказати $"new"$ класу, щоб
отримати об’єкт) — це те, чого ми не робимо з модулями. Також класи в Java не є одиницями
компіляції: загалом неможливо скомпілювати клас окремо від інших класів, на які він
посилається (наприклад, бо дозволено взаємно рекурсивні посилання). Об’єкт у Java теж
певною мірою подібний до модуля, бо надає набір іменованих компонентів; однак, як і класи,
об’єкти не містять типових компонентів — лише методи (функції) та поля (комірки-посилання,
що тримають вказівники на об’єкти). І сигнатури Java, і абстрактні класи (усі методи яких
віртуальні) певною мірою подібні до сигнатур у розумінні цього розділу, бо вони описують
компоненти об’єкта, не даючи реалізацій. Сигнатури й абстрактні класи можна вживати для
досягнення окремої компіляції в Java, але в дещо іншому стилі, ніж окрема компіляція,
обговорювана тут. Означають сигнатуру $I$, потім означають один клас, який реалізує $I$, і
окремо — інший, який очікує отримати об’єкт, що реалізує $I$. Ці два класи можна
скомпілювати окремо один від одного. Пакети Java також корисні для структурування й
розкладання просторів імен великих програмних систем, але вони не мають багатьох ознак
модулів у нашому розумінні: пакети не є одиницями окремої компіляції, і немає поняття
«сигнатура пакета». Це наводить на думку, що пакети можна було б перетворити на щось
ближче до справжніх модулів, озброївши їх сигнатурами. Це розширення дослідили Бауер, Еппел
і Фелтен (Bauer, Appel, and Felten, 1999).]

#soln("9.1.4")[Засновок $Gamma tack T_2 :: *$ у правилі T-TLet забезпечує, що локальна
змінна $X$ з’являється лише в межах області, де її означено, а не в $T_2$. Якби цю побічну
умову опустити, то дозволялося б не лише
$tack ("let" X = "Nat" "in" lambda y : X . y + 1) : "Nat" arrow.r "Nat"$, а й
$tack ("let" X = "Nat" "in" lambda y : X . y + 1) : X arrow.r "Nat"$. Таким чином, код
на кшталт $("let" X = "Nat" "in" lambda y : X . y + 1) ("let" X = "Nat" times "Nat" "in"
\{5, 4\})$ пройшов би перевірку типів, бо функції можна було б дати тип
$X arrow.r "Nat"$, а аргументові — тип $X$. Однак під час виконання цей код спробував би
інкременувати пару, і тому його слід відкинути.]

#soln("9.1.5")[Якби примітивні означення додали до просто типізованого лямбда-числення, ми,
ймовірно, захотіли б дозволити типовим змінним з’являтися в типах (що вимагає розширення
синтаксису типів) і дозволити означення типів з’являтися в контексті. Однак, на відміну від
$lambda_"let"$, кожна типова змінна мала б означення (і мала б вид $*$, бо мова не має
операторів над типами). Ці означення породжували б чутливе до контексту відношення
еквівалентності типів, що ґрунтується цілком на розкритті означень; тож додати правило
$F_omega$ T-Eq було б доречно. Зважаючи на відсутність операторів над типами, подальшим
розширенням могло б бути дозволити параметризовані означення типів із фіксованою арністю,
тобто дозволити в контексті означення на кшталт $X(Y_1, Y_2) = Y_1 arrow.r Y_2$, а потім
дозволити в типах повністю застосовані вжиття $X$, як-от $X("Nat", "Bool" arrow.r "Bool")$.
Це веде до можливості неправильно побудованих типів із хибною кількістю аргументів
(наприклад, $X$ сам по собі або $X("Nat")$), і тому могло б вимагати судження про
правильну побудову типів.]

#soln("9.1.8")[Це логічне відношення задовольняє ті самі властивості, що й відношення з
розділу 6 (бути монотонним частковим відношенням еквівалентності та бути замкненим щодо
слабкого головного розширення), з тих самих причин.]

#astmt("A.1", "Lemma:", [
Твердження. 1. Якщо $Gamma tack S "is" T :: K$ і $Gamma' supset.eq Gamma$, то
$Gamma' tack S "is" T :: K$. 2. Якщо $Gamma tack S "is" T :: K$, то
$Gamma tack T "is" S :: K$. 3. Якщо $Gamma tack S "is" T :: K$ і
$Gamma tack T "is" U :: K$, то $Gamma tack S "is" U :: K$. 4. Якщо
$Gamma tack S "is" T :: K$ і $Gamma tack▶ S' arrow.r.squiggly^* S$ і
$Gamma tack▶ T' arrow.r.squiggly^* T$, то $Gamma tack S' "is" T' :: K$.

Відповідна версія головної леми також справджується. Уже не правда, що всі шляхи є слабкими
головними нормальними формами, тож ми робимо це явною вимогою в пункті 2:])

#astmt("A.2", "Lemma [Main Lemma]:", [
1. Якщо $Gamma tack S "is" T :: K$, то $Gamma tack▶ S arrow.double.bar T :: K$. 2. Якщо
$Gamma tack▶ S arrow.l.r T :: K$, де $S$ і $T$ — шляхи (змінна, застосована нуль або
більше разів), при $Gamma tack▶ S arrow.b S$ і $Gamma tack▶ T arrow.b T$, то
$Gamma tack S "is" T :: K$.])

#astmt("A.3", "Lemma:", [
1. Якщо $Gamma' tack gamma "is" delta :: Gamma$, то $Gamma' tack delta "is" gamma :: Gamma$.
2. Якщо $Gamma' tack gamma "is" gamma' :: Gamma$ і
$Gamma' tack gamma' "is" gamma'' :: Gamma$, то $Gamma' tack gamma "is" gamma'' :: Gamma$.

#proof_[
1. Випливає з леми A.1(2).

2. Припустімо $X :: K in Gamma$. Тоді за лемою A.1(3) $Gamma' tack gamma(X) "is" gamma''(X) :: K$
так само, як і раніше. Або ж припустімо $X :: K = T in Gamma$. Тоді, серед інших наслідків,
ми знаємо, що $Gamma' tack gamma(X) "is" gamma'(X) :: K$,
$Gamma' tack gamma(T) "is" gamma'(X) :: K$,
$Gamma' tack gamma'(X) "is" gamma''(X) :: K$ і
$Gamma' tack gamma'(X) "is" gamma''(T) :: K$. За лемою A.1(2,3), отже, маємо
$Gamma' tack gamma(X) "is" gamma''(X) :: K$,
$Gamma' tack gamma(T) "is" gamma''(X) :: K$ і
$Gamma' tack gamma(X) "is" gamma''(T) :: K$, як вимагалося.
]])

#astmt("A.4", "Theorem [Fundamental Theorem]:", [
1. Якщо $Gamma tack T :: K$ і $Gamma' tack gamma "is" delta :: Gamma$, то
$Gamma' tack gamma(T) "is" delta(T) : K$. 2. Якщо $Gamma tack S equiv T :: K$ і
$Gamma' tack gamma "is" delta :: Gamma$, то $Gamma' tack gamma(S) "is" delta(T) : K$.

#proof_[
Провадимо доведення індукцією за виведеннями. Більшість випадків точно такі самі (з
точністю до переходу від лямбда-числення термів до лямбда-числення типів), як відповідні
доведення в розділі 6. Випадки для нових правил Q-Def і K-Def безпосередньо випливають з
наших припущень для $gamma$ і $delta$. Випадки для K-All і Q-All подібні один до одного; ми
накидаємо лише перший.

Випадок Q-All: $Gamma tack forall X :: K_1 . T_2 :: *$, бо $Gamma, X :: K_1 tack T_2 :: *$.
За головною лемою маємо
$Gamma', X :: K_1 tack gamma[X, X] "is" delta[X, X] : Gamma, X :: K_1$. За індукційною
гіпотезою маємо
$Gamma', X :: K_1 tack (gamma[X, X]) T_2 "is" (delta[X, X]) T_2 : *$. За головною лемою
$Gamma', X :: K_1 tack (gamma[X, X]) T_2 arrow.double.bar (delta[X, X]) T_2 : *$. Таким
чином, $Gamma' tack gamma(forall X :: K_1 . T_2) arrow.l.r delta(forall X :: K_1 . T_2) : *$.
Універсально кванторно зв’язані типи є слабкими головними нормальними формами, тож, востаннє
застосовуючи головну лему,
$Gamma' tack gamma(forall X :: K_1 . T_2) "is" delta(forall X :: K_1 . T_2) : *$.
]])

#astmt("A.5", "Lemma:", [
Нехай $gamma$ — тотожна підстановка. Якщо $Gamma tack diamond$, то
$Gamma tack gamma "is" gamma :: Gamma$.

#proof_[
Індукцією за доведенням $Gamma tack diamond$.

Випадок CTX-Type: $Gamma = Gamma', x : T$, при $Gamma' tack diamond$. За індукційною
гіпотезою.

Випадок CTX-Kind: $Gamma = Gamma', X :: K$, при $Gamma' tack diamond$. За індукційною
гіпотезою маємо $Gamma' tack gamma "is" gamma :: Gamma'$. За монотонністю
$Gamma tack gamma "is" gamma :: Gamma'$. Нарешті, за головною лемою маємо
$Gamma tack X "is" X :: K$, тож $Gamma tack gamma "is" gamma :: Gamma$.

Випадок CTX-Def: $Gamma = Gamma', X :: K = T$, при $Gamma' tack T :: K$. За індукційною
гіпотезою й монотонністю ми знову маємо $Gamma tack gamma "is" gamma :: Gamma'$. За
фундаментальною теоремою $Gamma tack T "is" T :: K$. Тоді за слабким головним розширенням
$Gamma tack X "is" T :: K$, $Gamma tack T "is" X :: K$ і $Gamma tack X "is" X :: K$.
Отже, $Gamma tack gamma "is" gamma :: Gamma$.
]])

#astmt("A.6", "Corollary [Completeness]:", [
Якщо $Gamma tack S :: K$, $Gamma tack T :: K$ і $Gamma tack S equiv T :: K$, то
$Gamma tack▶ S arrow.double.bar T :: K$.

#proof_[
Застосуйте фундаментальну теорему до тотожної підстановки.
]])

#astmt("A.7", "Corollary [Termination]:", [
Якщо $Gamma tack S :: K$ і $Gamma tack T :: K$, то $Gamma tack▶ S arrow.double.bar T :: K$
є розв’язним (тобто детермінований пошук доведення завжди мусить завершитися успіхом або
невдачею).

#proof_[
За повнотою ми знаємо, що $Gamma tack▶ S arrow.double.bar S :: K$ і
$Gamma tack▶ T arrow.double.bar T :: K$. Ми можемо показати індукцією за першим алгоритмом,
що порівняння $S$ і $T$ мусить завершитися.
]])

#soln("9.1.9")[Як один приклад, еквівалентність

#align(center)[$X :: (* arrow.r * arrow.r *) = (lambda Y :: (* arrow.r *) . Y "Nat") tack X (lambda Z :: * . Z) equiv X (lambda Z :: * . "Nat")$]

є довідною, бо обидві сторони довідно еквівалентні $"Nat"$. Однак за того самого означення
для $X$ маємо $X (lambda Z :: * . "Nat") ≢ X (lambda Z :: * . "Bool")$. Пфеннінґ і
Шюрман (Pfenning and Schürmann, 1998) дають синтаксичний критерій для виявлення сукупності
ін’єктивних операторів над типами, які дають еквівалентні результати лише при еквівалентних
аргументах, і тому з ними можна поводитися особливо в реалізації.]

#soln("9.2.1")[Еквівалентний найточніший інтерфейс був би

#align(center)[$Pi m : (Sigma m' : ( * ) . ( !m' )) . (Sigma m'' : ( * = !m . 1 times !m . 1 ) . ( !m . 1 times !m . 1 ))$]

який є підінтерфейсом нескінченно багатьох інтерфейсів, зокрема
$Pi m : (Sigma m' : ( * ) . ( !m' )) . (Sigma m'' : ( * ) . ( !m'' ))$ і
$Pi m : (Sigma m' : ( * = "Nat" ) . ( "Nat" )) . (Sigma m'' : ( * = "Nat" times "Nat" ) . ( "Nat" times "Nat" ))$.]

#soln("9.2.2")[Якби $"Nat" <: "Top"$, то ми могли б дозволити $( "Nat" ) <: ( "Top" )$ за
аналогією з підтипуванням за глибиною для записів. І навпаки, інтерфейси $( * = "Nat" )$ і
$( * = "Top" )$ мусять бути незв’язаними, бо модуль, що містить тип $"Nat"$, не є модулем,
що містить тип $"Top"$, і навпаки. Щоб побачити, що йде не так, припустімо
$( * = "Nat" ) <: ( * = "Top" )$ і нехай $M$ — модуль $( "Nat" )$. Тоді $M : ( * = "Nat" )$,
що за підсумовуванням далі дало б $M : ( * = "Top" )$. У цій точці ми могли б тоді показати,
що $!M equiv "Nat"$ і $!M equiv "Top"$, а отже, що $"Nat" equiv "Top"$.]

#soln("9.3.1")[Якщо $"Nat" <: "Top"$, то ми мали б очікувати, що $S("Nat")$ і $S("Top")$ —
види, незв’язані в ієрархії підвидів. Усі типи виду $S("Nat")$ довідно еквівалентні
$"Nat"$, і тому не повинні бути довідно еквівалентними $"Top"$. Див. також вправу A.]

#soln("9.3.7")[Ми знову провадимо доведення індукцією за розміром $K$. Припустімо
$Gamma tack S :: S(T :: K)$ і $Gamma tack T :: K$.

Випадок: $K = *$, тож $S(T :: K) = S(T)$. Тоді за правилом Q-SElim
$Gamma tack S equiv T :: S(T)$, а за SK-Forget $Gamma tack S(T) <: *$, тож за правилом
Q-Sub $Gamma tack S equiv T :: *$.

Випадок: $K = S(U)$, тож $S(T :: K) = S(T)$. За правилом Q-SElim маємо
$Gamma tack S equiv T :: S(S)$. За пропозицією 9.3.4(5), інверсією K-Sing і SK-Forget маємо
$Gamma tack S(S) <: *$, тож за Q-Sub $Gamma tack S equiv T :: *$. Оскільки
$Gamma tack T :: S(U)$, подібними аргументами маємо $Gamma tack T equiv U :: *$, а отже
$Gamma tack S equiv U :: *$ і $Gamma tack S(S) <: S(U)$. Тому за Q-Sub маємо
$Gamma tack S equiv T :: S(U)$, як вимагалося.

Випадок: $K = Pi X :: K_1 . K_2$, тож $S(T :: K) = Pi X :: K_1 . S(T X :: K_2)$. За
пропозицією 9.3.4(5) та інверсією маємо $Gamma, X :: K_1 tack diamond$, тож за пропозицією
9.3.2(1) і K-App $Gamma, X :: K_1 tack S X :: S(T X :: K_2)$. З тих самих міркувань маємо
$Gamma, X :: K_1 tack T X :: K_2$. За індукційною гіпотезою
$Gamma, X :: K_1 tack S X equiv T X :: K_2$. Тому за правилом Q-Ext маємо
$Gamma tack S equiv T :: Pi X :: K_1 . K_2$.

Випадок: $K = Sigma X :: K_1 . K_2$, тож
$S(T :: K) = S(pi_1 T :: K_1) times S(pi_2 T :: [X arrow.r pi_1 T] K_2)$. За K-Fst і K-Snd
маємо $Gamma tack pi_1 S :: S(pi_1 T :: K_1)$ і
$Gamma tack pi_2 S :: S(pi_2 T :: [X arrow.r pi_1 T] K_2)$. Знову за K-Fst і K-Snd маємо
$Gamma tack pi_1 T :: K_1$ і $Gamma tack pi_2 T :: [X arrow.r pi_1 T] K_2$, тож за
індукційною гіпотезою маємо $Gamma tack pi_1 S equiv pi_1 T :: K_1$ і
$Gamma tack pi_1 S equiv pi_2 T :: [X arrow.r pi_1 T] K_2$. Тому за правилом Q-Pair-Ext
маємо $Gamma tack S equiv T :: Sigma X :: K_1 . K_2$, як бажано.

За означеннями на рисунку 9-9 можливо, щоб $S(T :: K)$ був правильно побудованим видом
навіть тоді, коли $T$ не задовольняє вид $K$; наприклад, візьмімо $T = "Nat"$ і
$K = S("Nat" arrow.r "Nat")$. Тоді маємо
$Gamma tack "Nat" :: S("Nat" :: S("Nat" arrow.r "Nat"))$, але не
$Gamma tack "Nat" equiv "Nat" :: S("Nat" arrow.r "Nat")$.]

#soln("9.3.8")[Користуючись властивостями факту 9.3.6, ми можемо показати допустимість
Q-Beta-Fst.

#rules([
  $Gamma tack T_1 :: K_1$ $quad quad$ $Gamma tack T_1 :: S(T_1 :: K_1)$ $quad quad$ $Gamma tack T_2 :: S(T_1 :: K_2)$
  #linebreak()
  $Gamma tack \{T_1, T_2\} :: S(T_1 :: K_1) times K_2$
  #linebreak()
  $Gamma tack pi_1 \{T_1, T_2\} :: S(T_1 :: K_1)$
  #linebreak()
  $Gamma tack pi_1 \{T_1, T_2\} equiv T_1 :: K_1$
])

Доведення для Q-Beta-Snd точно аналогічне, а подібна ідея працює й для Q-AppAbs:

#rules([
  $Gamma, X :: K_"11" tack T_"12" :: K_"12"$ $quad quad$ $Gamma, X :: K_"11" tack T_"12" :: S(T_"12" :: K_"12")$
  #linebreak()
  $Gamma tack (lambda X :: K_"11" . T_"12") :: (Pi X :: K_"11" . S(T_"12" :: K_"12"))$
  #linebreak()
  $Gamma tack T_2 :: K_"12"$
  #linebreak()
  $Gamma tack (lambda X :: K_"11" . T_"12") T_2 :: S([X arrow.r T_2] T_"12" :: [X arrow.r T_2] K_"12")$
  #linebreak()
  $Gamma tack (lambda X :: K_"11" . T_"12") T_2 equiv [X arrow.r T_2] T_"12" :: [X arrow.r T_2] K_"12"$
])]

#soln("9.3.9")[Нехай $Gamma_1 = Y :: (S("Nat") arrow.r *) arrow.r *$. Тоді

#align(center)[$Y :: (S("Nat") arrow.r *) arrow.r * tack▶ Y (lambda X :: * . X) arrow.double.bar Y (lambda X :: * . "Nat") :: *$]

бо

#numbered("1.")[$Gamma_1 tack▶ Y (lambda X :: * . X) arrow.b Y (lambda X :: * . X)$][
  $Gamma_1 tack▶ Y (lambda X :: * . "Nat") arrow.b Y (lambda X :: * . "Nat")$][
  $Gamma_1 tack▶ Y (lambda X :: * . X) arrow.l.r Y (lambda X :: * . X) arrow.t^*$, бо
  $Gamma_1 tack▶ Y arrow.l.r Y arrow.t^((S("Nat") arrow.r *) arrow.r *)$, і
  #list(
    [$Gamma_1 tack▶ lambda X :: * . X arrow.double.bar lambda X :: * . "Nat" : S("Nat") arrow.r *$, бо
     #list(
       [$Gamma_1, Z :: S("Nat") tack▶ (lambda X :: * . X) Z arrow.double.bar (lambda X :: * . "Nat") Z :: *$, бо
        #list(
          [$Gamma_1, Z :: S("Nat") tack▶ (lambda X :: * . X) Z arrow.b "Nat"$,
           $Gamma_1, Z :: S("Nat") tack▶ (lambda X :: * . "Nat") Z arrow.b "Nat"$,
           $Gamma_1, Z :: S("Nat") tack▶ "Nat" arrow.l.r "Nat" arrow.t^*$.]
        )
       ]
     )
    ]
  )
]

Аналогічне доведення для
$Y :: (* arrow.r *) arrow.r * tack▶ Y (lambda X :: * . X) arrow.double.bar Y (lambda X :: * . "Nat") :: (lambda X :: * . X) Z arrow.double.bar *$
зазнає невдачі, бо воно вимагає довести, що
$Y :: (* arrow.r *) arrow.r *, Z :: * tack▶ (lambda X :: * . "Nat") Z :: *$, а отже, що
$Y :: (* arrow.r *) arrow.r *, Z :: * tack▶ Z arrow.l.r "Nat" arrow.t^*$.]

#soln("9.3.11")[Частина часу компіляції — це

#align(center)[$lambda X_m :: * times K_0 . \{(pi_1 X_m) times (pi_1 X_m), S_0\}$]

а частина часу виконання — це

#align(center)[$lambda X_m :: * times K_0 . lambda x_m : T_0 times (pi_1 X_m) . \{t_0, \{x_m . 2, x_m . 2\}\}$.]

Вони виконують ті самі обчислення, що й інтуїтивні розділення фаз, але беруть трохи
непотрібних аргументів (наприклад, другий аргумент типової пари $X_m$ і перший аргумент
пари $x_m$) та повертають трохи непотрібних результатів ($S_0$ і $t_0$).]

#soln("9.3.14")[
#numbered("1.")[Терми, що містять локальні модулі, можна перекласти як
$|"let" m = M "in" t| := "let" X_m = |M|_c "in" "let" x_m = |M|_r "in" |t|$. Обидві форми
$"let"$ можна виразити як похідні форми в $lambda_S$, або можна було б розширити мову, щоб
зробити їх примітивними.][
Додавання умовного модульного виразу руйнує розрізнення фаз, бо типи в умовному модулі,
наприклад $"if" dots "then" ( "Nat" :: * ) "else" ( "Unit" :: * )$, залежать від значення
перевірки часу виконання.]]

#soln("9.2.3")[Модуль, означений як

#align(center)[$(lambda m : (Sigma m' : ( * ) . ( !m' ))) . ( ( ( lambda X :: * . ( !m . 1 ) :: * arrow.r * ), !m . 2 ) ( ( ( "Nat" :: * ), ( 3 :: "Nat" ) ) :> Sigma m' : ( * ) . ( !m' )))$]

або, користуючись синтаксичним цукром,

#align(center)[$"let" m = ( ( "Nat" :: * ), ( 3 :: "Nat" ) ) :> Sigma m : ( * ) . ( !m ) "in" ( ( lambda X :: * . ( !m . 1 ) :: * arrow.r * ), !m . 2 )$]

задовольняє інтерфейс $Sigma m' : ( * arrow.r * ) . ( ( !m' )("Nat") )$ і, загальніше,
інтерфейс $Sigma m' : ( * arrow.r * ) . ( ( !m' )(T) )$ для будь-якого типу $T$, але не
задовольняє жодного інтерфейсу, який був би підінтерфейсом усіх цих.]

#soln("10.1.22")[У системі типів Дамаса й Мілнера маємо:

#rules([
  $z_1 : X tack z_1 : X$ $quad quad$ $z_1 : X ; z_2 : X tack z_2 : X$
  #linebreak()
  $z_1 : X tack "let" z_2 = z_1 "in" z_2 : X$
  #linebreak()
  $tack lambda z_1 . "let" z_2 = z_1 "in" z_2 : X arrow.r X$
])

Зауважте, що, оскільки $X$ з’являється вільно в середовищі $z_1 : X$, неможливо
нетривіально застосувати dm-Gen до судження $z_1 : X tack z_1 : X$. Тому $z_2$ не може
отримати типову схему $forall X . X$, і весь вираз не може отримати тип $X arrow.r Y$, де
$X$ і $Y$ різні.]

#soln("10.1.23")[Простo довести, що тотожна функція має тип $"int" arrow.r "int"$:

#rules([
  $Gamma_0 ; z : "int" tack z : "int"$
  #linebreak()
  $Gamma_0 tack lambda z . z : "int" arrow.r "int"$
])

Насправді ніщо в цьому виведенні типу не залежить від вибору $"int"$ як типу $z$. Тож ми
з тим самим успіхом можемо взяти натомість типову змінну $X$. Крім того, утворивши
стрілковий тип $X arrow.r X$, ми можемо вжити dm-Gen, щоб універсально кванторно зв’язати
$X$, оскільки $X$ більше не з’являється в середовищі.

#rules([
  $Gamma_0 ; z : X tack z : X$
  #linebreak()
  $Gamma_0 tack lambda z . z : X arrow.r X$ $quad quad$ $X eq.not in "ftv"(Gamma_0)$
  #linebreak()
  $Gamma_0 tack lambda z . z : forall X . X arrow.r X$
])

Варто зауважити, що, хоч виведення типу вживає довільну типову змінну $X$, підсумкове
судження типізації не має вільних типових змінних. Тому воно не залежить від вибору $X$.
Далі ми називаємо наведене вище виведення типу $Delta_0$.

Далі ми доводимо, що функція-наступник має тип $"int" arrow.r "int"$ за початкового
середовища $Gamma_0$. Ми пишемо $Gamma_1$ для $Gamma_0 ; z : "int"$ і робимо вжиття dm-Var
неявними.

#rules([
  $Gamma_1 tack hat(+) : "int" arrow.r "int" arrow.r "int"$ $quad quad$ $Gamma_1 tack z : "int"$
  #linebreak()
  $Gamma_1 tack hat(+) z : "int" arrow.r "int"$ $quad quad$ $Gamma_1 tack hat(1) : "int"$
  #linebreak()
  $Gamma_1 tack z hat(+) hat(1) : "int"$
  #linebreak()
  $Gamma_0 tack lambda z . z hat(+) hat(1) : "int" arrow.r "int"$
])

Далі ми називаємо наведене вище виведення типу $Delta_1$. Тепер ми можемо побудувати
виведення для третього судження типізації. Ми пишемо $Gamma_2$ для
$Gamma_0 ; f : "int" arrow.r "int"$.

#rules([
  $Gamma_2 tack f : "int" arrow.r "int"$ $quad quad$ $Gamma_2 tack hat(2) : "int"$
  #linebreak()
  $Gamma_2 tack f hat(2) : "int"$
  #linebreak()
  $Gamma_0 tack "let" f = lambda z . z hat(+) hat(1) "in" f hat(2) : "int"$
])

Щоб вивести четверте судження типізації, ми повторно вживаємо $Delta_0$, яке доводить, що
тотожна функція має поліморфний тип $forall X . X arrow.r X$. Ми пишемо $Gamma_3$ для
$Gamma_0 ; f : forall X . X arrow.r X$. За dm-Var і dm-Inst маємо водночас
$Gamma_3 tack f : ("int" arrow.r "int") arrow.r ("int" arrow.r "int")$ і
$Gamma_3 tack f : "int" arrow.r "int"$. Таким чином, ми можемо побудувати таке виведення:

#rules([
  $Gamma_3 tack f : ("int" arrow.r "int") arrow.r ("int" arrow.r "int")$ $quad quad$ $Gamma_3 tack f : "int" arrow.r "int"$
  #linebreak()
  $Gamma_3 tack f f : "int" arrow.r "int"$ $quad quad$ $Gamma_3 tack hat(2) : "int"$
  #linebreak()
  $Gamma_3 tack f f hat(2) : "int"$
  #linebreak()
  $Gamma_0 tack "let" f = lambda z . z "in" f f hat(2) : "int"$
])

Перше й третє судження дійсні в просто типізованому лямбда-численні, бо вони не вживають
ані dm-Gen, ані dm-Inst і вживають dm-Let лише щоб увести в середовище мономорфне зв’язування
$f : "int" arrow.r "int"$. Друге судження, звісно, ні: оскільки воно містить нетривіальну
типову схему, воно навіть не є правильно побудованим судженням у просто типізованому
лямбда-численні. Четверте судження є правильно побудованим, але не довідним у просто
типізованому лямбда-численні. Це тому, що $f$ ужито за двох несумісних типів, а саме
$("int" arrow.r "int") arrow.r ("int" arrow.r "int")$ та $"int" arrow.r "int"$, усередині
виразу $f f hat(2)$. Обидва ці типи є примірниками $forall X . X arrow.r X$ — типової схеми,
приписаної $f$ у середовищі $Gamma_3$.

З огляду на правила, виведення $Gamma_0 tack hat(1) : T$ мусить починатися з примірника
dm-Var вигляду $Gamma_0 tack hat(1) : "int"$. За ним може йти довільна кількість примірників
послідовності (dm-Gen; dm-Inst), які перетворюють $"int"$ на типову схему вигляду
$forall macron(X) . "int"$, а потім назад на $"int"$. Отже, $T$ мусить бути $"int"$.
Оскільки $"int"$ не є стрілковим типом, з цього випливає, що застосування $hat(1) hat(2)$ не
може бути добре типізованим за $Gamma_0$. Насправді, оскільки цей вираз застрягає, він не
може бути добре типізованим у жодній несуперечливій системі типів.

Вираз $lambda f . (f f)$ недобре типізований у просто типізованому лямбда-численні, бо
жоден тип $T$ не може збігатися з типом вигляду $T arrow.r T'$: справді, $T$ був би власним
підтермом себе. У DM цей вираз також недобре типізований, але доведення цього факту трохи
складніше. Треба зазначити, що, оскільки $f$ пов’язано лямбдою, йому в середовищі мусить
бути приписано тип $T$ (а не типову схему). Крім того, треба зауважити, що dm-Gen
незастосовне (хіба що тривіально) до судження $Gamma_0 ; f : T tack f : T$, бо всі типові
змінні в типі $T$ з’являються вільно в середовищі $Gamma_0 ; f : T$. Щойно ці пункти
зазначено, доведення таке саме, як у просто типізованому лямбда-численні.

Важливо зауважити, що наведений вище аргумент критично спирається на той факт, що $f$
пов’язано лямбдою і йому мусить бути приписано тип, а не типову схему. Справді, раніше в цій
вправі ми довели, що самозастосування $f f$ добре типізоване, коли $f$ пов’язано через
$"let"$ і йому приписано типову схему $forall X . X arrow.r X$. З тієї самої причини
$lambda f . (f f)$ добре типізоване в неявно типізованому варіанті системи F. Це також
спирається на те, що типи скінченні: справді, $lambda f . (f f)$ добре типізоване в
розширенні просто типізованого лямбда-числення рекурсивними типами, де рівняння
$T = T arrow.r T'$ має розв’язок. Пізніше ми розробимо алгоритм виведення типів для
ML-як-системи-типів і доведемо, що він правильний і повний. Тоді, щоб довести, що терм
недобре типізований, буде досить змоделювати прохід алгоритму й перевірити, що він
повідомляє про невдачу.]

#soln("10.3.2")[Наші гіпотези — $C, Gamma tack t : forall macron(X)[D] . T$ (1) і
$C ⊢ [arrow(X), arrow(T)] D$ (2). Ми також можемо припустити, без втрати загальності,
$macron(X) eq.not "ftv"(C, Gamma, arrow(T))$ (3). За hmx-Inst і (1) маємо
$C and D, Gamma tack t : T$, що за лемою 10.3.1 дає
$C and D and macron(X) = arrow(T), Gamma tack t : T$ (4). Тепер ми твердимо, що
$macron(X) = arrow(T) ⊢ T <= [macron(X), arrow(T)] T$ (5) справджується; доведення
наведено в наступному абзаці. Застосовуючи hmx-Sub до (4) і до (5), отримуємо
$C and D and macron(X) = arrow(T), Gamma tack t : [macron(X), arrow(T)] T$ (6). За C-Eq і
за (2) маємо $C and macron(X) = arrow(T) ⊢ D$, тож (6) можна записати
$C and macron(X) = arrow(T), Gamma tack t : [macron(X), arrow(T)] T$ (7). Нарешті, (3)
тягне $macron(X) eq.not "ftv"(Gamma, [macron(X), arrow(T)] T)$ (8). Застосовуючи правило
hmx-Exists до (7) і (8), отримуємо
$exists macron(X) . (C and macron(X) = arrow(T)), Gamma tack t : [macron(X), arrow(T)] T$
(9). За C-NameEq і за (3) $exists macron(X) . (C and macron(X) = arrow(T))$ еквівалентне
$C$, отже, (9) — це мета $C, Gamma tack t : [macron(X), arrow(T)] T$.

Тепер залишається встановити (5). Один можливий метод доведення — розкрити означення $⊢$ і
міркувати структурною індукцією за $T$. Ось інший, аксіоматичний підхід. Нехай $Z$ — свіже
для $T$, $macron(X)$ і $arrow(T)$. За рефлексивністю підтипування та за C-ExTrans маємо
$"true" equiv T <= T equiv exists Z . (T <= Z and Z <= T)$, що за конгруентністю $equiv$ і за
C-ExAnd тягне
$macron(X) = arrow(T) equiv exists Z . (T <= Z and macron(X) = arrow(T) and Z <= T)$ (10).
Крім того, за C-Eq маємо
$(macron(X) = arrow(T) and Z <= T) equiv (macron(X) = arrow(T) and Z <= [macron(X), arrow(T)] T) ⊢ (Z <= [macron(X), arrow(T)] T)$
(11). Поєднуючи (10) і (11), отримуємо
$macron(X) = arrow(T) ⊢ exists Z . (T <= Z and Z <= [macron(X), arrow(T)] T)$, що за
C-ExTrans можна прочитати як $macron(X) = arrow(T) ⊢ T <= [macron(X), arrow(T)] T$.]

#soln("10.3.3")[Найпростіше можливе виведення $"true", tack lambda z . z : "int" arrow.r "int"$
є синтаксично керованим. Воно близько нагадує виведення Дамаса — Мілнера, наведене у
вправі 10.1.23.

#rules([
  $"true", z : "int" tack z : "int"$
  #linebreak()
  $"true", tack lambda z . z : "int" arrow.r "int"$
])

Як і у вправі 10.1.23, ми можемо взяти типову змінну $X$ натомість типу $"int"$, а потім
ужити hmx-Gen, щоб універсально кванторно зв’язати $X$.

#rules([
  $"true", z : X tack z : X$
  #linebreak()
  $"true", tack lambda z . z : X arrow.r X$ $quad quad$ $X eq.not "ftv"("true", )$
  #linebreak()
  $"true", tack lambda z . z : forall X ["true"] . X arrow.r X$
])

Дійсність цього примірника hmx-Gen спирається на еквівалентність
$"true" and "true" equiv "true"$ і на той факт, що судження ототожнюють з точністю до
еквівалентності їхніх припущень-обмежень. Якщо тепер ми хочемо примірникувати $X$ через
$"int"$, ми можемо вжити hmx-Inst′ так:

#rules([
  $"true", tack lambda z . z : forall X ["true"] . X arrow.r X$ $quad quad$ $"true" ⊢ [X, "int"] "true"$
  #linebreak()
  $"true", tack lambda z . z : "int" arrow.r "int"$
])

Строго кажучи, це не виведення в HM(X), бо hmx-Inst′ не належить до правил рисунка 10-7.
Однак, оскільки доведення леми 10.3.1 і розв’язок вправи 10.3.2 є конструктивними, можна
показати виведення в HM(X), що лежить в його основі. Ми знаходимо:

#rules([
  $Y = "int", z : X tack z : X$
  #linebreak()
  $Y = "int", tack lambda z . z : X arrow.r X$
  #linebreak()
  $Y = "int", tack lambda z . z : forall X . X arrow.r X$
  #linebreak()
  $Y = "int", tack lambda z . z : Y arrow.r Y$ $quad quad$ $Y = "int" ⊢ Y arrow.r Y <= "int" arrow.r "int"$
  #linebreak()
  $Y = "int", tack lambda z . z : "int" arrow.r "int"$
  #linebreak()
  $exists Y . (Y = "int"), tack lambda z . z : "int" arrow.r "int"$
])

Оскільки $exists Y . (Y = "int")$ еквівалентне $"true"$, висновок справді є бажаним
судженням.]

#soln("10.4.1")[Нехай $X eq.not in "ftv"(Gamma)$ (1). Припустімо, що існують задовольнюване
обмеження $C$ і тип $T$ такі, що $C, Gamma tack t : T$ (2) справджується. Завдяки (1) ми
знаходимо, що з точністю до перейменування $C$ і $T$ ми можемо додатково припустити
$X eq.not in "ftv"(C, T)$ (3). Тоді, застосовуючи лему 10.3.1 до (2), отримуємо
$C and T = X, Gamma tack t : T$, що за hmx-Sub дає $C and T = X, Gamma tack t : X$ (4).
Крім того, за (3) і C-NameEq маємо $exists X . (C and T = X) equiv C$. Оскільки $C$
задовольнюване, це тягне, що $C and T = X$ також задовольнюване. Унаслідок цього ми знайшли
задовольнюване обмеження $C'$ таке, що $C', Gamma tack t : X$ справджується.

Тепер припустімо, що $Gamma$ замкнене, а $X$ довільне. Тоді (1) справджується, тож
попередній абзац доводить, що, якщо $t$ добре типізований у межах $Gamma$, то існує
задовольнюване обмеження $C'$ таке, що $C', Gamma tack t : X$ справджується. За
властивістю повноти ми тоді мусимо мати $C' ⊢ ⟦Gamma tack t : X⟧$. Оскільки $C'$
задовольнюване, це тягне, що $⟦Gamma tack t : X⟧$ також задовольнюване. І навпаки, якщо
$⟦Gamma tack t : X⟧$ задовольнюване, то за властивістю несуперечливості $t$ добре
типізований у межах $Gamma$.]

#soln("10.7.1")[Маємо

#align(center)[$"let" Gamma_0 "in" ⟦c t_1 dots t_n : T'⟧ equiv "let" Gamma_0 "in" exists Z_1 dots Z_n . (and.big_(i=1)^n ⟦t_i : Z_i⟧ and c prec.eq Z_1 arrow.r dots arrow.r Z_n arrow.r T')$ (1)]

#align(center)[$equiv "let" Gamma_0 "in" exists Z_1 dots Z_n macron(X) . (and.big_(i=1)^n ⟦t_i : Z_i⟧ and T_1 arrow.r dots arrow.r T_n arrow.r T <= Z_1 arrow.r dots arrow.r Z_n arrow.r T')$ (2)]

#align(center)[$equiv "let" Gamma_0 "in" exists macron(X) . (and.big_(i=1)^n ⟦t_i : T_i⟧ and T <= T')$ (3)]

де (1) — за означенням породження обмежень; (2) — за C-InId; (3) — за C-Arrow, C-ExAnd і
лемою 10.4.6.]

#soln("10.7.2")[Спершу ми мусимо переконатися, що R-Add поважає $⊑$ (означення 10.5.4).
Оскільки правило чисте, досить установити, що
$"let" Gamma_0 "in" ⟦hat(n)_1 hat(+) hat(n)_2 : T⟧$ тягне
$"let" Gamma_0 "in" ⟦macron(n)_1 + macron(n)_2 : T⟧$. Справді, маємо

#align(center)[$"let" Gamma_0 "in" ⟦hat(n)_1 hat(+) hat(n)_2 : T⟧ equiv "let" Gamma_0 "in" (⟦hat(n)_1 : "int"⟧ and ⟦hat(n)_2 : "int"⟧ and "int" <= T)$ (1)]

#align(center)[$equiv "let" Gamma_0 "in" ("int" <= "int" and "int" <= "int" and "int" <= T)$ (2)]

#align(center)[$equiv "int" <= T$ (3)]

#align(center)[$equiv "let" Gamma_0 "in" ⟦macron(n)_1 + macron(n)_2 : T⟧$ (4)]

де (1) і (2) — за вправою 10.7.1; (3) — за C-In\* і за рефлексивністю підтипування;
(4) — знову за вправою 10.7.1.

По-друге, ми мусимо перевірити, що якщо конфігурація $c v_1 dots v_k slash mu$ (де
$k >= 0$) добре типізована, то вона або редукована, або $c v_1 dots v_k$ — значення. Ми
починаємо з перевірки, що кожне значення, добре типізоване з типом $"int"$, має вигляд
$hat(n)$. Справді, припустімо, що $"let" Gamma_0 ; "ref" M "in" ⟦v : "int"⟧$
задовольнюване. Тоді $v$ не може бути програмною змінною, бо добре типізоване значення
мусить бути замкненим. $v$ не може бути коміркою пам’яті $m$, бо інакше
$"ref" M(m) <= "int"$ було б задовольнюваним — але конструктори типів $"ref"$ та $"int"$
несумісні. $v$ не може бути $hat(+)$ чи $hat(+) v'$, бо інакше
$"int" arrow.r "int" arrow.r "int" <= "int"$ або $"int" arrow.r "int" <= "int"$ було б
задовольнюваним — але конструктори типів $arrow.r$ та $"int"$ несумісні. Подібно $v$ не
може бути лямбда-абстракцією. Отже, $v$ мусить мати вигляд $hat(n)$, бо це єдиний
випадок, що лишився.

Далі зауважимо, що, згідно з правилами породження обмежень, якщо конфігурація
$c v_1 dots v_k slash mu$ добре типізована, то задовольнюваним є обмеження вигляду
$"let" Gamma_0 ; "ref" M "in" (c prec.eq X_1 arrow.r dots arrow.r X_k arrow.r T and ⟦v_1 : X_1⟧ and dots and ⟦v_k : X_k⟧)$.
Тепер ми міркуємо за випадками для $c$.

◦ Випадок $c$ — це $hat(n)$. Тоді $Gamma_0(c)$ — це $"int"$. Оскільки конструктори типів
$"int"$ та $arrow.r$ несумісні один з одним, це тягне $k = 0$. Оскільки $hat(n)$ —
конструктор, вираз є значенням.

◦ Випадок $c$ — це $hat(+)$. Ми можемо припустити $k >= 2$, бо інакше вираз є значенням.
Тоді $Gamma_0(c)$ — це $"int" arrow.r "int" arrow.r "int"$, тож за C-Arrow наведене вище
обмеження тягне
$"let" Gamma_0 ; "ref" M "in" (X_1 <= "int" and X_2 <= "int" and ⟦v_1 : X_1⟧ and ⟦v_2 : X_2⟧)$,
що за лемою 10.4.5 тягне
$"let" Gamma_0 ; "ref" M "in" (⟦v_1 : "int"⟧ and ⟦v_2 : "int"⟧)$. Таким чином, $v_1$ і
$v_2$ добре типізовані з типом $"int"$. За наведеним вище зауваженням вони мусять бути
цілочисловими літералами $hat(n)_1$ і $hat(n)_2$. Унаслідок цього конфігурація редукована
за R-Add.]

#soln("10.7.5")[Спершу ми мусимо переконатися, що R-Ref, R-Deref і R-Assign поважають $⊑$
(означення 10.5.4).

◦ Випадок R-Ref. Редукція — це $"ref" v slash mu arrow.r.long m slash (m, v)$, де
$m eq.not in "fpi"(v)$ (1). Нехай $T$ — довільний тип. Згідно з означенням 10.5.4, мета —
показати, що існують множина типових змінних $macron(Y)$ і тип сховища $M'$ такі, що
$macron(Y) eq.not "ftv"(T)$ і $"ftv"(M') subset.eq macron(Y)$ і
$"dom"(M') = \{m\}$ і $"let" Gamma_0 "in" ⟦"ref" v : T⟧$ тягне
$exists macron(Y) . "let" Gamma_0 ; "ref" M' "in" ⟦m slash (m, v) : T slash M'⟧$. Тепер
маємо

#align(center)[$"let" Gamma_0 "in" ⟦"ref" v : T⟧ equiv exists Y . "let" Gamma_0 "in" ("ref" Y <= T and ⟦v : Y⟧)$ (2)]

#align(center)[$equiv exists Y . "let" Gamma_0 ; "ref" M' "in" (m prec.eq T and ⟦v : M'(m)⟧)$ (3)]

#align(center)[$equiv exists Y . "let" Gamma_0 ; "ref" M' "in" ⟦m slash (m, v) : T slash M'⟧$ (4)]

де (2) — за вправою 10.7.1 і за C-InEx; (3) припускає, що $M'$ означено як $m, Y$, і
випливає з (1), C-InId і C-In\*; а (4) — за означенням породження обмежень.

◦ Випадок R-Deref. Редукція — це $!m slash (m, v) arrow.r.long v slash (m, v)$. Нехай $T$ —
довільний тип, а $M$ — тип сховища з областю визначення $\{m\}$. Маємо

#align(center)[$"let" Gamma_0 ; "ref" M "in" ⟦!m slash (m, v) : T slash M⟧ equiv "let" Gamma_0 ; "ref" M "in" exists Y . ("ref" M(m) <= "ref" Y and Y <= T and ⟦v : M(m)⟧)$ (1)]

#align(center)[$equiv "let" Gamma_0 ; "ref" M "in" exists Y . (M(m) = Y and Y <= T and ⟦v : M(m)⟧)$ (2)]

#align(center)[$equiv "let" Gamma_0 ; "ref" M "in" (M(m) <= T and ⟦v : M(m)⟧)$ (3)]

#align(center)[$⊢ "let" Gamma_0 ; "ref" M "in" (⟦v : T⟧ and ⟦v : M(m)⟧)$ (4)]

#align(center)[$equiv "let" Gamma_0 ; "ref" M "in" ⟦v slash (m, v) : T slash M⟧$ (5)]

де (1) — за вправою 10.7.1 і за C-InId; (2) випливає з C-ExTrans і з того, що $"ref"$ є
інваріантним конструктором типів; (3) — за C-NameEq; (4) — за лемою 10.4.5 і C-Dup; а (5) —
знову за означенням породження обмежень.

◦ Випадок R-Assign. Редукція — це $m := v slash (m, v_0) arrow.r.long v slash (m, v)$.
Нехай $T$ — довільний тип, а $M$ — тип сховища з областю визначення $\{m\}$. Маємо

#align(center)[$"let" Gamma_0 ; "ref" M "in" ⟦m := v slash (m, v_0) : T slash M⟧ ⊢ "let" Gamma_0 ; "ref" M "in" ⟦m := v : T⟧$ (1)]

#align(center)[$equiv "let" Gamma_0 ; "ref" M "in" exists Z . ("ref" M(m) <= "ref" Z and ⟦v : Z⟧ and Z <= T)$ (2)]

#align(center)[$equiv "let" Gamma_0 ; "ref" M "in" exists Z . (M(m) = Z and Z <= T and ⟦v : Z⟧)$ (3)]

#align(center)[$equiv "let" Gamma_0 ; "ref" M "in" (M(m) <= T and ⟦v : M(m)⟧)$ (4)]

#align(center)[$⊢ "let" Gamma_0 ; "ref" M "in" ⟦v slash (m, v) : T slash M⟧$ (5)]

де (1) — за означенням породження обмежень; (2) — за вправою 10.7.1 і C-InId;
(3) випливає з того, що $"ref"$ є інваріантним конструктором типів; (4) — за C-NameEq;
а (5) отримано так само, як у попередньому випадку.

По-друге, ми мусимо перевірити, що якщо конфігурація $c v_1 dots v_k slash mu$ (де
$k >= 0$) добре типізована, то вона або редукована, або $c v_1 dots v_k$ — значення. Ми
даємо лише нарис цього доведення; подробиці подібного доведення див. у розв’язку вправи
10.7.2. Ми починаємо з перевірки, що кожне значення, добре типізоване з типом вигляду
$"ref" T$, є коміркою пам’яті. Це твердження спирається на той факт, що конструктор типів
$"ref"$ ізольовано.

Далі зауважимо, що, згідно з правилами породження обмежень, якщо конфігурація
$c v_1 dots v_k slash mu$ добре типізована, то задовольнюваним є обмеження вигляду
$"let" Gamma_0 ; "ref" M "in" (c prec.eq X_1 arrow.r dots arrow.r X_k arrow.r T and ⟦v_1 : X_1⟧ and dots and ⟦v_k : X_k⟧)$.
Тепер ми міркуємо за випадками для $c$.

◦ Випадок $c$ — це $"ref"$. Якщо $k = 0$, то вираз є значенням; інакше він редукований за
R-Ref.

◦ Випадок $c$ — це $!$. Ми можемо припустити $k >= 1$; інакше вираз є значенням. За
означенням $Gamma_0(!)$ наведене вище обмеження тягне
$"let" Gamma_0 ; "ref" M "in" exists Y . ("ref" Y arrow.r Y <= X_1 arrow.r dots arrow.r X_k arrow.r T and ⟦v_1 : X_1⟧)$,
що за C-Arrow, лемою 10.4.5 і C-InEx тягне
$exists Y . "let" Gamma_0 ; "ref" M "in" ⟦v_1 : "ref" Y⟧$. Таким чином, $v_1$ добре
типізований з типом вигляду $"ref" Y$. За наведеним вище зауваженням $v_1$ мусить бути
коміркою пам’яті $m$. Крім того, оскільки кожна добре типізована конфігурація замкнена,
$m$ мусить належати $"dom"(mu)$. Унаслідок цього конфігурація $"ref" v_1 dots v_k slash mu$
редукована за R-Deref.

◦ Випадок $c$ — це $:=$. Ми можемо припустити $k >= 2$, бо інакше вираз є значенням. Як і
вище, ми перевіряємо, що $v_1$ мусить бути коміркою пам’яті й належати $"dom"(mu)$. Таким
чином, конфігурація редукована за R-Assign.]

#soln("10.8.2")[Операція доступу до поля $dot.c chevron.l ell_b chevron.r$ може отримати
типову схему $forall X_b . \{ell_b : X_b\} arrow.r X_b$. Однак ця типова схема
незадовільна, бо вона дозволяє доступ до $ell_b$ лише в записах, де $ell_a$ та $ell_c$
неозначені. Типова схема $forall X_a X_b . \{ell_a : X_a ; ell_b : X_b\} arrow.r X_b$
також є дійсною типовою схемою для $dot.c chevron.l ell_b chevron.r$, але дозволяє доступ
до $ell_b$ лише в записах, де $ell_a$ означене, а $ell_c$ — ні. Підсумовуючи, задовільний
опис $dot.c chevron.l ell_b chevron.r$ вимагає цілої родини типових схем, жодна з яких не
є головною (загальнішою за інші).

Подібна проблема виникає з розширенням запису $chevron.l dot.c "with" ell_b = dot.c chevron.r$.
Потенційний розв’язок — озброїти типи записів відношенням підтипування, так щоб
(скажімо) і $\{ell_a : T_a ; ell_b : T_b\}$, і $\{ell_a : T_a ; ell_b : T_b ; ell_c : T_c\}$
були підтипами $\{ell_b : T_b\}$. Тоді $forall X_b . \{ell_b : X_b\} arrow.r X_b$ стає
задовільною типовою схемою для операції доступу до поля
$dot.c chevron.l ell_b chevron.r$. Справді, операція тепер застосовна до будь-якого запису,
що допускає тип вигляду $\{ell_b : T_b\}$, тобто, завдяки підтипуванню, до будь-якого
запису, де $ell_b$ означене, незалежно від того, які ще поля означено.

Однак це лише половина розв’язку, бо з розширенням запису все ще є проблема. Типова схема
$forall X_b . \{ell_b : X_b\} arrow.r \{ell_b : X_b\}$ дійсна й робить розширення запису
застосовним до будь-якого запису, де $ell_b$ означене, що добре. Біда в її типі
повернення: вона стверджує, що в новому записі безпечно вважати означеним лише $ell_b$.
Іншими словами, вона спричиняє втрату статичної інформації про всі поля, крім $ell_b$.
Подолання цієї драматичної втрати точності — одна з ключових мотивацій для введення рядків.]

#soln("10.8.5")[Ми пропонуємо читачеві перевірити, що $X$ мусить мати вид $star . "Type"$, а
$Y$ мусить мати вид $star . "Row"(\{ell\})$. Тип з усіма явно виписаними верхніми індексами —
це $X arrow.r."Type" Pi (ell^((star, "Row"())) : "int"^"Type" ; (Y arrow.r^("Row"(\{ell\})) upright(partial)^((star, "Row"(\{ell\}))) X))$.
У цьому випадку, оскільки конструктор типів $Pi$ трапляється з правого боку стрілки
верхнього рівня, можна здогадатися, що тип мусить мати вид $star . "Type"$. Є випадки, коли
неможливо здогадатися про вид типу, бо він може мати кілька видів; розгляньмо, наприклад,
$upright(partial) "int"$.]

#soln("10.8.27")[Задля загальності ми провадимо доведення в присутності підтипування,
тобто не припускаємо, що підтипування інтерпретують як рівність. Ми формулюємо деякі
гіпотези про інтерпретацію підтипування: конструктори типів $(ell : dot.c ; dot.c)$,
$upright(partial)$ та $Pi$ мусять бути коваріантними; конструктори типів $arrow.r$ і $Pi$
мусять бути ізольованими.

Ми починаємо з попереднього факту: якщо область визначення $V$ — це
$\{ell_1, dots, ell_n\}$, де $ell_1 < dots < ell_n$, то обмеження
$"let" Gamma_0 "in" ⟦\{V ; v\} : T⟧$ еквівалентне
$"let" Gamma_0 "in" exists Z_1 dots Z_n Z . (and.big_(i=1)^n ⟦V(ell_i) : Z_i⟧ and ⟦v : Z⟧ and Pi (ell_1 : Z_1 ; dots ; ell_n : Z_n ; upright(partial) Z) <= T)$.
Ми пропонуємо читачеві перевірити цей факт, користуючись правилами породження обмежень,
означенням $Gamma_0$ і правилом C-InId, а також наведеними вище гіпотезами коваріантності.
Зауважимо, що за C-Row-LL наведене вище обмеження інваріантне щодо перестановки міток
$ell_1, dots, ell_n$, тож наведений вище факт усе ще справджується, коли гіпотезу
$ell_1 < dots < ell_n$ знято.

Тепер ми доводимо, що правила R-Update, R-Access-1 і R-Access-2 мають властивість
збереження типу за редукцією (означення 10.5.4). Оскільки сховище не задіяне, мета —
встановити, що $"let" Gamma_0 "in" ⟦t : T⟧$ тягне $"let" Gamma_0 "in" ⟦t' : T⟧$, де $t$ —
редекс, а $t'$ — редукт.

◦ Випадок R-Update. Маємо:

#align(center)[$"let" Gamma_0 "in" ⟦\{\{V ; v\} "with" ell = v'\} : T⟧ equiv "let" Gamma_0 "in" exists X X' Y . (⟦\{V ; v\} : Pi (ell : X ; Y)⟧ and ⟦v' : X'⟧ and Pi (ell : X' ; Y) <= T)$ (1)]

#align(center)[$equiv "let" Gamma_0 "in" exists X X' Y Z_1 dots Z_n Z . (and.big_(i=1)^n ⟦V(ell_i) : Z_i⟧ and ⟦v : Z⟧ and Pi (ell_1 : Z_1 ; dots ; ell_n : Z_n ; upright(partial) Z) <= Pi (ell : X ; Y) and ⟦v' : X'⟧ and Pi (ell : X' ; Y) <= T)$ (2)]

де (1) — за вправою 10.7.1, а (2) випливає з попереднього факту та з C-ExAnd, за умови що
$\{ell_1, dots, ell_n\}$ — область визначення $V$. Тепер ми розрізняємо два підвипадки:

Підвипадок $ell in "dom"(V)$. Ми можемо припустити, без втрати загальності, що $ell$ — це
$ell_1$. Тоді за нашими гіпотезами коваріантності підобмеження в другому рядку (2) тягне
$(ell_2 : Z_2 ; dots ; ell_n : Z_n ; upright(partial) Z) <= Y$, що у свою чергу тягне
$Pi (ell_1 : X' ; ell_2 : Z_2 ; dots ; ell_n : Z_n ; upright(partial) Z) <= Pi (ell : X' ; Y)$.
За транзитивністю підтипування підобмеження в другому й третьому рядках (2) тягне
$Pi (ell_1 : X' ; ell_2 : Z_2 ; dots ; ell_n : Z_n ; upright(partial) Z) <= T$. За цим
зауваженням і за C-Ex\*, (2) тягне

#align(center)[$"let" Gamma_0 "in" exists X' Z_2 dots Z_n Z . (⟦v' : X'⟧ and and.big_(i=2)^n ⟦V(ell_i) : Z_i⟧ and ⟦v : Z⟧ and Pi (ell_1 : X' ; ell_2 : Z_2 ; dots ; ell_n : Z_n ; upright(partial) Z) <= T)$ (3)]

що за нашим попереднім фактом є саме $"let" Gamma_0 "in" ⟦\{V[ell, v'] ; v\} : T⟧$.

Підвипадок $ell eq.not in "dom"(V)$. За C-Row-DL і C-Row-LL терм
$(ell_1 : Z_1 ; dots ; ell_n : Z_n ; upright(partial) Z)$ можна замінити на
$(ell : Z ; ell_1 : Z_1 ; dots ; ell_n : Z_n ; upright(partial) Z)$. Таким чином, міркуючи
як у попередньому підвипадку, ми знаходимо, що (2) тягне

#align(center)[$"let" Gamma_0 "in" exists X' Z_1 dots Z_n Z . (⟦v' : X'⟧ and and.big_(i=1)^n ⟦V(ell_i) : Z_i⟧ and ⟦v : Z⟧ and Pi (ell_1 : X' ; ell_1 : Z_1 ; dots ; ell_n : Z_n ; upright(partial) Z) <= T)$ (4)]

що за нашим попереднім фактом є саме $"let" Gamma_0 "in" ⟦\{V[ell, v'] ; v\} : T⟧$.

◦ Випадки R-Access-1, R-Access-2. Маємо:

#align(center)[$"let" Gamma_0 "in" ⟦\{V ; v\} . \{ell\} : T⟧ equiv "let" Gamma_0 "in" exists X Y . (⟦\{V ; v\} : Pi (ell : X ; Y)⟧ and X <= T)$ (1)]

#align(center)[$equiv "let" Gamma_0 "in" exists X Y Z_1 dots Z_n Z . (and.big_(i=1)^n ⟦V(ell_i) : Z_i⟧ and ⟦v : Z⟧ and Pi (ell_1 : Z_1 ; dots ; ell_n : Z_n ; upright(partial) Z) <= Pi (ell : X ; Y) and X <= T)$ (2)]

де (1) — за вправою 10.7.1, а (2) випливає з попереднього факту та з C-ExAnd, за умови що
$\{ell_1, dots, ell_n\}$ — область визначення $V$. Тепер ми розрізняємо два підвипадки:

Підвипадок $ell in "dom"(V)$, тобто (R-Access-1). Ми можемо припустити, без втрати
загальності, що $ell$ — це $ell_1$. Тоді за нашими гіпотезами коваріантності підобмеження
в другому рядку (2) тягне $Z_1 <= X$. За транзитивністю підтипування, за лемою 10.4.5 і за
C-Ex\*, ми знаходимо, що (2) тягне $"let" Gamma_0 "in" ⟦V(ell) : T⟧$.

Підвипадок $ell eq.not in "dom"(V)$, тобто (R-Access-2). За C-Row-DL і C-Row-LL терм
$(ell_1 : Z_1 ; dots ; ell_n : Z_n ; upright(partial) Z)$ можна замінити на
$(ell : Z ; ell_1 : Z_1 ; dots ; ell_n : Z_n ; upright(partial) Z)$. Таким чином, міркуючи
як у попередньому підвипадку, ми знаходимо, що (2) тягне $"let" Gamma_0 "in" ⟦v : T⟧$.

Перш ніж взятися до доведення властивості поступу, коротко перевірмо, що кожне значення
$v$, добре типізоване з типом $Pi T$, мусить бути значенням запису, тобто мати вигляд
$\{V ; w\}$. Справді, припустімо, що $"let" Gamma_0 ; "ref" M "in" ⟦v : Pi T⟧$
задовольнюване. Тоді $v$ не може бути програмною змінною, бо добре типізоване значення
мусить бути замкненим. Крім того, $v$ не може бути коміркою пам’яті $m$, бо
$"ref" M(m) <= Pi T$ незадовольнюване: справді, конструктори типів $"ref"$ і $Pi$
несумісні (нагадаємо, що $Pi$ ізольовано). Подібно $v$ не може бути частково застосованою
константою чи лямбда-абстракцією, бо $T' arrow.r T'' <= Pi T$ незадовольнюване. Отже, $v$
мусить бути повністю застосованим конструктором. Оскільки єдині конструктори в мові — це
конструктори записів $\{\}L$, $v$ мусить бути значенням запису. (Якби в мові були інші
конструктори, їх теж можна було б виключити, за умови що їхні типи повернення несумісні з
$Pi$.)

Тепер ми мусимо довести, що якщо конфігурація $c v_1 dots v_k slash mu$ добре типізована,
то вона або редукована, або $c v_1 dots v_k$ — значення. За гіпотезою доброї типізованості
задовольнюваним є обмеження вигляду
$"let" Gamma_0 ; "ref" M "in" ⟦c v_1 dots v_k : T⟧$.

◦ Випадок $c$ — це $\{\}L$. Якщо $k$ не більше за $n + 1$, де $n$ — потужність $L$, то
$c v_1 dots v_k$ є значенням. Інакше, розкриваючи наведене вище обмеження, ми знаходимо, що
воно не може бути задовольнюваним, бо $Pi$ та $arrow.r$ несумісні; це дає суперечність.

◦ Випадок $c$ — це $\{dot.c "with" ell = dot.c\}$. Аналогічно до наступного випадку.

◦ Випадок $c$ — це $dot.c . \{ell\}$. Якщо $k = 0$, то $c v_1 dots v_k$ є значенням.
Припустімо $k >= 1$. Тоді обмеження $"let" Gamma_0 ; "ref" M "in" ⟦c v_1 : T⟧$ є
задовольнюваним. За вправою 10.7.1 це тягне, що
$"let" Gamma_0 ; "ref" M "in" ⟦v_1 : Pi (ell : X ; Y)⟧$ задовольнюване. Таким чином, $v_1$
мусить бути значенням запису, і конфігурація редукована за R-Access-1 або R-Access-2.]

#soln("10.8.33")[Щоб зробити розширення строгим, досить обмежити його зв’язування в
початковому середовищі $Gamma_0$ так:

#align(center)[$chevron.l dot.c "with" ell = dot.c chevron.r : forall X Y . Pi (ell : "abs" ; Y) arrow.r X arrow.r Pi (ell : "pre" X ; Y)$]

Нове зв’язування, менш загальне за попереднє, вимагає, щоб поле $ell$ було відсутнє у
вхідному записі. Операційну семантику змінювати не потрібно, бо строге розширення збігається
з вільним розширенням, коли воно означене.

Означення операційної семантики (вільного) обмеження ми залишаємо читачеві. Його
зв’язування в початковому середовищі мусить бути таким:

#align(center)[$dot.c without chevron.l ell chevron.r : forall X Y . Pi (ell : X ; Y) arrow.r Pi (ell : "abs" ; Y)$]

У принципі, немає потреби здогадуватися про це зв’язування: його можна виявити через
кодування скінченних записів через повні записи (10.8.32). Строгому обмеженню, яке вимагає,
щоб поле було присутнє у вхідному записі, можна приписати таку типову схему:

#align(center)[$dot.c without chevron.l ell chevron.r : forall X Y . Pi (ell : "pre" X ; Y) arrow.r Pi (ell : "abs" ; Y)$]]

#soln("10.8.34")[Неформальне речення «надати запис із більшою кількістю полів у контексті,
де очікують запис із меншою кількістю полів» можна зрозуміти як «надати аргумент типу
$Pi (ell : "pre" T ; T')$ функції, чий тип області визначення — $Pi (ell : "abs" ; T')$»,
або, загальніше, як «написати програму, чия добра типізованість вимагає, щоб було
задовольнюваним деяке обмеження вигляду $Pi (ell : "pre" T ; T') <= Pi (ell : "abs" ; T')$».

Тепер, у неструктурному порядку підтипування, де $"pre" arrow.r.long "abs"$ справджується,
таке обмеження еквівалентне $"true"$. Навпаки, якщо підтипування інтерпретують як рівність,
то таке обмеження еквівалентне $"false"$. Іншими словами, саме закон
$"pre" T <= "abs" equiv "true"$ породжує підтипування за шириною.

Варто порівняти з тим, як підтипування за шириною означують у системах типів, які не мають
рядків. У таких системах тип запису має вигляд $\{ell_1 : T_1 ; dots ; ell_n : T_n\}$.
Забудьмо про типи $T_1, dots, T_n$, бо вони описують вміст полів, а не їхню присутність, і
тому ортогональні до розглядуваного питання. Тоді тип запису — це множина
$\{ell_1, dots, ell_n\}$, а підтипування за шириною отримують, ототожнюючи підтипування з
(оберненим) включенням множин. У системі типів, яка використовує рядки, з іншого боку, тип
запису — це повне відображення з міток рядків у $"pre"$ або $"abs"$. (Оскільки ми
ігноруємо $T_1, dots, T_n$, уявімо на хвилю, що $"pre"$ — нульарний конструктор типів.)
Тоді наведений вище тип запису записують як
$\{ell_1 : "pre" ; dots ; ell_n : "pre" ; upright(partial) "abs"\}$. Іншими словами,
множину тепер кодують її характеристичною функцією. Підтипування за шириною отримують,
дозволяючи $"pre" arrow.r.long "abs"$ і піднімаючи це впорядкування поточково на рядки (що
відповідає нашій домовленості, що рядки коваріантні).]
