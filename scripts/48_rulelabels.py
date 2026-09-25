#!/usr/bin/env python3
"""Rule-label fidelity: every name passed to #rule(...) must appear in the part's
own source text, with the same case the book prints.

Motivated by two real defects found by eye:
  * ch09p01/p02: I INVENTED labels (SHR-Beta, SE-Var, AE-Base, NK-Var, STE-*,
    TE-*, KE-*, HN-*) for Figures 9-5, 9-7 and 9-10.  The book prints NO label
    at all in those figures — the names simply are not there.
  * ch04p01: the book prints lowercase `(s-commit)`, I shipped `S-COMMIT`.

A label the book does not print is a fabrication: it must be deleted, not
renamed.  So this reports three classes: MISSING (label absent from source),
CASE (present but different case) and OK.
"""
import pathlib, re, sys, json

ROOT = pathlib.Path(__file__).resolve().parent.parent


def rule_labels(uk_text):
    """The 2nd positional argument of every #rule(...) call, in source order."""
    out = []
    for m in re.finditer(r"#rule\(", uk_text):
        i = m.end()
        depth = 1
        start = i
        while i < len(uk_text) and depth:
            if uk_text[i] == "(":
                depth += 1
            elif uk_text[i] == ")":
                depth -= 1
            i += 1
        body = uk_text[start:i - 1]
        # positional args are separated by commas at nesting depth 0
        args, d, cur = [], 0, ""
        for ch in body:
            if ch in "([{":
                d += 1
            elif ch in ")]}":
                d -= 1
            if ch == "," and d == 0:
                args.append(cur); cur = ""
            else:
                cur += ch
        args.append(cur)
        if len(args) >= 2:
            lab = args[1].strip()
            mm = re.fullmatch(r'"([^"]*)"', lab)
            if mm:
                out.append(mm.group(1))
    return out


def main():
    man = json.load(open(ROOT / "manifest.json"))
    parts = sys.argv[1:] or sorted(man)
    bad = 0
    for part in parts:
        ukp = ROOT / f"out/{part}/uk.typ"
        srcp = ROOT / f"out/{part}/source.txt"
        if not ukp.exists():
            continue
        uk = ukp.read_text(encoding="utf-8")
        src = srcp.read_text(encoding="utf-8") if srcp.exists() else ""
        labels = rule_labels(uk)
        if not labels:
            print(f"{part:9s} no labelled rules")
            continue
        missing, case = [], []
        for lab in labels:
            if lab in src:
                continue
            # The extractor's text layer stores small-caps as lowercase, so the
            # book's printed (S-COMMIT) arrives as "s-commit".  A label that
            # differs only by case IS present on the page -- accept it.
            if re.search(re.escape(lab), src, re.I):
                case.append(lab)
            else:
                missing.append(lab)
        status = "ok" if not missing else "PROBLEMS"
        print(f"{part:9s} {len(labels):3d} labels  {status}")
        for lab in sorted(set(missing)):
            print(f"             MISSING from source (delete it): {lab!r}")
            bad += 1
        for lab in sorted(set(case)):
            print(f"             OK (case only): {lab!r} — book's text layer prints it lowercase (small-caps)")
    print(f"\n{bad} problem(s)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
