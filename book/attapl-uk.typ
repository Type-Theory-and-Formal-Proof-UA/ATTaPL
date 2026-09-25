// Згенеровано scripts/50_assemble.py — не редагувати вручну.
// Усі перекладені розділи в одному документі.
#import "/templates/html.typ": html-support
#show: html-support
#import "/templates/parts.typ": partpage
#include "/templates/frontmatter.typ"
#include "/book/preface.typ"
#partpage("I", [Точний аналіз типів])
#include "/book/ch01.typ"
#include "/book/ch02.typ"
#include "/book/ch03.typ"
#partpage("II", [Типи для низькорівневих мов])
#include "/book/ch04.typ"
#include "/book/ch05.typ"
#partpage("III", [Типи та міркування про програми])
#include "/book/ch06.typ"
#include "/book/ch07.typ"
#partpage("IV", [Типи для програмування «в великому»])
#include "/book/ch08.typ"
#include "/book/ch09.typ"
#partpage("V", [Виведення типів])
#include "/book/ch10.typ"
#include "/book/appa.typ"
#include "/book/refs.typ"
#include "/book/index.typ"
