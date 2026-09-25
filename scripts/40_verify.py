#!/usr/bin/env python3
"""Verify one translated part against its own source slice.

Checks, all mechanical:
  1. statement counts PER KIND (source English label vs the target macro used)
  2. leftover TODO markers
  3. the arrow trap: arrow.r.double.long / arrow.r.long.double print ⟹, not the
     ⇒ the book uses — count them against arrow.r.double
  4. apostrophe code point: Ukrainian prose must use U+2019, not U+02BC or '
  5. Cyrillic left inside math mode without quotes (Typst rejects it, but a
     child may have "fixed" it by quoting English text)
  6. figures: caption count in source vs #figure in the translation
Usage: python3 scripts/40_verify.py [part ...]
"""
import re, sys, pathlib, json

ROOT = pathlib.Path(__file__).resolve().parent.parent

KINDS = {
    "Theorem": "thm", "Lemma": "lem", "Corollary": "cor", "Definition": "defn",
    "Proposition": "prop_", "Claim": "claim", "Notation": "notation",
    "Convention": "convention", "Fact": "fact", "Axiom": "axiom",
    "Example": "example", "Remark": "remark", "Exercise": "exr",
}
SYM_TRAPS = ["arrow.r.double.long", "arrow.r.long.double"]


def verify(part):
    src_p = ROOT / "out" / part / "source.txt"
    uk_p = ROOT / "out" / part / "uk.typ"
    if not uk_p.exists():
        return {"part": part, "status": "MISSING", "problems": ["no uk.typ on disk"],
                "notes": [], "counts": {}, "figures": ("-", "-"), "words": 0}
    src = src_p.read_text(encoding="utf-8")
    uk = uk_p.read_text(encoding="utf-8")
    problems, notes = [], []

    # 1. per-kind statement counts. The source may mention a kind in prose and in
    #    cross-references, so compare the *headline* form ("Lemma:" / "Exercise [").
    counts = {}
    for en, macro in KINDS.items():
        s = len(re.findall(rf"\b{en}\b(?:\s*\[[^\]]*\])?\s*(?:\(|:)", src))
        t = len(re.findall(rf"#\w+\(", uk)) if False else len(re.findall(rf"#{re.escape(macro)}\b", uk))
        counts[en] = (s, t)
        if s != t:
            notes.append(f"{en}: source≈{s} translated={t}")

    # 2. TODO markers
    todos = len(re.findall(r"\bTODO\b", uk))
    if todos:
        problems.append(f"{todos} TODO marker(s) left")

    # 3. arrow trap
    bad = sum(uk.count(s) for s in SYM_TRAPS)
    if bad:
        problems.append(f"{bad} x ⟹-spelling (arrow.r.double.long / arrow.r.long.double)")

    # 4. apostrophes
    # The word pattern requires a CYRILLIC letter on at least one side: a straight
    # apostrophe is a defect only inside Ukrainian text.  Non-Cyrillic names
    # legitimately keep it ("O'Keefe", the OCaml prime "tm1'", the rule "hmx-Inst'").
    n2019, n02bc = uk.count("\u2019"), uk.count("\u02bc")
    nstraight = len(re.findall(r"[А-Яа-яЇїІіЄєҐґ][\w\u2019\u02bc']*'[\w\u2019\u02bc']*|[A-Za-zА-Яа-яїієґ']*'[А-Яа-яЇїІіЄєҐґ]", uk))
    if n02bc:
        problems.append(f"{n02bc} x U+02BC apostrophe (must be U+2019)")
    if nstraight:
        problems.append(f"{nstraight} x straight ' inside a Ukrainian word")

    # 5. unquoted Cyrillic in math
    for m in re.finditer(r"\$[^$]*\$", uk):
        body = m.group(0)
        if re.search(r"[А-Яа-яЇїІіЄєҐґ]", body) and '"' not in body:
            notes.append(f"Cyrillic in math without quotes: {body[:60]!r}")
            break

    # 6. figures
    fsrc = len(re.findall(r"<<<FIGURE-BODY: \[((?:Figure|Table)[^\]]*)\]>>>", src))
    fuk = len(re.findall(r"#figure\(", uk))

    return {"part": part, "status": "ok" if not problems else "PROBLEMS",
            "problems": problems, "notes": notes, "counts": counts,
            "figures": (fsrc, fuk), "words": len(re.findall(r"\S+", uk))}


if __name__ == "__main__":
    parts = sys.argv[1:] or [p.name for p in sorted((ROOT / "out").iterdir()) if p.is_dir()]
    rows = [verify(p) for p in parts]
    for r in rows:
        print("=" * 72)
        print(f"{r['part']:9s} {r['status']:9s} words={r.get('words', 0):6d} "
              f"figures src={r.get('figures', ('-', '-'))[0]} uk={r.get('figures', ('-', '-'))[1]}")
        for p in r["problems"]:
            print("   PROBLEM:", p)
        mism = [f"{k}:{v[0]}/{v[1]}" for k, v in r.get("counts", {}).items() if v[0] != v[1]]
        if mism:
            print("   kind-count source/translated:", ", ".join(mism))
        for n in r["notes"][:6]:
            print("   note:", n)
    json.dump(rows, open(ROOT / "verify.json", "w"), ensure_ascii=False, indent=1)
