#!/usr/bin/env python3
"""Merge the parallel-translated back-matter parts into out/<part>/uk.typ.

refs  -> out/refs01/uk.typ   from _part1.._part4.typ
index -> out/index01/uk.typ  from _part1.._part2.typ

Each part file was written by a separate agent and therefore repeats the shared
header (a comment, the preamble import) and its own helper definitions.  The
merge keeps exactly ONE preamble import and ONE definition of each helper, in
the first part that defines it; later parts contribute only their body lines.
"""
import pathlib, re, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

JOBS = [
    ('refs01', 4, 'Бібліографія', 'References'),
    ('index01', 2, 'Покажчик', 'Index'),
]
HEAD_RE = re.compile(r'^\s*(//.*|#import\s+"/templates/preamble\.typ"\s*:\s*\*|#let\s+\w+\s*=.*)$')


def body_of(path):
    """Return (imports, helper_defs, body_lines) for one part file."""
    imports, defs, body = [], [], []
    for line in path.read_text(encoding='utf-8').split('\n'):
        s = line.strip()
        if s.startswith('//') and not body:
            continue
        if s.startswith('#import "/templates/preamble.typ"'):
            imports.append(line)
            continue
        if s.startswith('#let ') and not body:
            m = re.match(r'#let\s+(\w+)', s)
            if m:
                defs.append((m.group(1), line))
                continue
        body.append(line)
    return imports, defs, body


def merge(unit, nparts, uk_title, en_title):
    d = ROOT / 'out' / unit
    imports, defs, seen, body = [], [], set(), []
    missing = []
    for i in range(1, nparts + 1):
        p = d / f'_part{i}.typ'
        if not p.exists():
            missing.append(p.name)
            continue
        im, df, bd = body_of(p)
        if im and not imports:
            imports = im
        for name, line in df:
            if name not in seen:
                seen.add(name)
                defs.append(line)
        body.append(f'\n// ---- частина {i} ----')
        body.extend(bd)
    if missing:
        print(f'{unit}: MISSING parts {missing} — not merged')
        return None
    header = [f'// Згенеровано scripts/58_merge_back.py з _part*.typ — не редагувати вручну.',
              f'// {uk_title} ({en_title})']
    header += imports if imports else ['#import "/templates/preamble.typ": *']
    header += defs
    # Back-matter heading: the book prints it in italic, flush with the columns.
    header.append(f'#heading(level: 1, outlined: true)[{uk_title}]')
    out = d / 'uk.typ'
    out.write_text('\n'.join(header) + '\n' + '\n'.join(body) + '\n', encoding='utf-8')
    r = subprocess.run(['typst', 'compile', '--root', str(ROOT), str(out), f'/tmp/{unit}.pdf'],
                       capture_output=True, text=True)
    status = 'ok' if r.returncode == 0 else 'FAIL'
    print(f'{unit}: merged -> {out}  compile={status}')
    if r.returncode != 0:
        for l in r.stderr.strip().split('\n')[:6]:
            print('   ', l)
    return out


if __name__ == '__main__':
    only = sys.argv[1] if len(sys.argv) > 1 else None
    for unit, n, uk, en in JOBS:
        if only and unit != only:
            continue
        merge(unit, n, uk, en)
