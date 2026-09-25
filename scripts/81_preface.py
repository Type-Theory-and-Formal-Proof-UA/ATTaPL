#!/usr/bin/env python3
"""Extract the Preface (book pages 10-14) as translatable source text.

The preface is front matter, not a chapter, so it was never in manifest.json and
never reached a translator.  It is real prose (the editor's overview of the five
parts and the acknowledgements), so it belongs in the translated book for the same
reason the appendix, references and index do.

Cleaning follows the measured page bands from scripts/72_refsorder.py: the running
head ("Preface" + folio) sits at y=34.2 and is dropped; the body spans 67.5..569.8.
The folio appears as a bare roman numeral line and is dropped too.
"""
import fitz, pathlib, re

ROOT = pathlib.Path('/Users/ihor/atapl')
doc = fitz.open(next(ROOT.glob('*.pdf')))
FIRST, LAST = 9, 13          # 0-based page indices: book pages 10..14

out_dir = ROOT / 'out' / 'preface01'
out_dir.mkdir(parents=True, exist_ok=True)

chunks = []
for p in range(FIRST, LAST + 1):
    lines = []
    for blk in doc[p].get_text('dict')['blocks']:
        for l in blk.get('lines', []):
            sp = [s for s in l['spans'] if s['text'].strip()]
            if not sp:
                continue
            y = min(s['bbox'][1] for s in sp)
            if y < 50 or y > 600:            # running head / footer band
                continue
            x = min(s['bbox'][0] for s in sp)
            txt = ''.join(s['text'] for s in sp).strip()
            if re.fullmatch(r'[ivxlcdm]{1,6}', txt) and y < 90:
                continue                      # folio alone on its line
            lines.append((round(y, 1), x, txt, sp[0]['font']))
    # join hyphenated line breaks, then collapse to one paragraph per blank gap
    body = []
    prev_y = None
    for y, x, txt, _ in lines:
        if prev_y is not None and y - prev_y > 16:
            body.append('')                   # paragraph break
        body.append(txt)
        prev_y = y
    chunks.append('\n'.join(body))

raw = '\n\n'.join(chunks)
# rejoin typesetter's hyphen breaks: "dis-\ntributed" -> "distributed"
raw = re.sub(r'([A-Za-z])-\n([a-z])', r'\1\2', raw)
raw = re.sub(r'\n+', '\n', raw)
# fold ligatures (presentation forms, see scripts/76_refsemit.py)
LIG = {'\ufb00': 'ff', '\ufb01': 'fi', '\ufb02': 'fl', '\ufb03': 'ffi', '\ufb04': 'ffl'}
for a, b in LIG.items():
    raw = raw.replace(a, b)

# headings the extractor prints inline
raw = raw.replace('Preface\n', '', 1)
(src := out_dir / 'source.txt').write_text(raw.strip() + '\n', encoding='utf-8')
print('wrote', src)
print('words:', len(raw.split()))
print('--- first 500 chars ---')
print(raw[:500])
print('--- last 300 chars ---')
print(raw[-300:])
