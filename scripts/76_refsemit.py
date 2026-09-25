#!/usr/bin/env python3
"""Emit the four bibliography parts (_gen1..4.txt) from the book's own spans.

What must be reproduced faithfully:
  * the ENTRY split (one reference per entry);
  * the ITALICS marking work titles (journal / proceedings / book names); and
  * the WORD SEPARATION, including words that run across a line break.

Rather than guess where a title starts, read the italic spans: in this section font
`F5` is the italic title font, `Gb` the roman body, `F1` the URL font and `F3` the
math font.

Two measurements drive every layout decision, both taken from the book itself:

  * LINE CLUSTERING — spans are grouped into printed lines by y-proximity (4pt), NOT
    by bucketing y.  Bucketing splits a printed line when its spans differ by 0.1pt
    (p550: y=142.5 vs y=142.6), which emitted a fragment as a bogus extra entry.

  * WORD GAPS — for adjacent spans on a printed line the horizontal gap is either
    0.0pt (contiguous, 473 occurrences book-wide) or >= 5.5pt (a word space, 118
    occurrences), with essentially nothing in between.  So a space belongs between two
    spans exactly when the gap is >= SPACE_GAP, or when the source text already
    carries whitespace at the boundary.  This is what keeps "Manager].May 2002" from
    appearing and restores the space in "baastad. 92/proc.ps.Z".

A word split by a typeset hyphen ("communi-" / "cation", "Programma-" / "tion") is
rejoined by dropping the hyphen; whether a line-final hyphen is a typeset break or an
authored compound is decided against the book's own mid-line vocabularies.
"""
import fitz, json, pathlib, re
from collections import Counter

ROOT = pathlib.Path('/Users/ihor/atapl')
doc = fitz.open(next(ROOT.glob('*.pdf')))
U = json.load(open(ROOT / 'src' / 'units.json'))['refs']
OUT = ROOT / 'out' / 'refs01'

ITALIC = {'F5'}            # the italic title font of this section
START_MAX_X = 170.0        # entries flush left at 163/167; continuations at 173/177
SPACE_GAP = 5.5            # pt; measured: 0.0 contiguous, >=5.5 a word space
LIG = {'\ufb00': 'ff', '\ufb01': 'fi', '\ufb02': 'fl', '\ufb03': 'ffi', '\ufb04': 'ffl'}
TOKEN = re.compile(r'[A-Za-z\u00c0-\u00ff][\w\u00c0-\u00ff’\'-]*')


def fold(s):
    """Expand ligatures (U+FB01 fi, U+FB02 fl, ...) — the extraction keeps them while
    the book's words contain the expanded forms, so comparisons must fold them."""
    for a, b in LIG.items():
        s = s.replace(a, b)
    return s


def esc(s):
    """Escape Typst specials in content mode.

    Three traps, each found by compiling the real entries:
      * brackets: every entry is wrapped as `#refentry[ ... ]`, so an unescaped `]`
        inside a reference would close the wrapper early;
      * `\\`, `#`, `$`, `@`, `*`, `_`, `~`: ordinary markup specials (a `\\` is
        dropped, since none in this section carries meaning);
      * a URL's `//`: Typst reads `//` in markup as the start of a LINE COMMENT, so a
        raw `ftp://host/path` swallows the rest of the entry and the wrapper's closing
        bracket with it ("unclosed delimiter").  Escaping the first slash of the pair
        (`ftp:\\//host/path`) renders the URL correctly, verified by compiling and
        reading the text back.
    """
    s = s.replace('\\', '')
    for ch in '#$@*_~[]':
        s = s.replace(ch, '\\' + ch)
    s = re.sub(r'(\w:)//', r'\1\\//', s)
    # Ligatures are PRESENTATION forms, not text: the extraction renders `ff`/`fi`/`fl`
    # as U+FB00…U+FB04 and they would be printed verbatim as a single glyph, so a
    # reader copying a title gets a word that won't match "efficient"/"flow"/
    # "verification" anywhere.  fold() was only ever applied when COMPARING
    # (hyphen vocabularies, the solid/hyphenated decision); the emitted run needs the
    # expanded spelling too, and esc() is the one funnel every run passes through.
    return fold(s)


def page_spans(page):
    """[(y, x0, x1, italic, text)] for the body of one page."""
    out = []
    for blk in doc[page].get_text('dict')['blocks']:
        for l in blk.get('lines', []):
            for s in l['spans']:
                if not s['text'].strip():
                    continue
                y = s['bbox'][1]
                # Measured window (see scripts/72_refsorder.py): the running head
                # is at y=34.2, the body spans 67.5 … 569.8.  A 100pt floor cut
                # off the head line of every page's first entry.
                if not (50 < y < 600):
                    continue
                out.append((y, s['bbox'][0], s['bbox'][2], s['font'] in ITALIC, s['text']))
    out.sort(key=lambda t: (t[0], t[1]))
    return out


def cluster_lines(spans):
    """Group spans into printed lines by y-proximity: [[span, ...], ...]."""
    lines = []
    for sp in spans:
        if lines and sp[0] - lines[-1][0] <= 4.0:
            lines[-1][1].append(sp)
        else:
            lines.append([sp[0], [sp]])
    return [sorted(l[1], key=lambda t: t[1]) for l in lines]


def build_vocab():
    """Mid-line `solid` / `hyph` vocabularies, plus the `bridged` word set.

    Deciding whether a line-final hyphen is authored needs evidence from the book: a
    typesetter's break only ever occurs at a line END, so a compound written with a
    hyphen mid-line ("control-flow", "Springer-Verlag") is authored, while a word that
    only appears solid mid-line ("communication") was broken by the typesetter.  A
    line-final hyphenated token is excluded from both sets — it is the evidence being
    gathered and must not be used as proof of itself.

    `bridged` records words formed by joining a break to the next line, so a proper
    noun appearing only once in the book (at a break) is not reported as unknown.
    """
    solid, hyph, bridged = set(), set(), set()
    for p in range(U['first'], U['last'] + 1):
        texts = []
        for line in cluster_lines(page_spans(p)):
            t = fold(''.join(s[4] for s in line))
            texts.append(t)
            end = len(t.rstrip())
            for m in TOKEN.finditer(t):
                tok = m.group(0)
                # Only a LINE-FINAL HYPHENATED token is excluded: it is the evidence
                # being gathered and must not be used as proof of itself.  A line-final
                # token WITHOUT a hyphen is perfectly good evidence (the word is
                # printed whole), and excluding it would drop legitimate words like
                # "cryptographic" and "nominal" that merely happen to end a line —
                # which is exactly what made them show up as unknown words.
                if m.end() >= end and tok.endswith('-'):
                    continue
                (hyph if '-' in tok else solid).add(tok.lower())
        for i in range(len(texts) - 1):
            a, b = texts[i].rstrip(), texts[i + 1].lstrip()
            if a.endswith('-'):
                ta, tb = TOKEN.findall(a), TOKEN.findall(b)
                if ta and tb:
                    bridged.add((ta[-1][:-1] + tb[0]).lower())
    return solid, hyph, bridged


def glue_line(line):
    """[(italic, text)] for one printed line, inserting printed word spaces.

    The separator decision is geometric: a space belongs between two spans exactly
    when their gap is >= SPACE_GAP, or when the source already carries whitespace
    there.  Getting this wrong is visible — "Manager].May 2002" (space lost) or
    "B, l, u, m, e" (a space inserted after every letter).
    """
    parts = []
    for i, (_y, x0, x1, it, text) in enumerate(line):
        if i:
            prev_x1 = line[i - 1][2]
            prev_text = parts[-1][1]
            if (x0 - prev_x1) >= SPACE_GAP or text[:1].isspace() \
                    or prev_text[-1:].isspace():
                parts.append((False, ' '))
        parts.append((it, text.strip('\n')))
    return parts


def build_entry(lines, solid, hyph):
    """(texts, styles, decided) for a whole entry, joining its printed lines.

    The entry is assembled as ONE string plus a parallel per-character style list,
    and the hyphen sites are resolved on that whole string.  Resolving per-run would
    be wrong: a placeholder often lands in a run of its own, so its neighbours would
    read as empty and the site would be dropped silently (which is how the earlier
    version lost ALL 181 hyphen sites while reporting zero).
    """
    text, style = '', []

    def add(s, it):
        nonlocal text
        text += s
        style.extend([it] * len(s))

    for li, line in enumerate(lines):
        if li:
            prev = text.rstrip()
            cur = ''.join(s[4] for s in line).lstrip()
            if prev.endswith('-') and cur[:1].isalpha():
                # The hyphen is AMBIGUOUS — a typesetter's break ("sub-" +
                # "stitutions") or an authored compound broken at its own hyphen
                # ("dexptime-" + "complete") look identical.  Drop it and record a
                # placeholder; resolve_joins decides it against the book.
                k = len(text) - 1
                while k >= 0 and text[k].isspace():
                    k -= 1
                if k >= 0 and text[k] == '-':
                    text = text[:k]
                    del style[k:]
                add('\x00', False)
            else:
                add(' ', False)
        for it, t in glue_line(line):
            add(t.replace('\n', ' '), it)

    decided = []
    text, style = resolve_joins(text, style, solid, hyph, decided)
    # merge neighbouring runs of the same style
    merged = []
    for i, ch in enumerate(text):
        it = style[i]
        if merged and merged[-1][0] == it:
            merged[-1][1] += ch
        else:
            merged.append([it, ch])
    return [t for _it, t in merged], [it for it, _t in merged], decided


def resolve_joins(text, style, solid, hyph, decided):
    """Decide each line-final hyphen site against the book's vocabularies.

    "communication" is in the SOLID vocabulary, so the break in "communi-" is
    typeset and the halves are joined.  "control-flow" is in the HYPHENATED one, so
    the hyphen is authored and kept.  Checked in that order, so a word that genuinely
    contains a hyphen (the French "Programmation", "semi-unification") resolves right.

    Returns (text, style) with the placeholder replaced by '' or '-'.
    """
    out, outst, i = '', [], 0
    while i < len(text):
        if text[i] != '\x00':
            out += text[i]
            outst.append(style[i])
            i += 1
            continue
        j = i - 1
        while j >= 0 and (text[j].isalpha() or text[j] in '’\''):
            j -= 1
        left = text[j + 1:i]
        k = i + 1
        while k < len(text) and (text[k].isalpha() or text[k] in '’\''):
            k += 1
        right = text[i + 1:k]
        keep = ''
        if left and right:
            # fold() both sides: the vocabulary was built from de-ligatured text, and a
            # candidate like "control-ﬂow" (with an fl ligature) would never match it raw
            joined = fold(left + right).lower()
            hyphenated = fold(left + '-' + right).lower()
            if joined not in solid and hyphenated in hyph:
                keep = '-'
            decided.append((left, right, 'hyphen' if keep else 'join'))
        if keep:
            out += keep
            outst.append(False)
        i += 1
    return out, outst


def markup(runs):
    """Typst string with #emph[...] around the italic runs.

    Whitespace at an italic run's edges is moved OUTSIDE the markup: the book sets
    ". Explicit substitutions." then " Journal of Functional Programming" in italics,
    and a leading space left inside #emph[...] renders a visibly wider gap while
    dropping it glues the words ("processing.#emph[Journal]").
    """
    out = ''
    for it, t in runs:
        if not t:
            continue
        if it:
            lead = t[:1] if t[:1].isspace() else ''
            trail = t[-1:] if t[-1:].isspace() else ''
            body = esc(t.strip())
            out += lead + ('#emph[' + body + ']' if body else '') + trail
        else:
            out += esc(t)
    out = re.sub(r'(?<=[^\s\[(])#emph\[(?=[A-Z])', ' #emph[', out)   # glued boundary
    out = re.sub(r'\]#emph\[', '] #emph[', out)
    return re.sub(r'[ \t]+', ' ', out).strip()


def main():
    print('building vocabulary ...')
    solid, hyph, bridged = build_vocab()
    print(f'  {len(solid)} solid mid-line words, {len(hyph)} hyphenated, '
          f'{len(bridged)} break-joined')

    entries, cur = [], []
    for p in range(U['first'], U['last'] + 1):
        for line in cluster_lines(page_spans(p)):
            if min(s[1] for s in line) <= START_MAX_X:
                if cur:
                    entries.append(cur)
                cur = [line]
            else:
                cur.append(line)
    if cur:
        entries.append(cur)
    print(f'entries found: {len(entries)}')

    decided, built = [], []
    for lines in entries:
        texts, styles, dec = build_entry(lines, solid, hyph)
        decided += dec
        e = markup(list(zip(styles, texts)))
        if not e or e.lower() == 'references':
            continue
        built.append(e)

    kept = [d for d in decided if d[2] == 'hyphen']
    print(f'line-final hyphen sites: {len(decided)}  (kept as hyphen: {len(kept)})')
    for left, right, _how in kept:
        print(f'   KEPT: {left}-{right}')

    # ---- verification: every word of the output must occur in the book
    vocab = set(solid) | set(hyph) | set(bridged)
    for w in list(vocab):
        for part in re.split(r'[-–—]', w):
            if part:
                vocab.add(part)
    for w in list(vocab):
        vocab.add(w.lower())
        vocab.add(w.capitalize())
    bad = Counter()
    for e in built:
        plain = fold(e.replace('#emph[', '').replace(']', '').replace('\\', ''))
        for tok in TOKEN.findall(plain):
            if len(tok) < 4 or tok.isdigit():
                continue
            if tok.lower() in vocab or tok in vocab:
                continue
            bad[tok] += 1
    if bad:
        print('words not found in the book (check these):')
        for w, n in bad.most_common(20):
            print(f'   {w}  x{n}')
    else:
        print('vocabulary check: PASS — every word appears in the book')

    parts = 4
    per = (len(built) + parts - 1) // parts
    for i in range(parts):
        chunk = built[i * per:(i + 1) * per]
        if not chunk:
            continue
        f = OUT / f'_gen{i + 1}.txt'
        f.write_text('\n\n'.join(chunk), encoding='utf-8')
        print(f'  _gen{i + 1}.txt: {len(chunk):3d} entries')


if __name__ == '__main__':
    main()
