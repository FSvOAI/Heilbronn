#!/usr/bin/env python3
"""Aggregate result_*.json files from a certification run and decide what has been proved.

Usage: python summarize.py <folder-with-result-json-files> [--md summary.md]
Prints a table, the overall verdict, and ready-to-paste workflow inputs for refining unresolved parts.
"""
import glob, json, os, sys
from collections import Counter

def main():
    folder = sys.argv[1] if len(sys.argv) > 1 else '.'
    md_path = sys.argv[sys.argv.index('--md') + 1] if '--md' in sys.argv else None
    files = sorted(glob.glob(os.path.join(folder, '**', 'result_*.json'), recursive=True))
    rows = [json.load(open(f)) for f in files]
    if not rows:
        print('no result files found'); return
    lines = []
    P = lambda s='': (print(s), lines.append(s))
    n = rows[0]['n']; target = rows[0]['cutoff']
    P(f'# Heilbronn triangle certification summary: n = {n}, target = {target!r}')
    P('')
    P('| case | part | prefix | verdict | status | runtime (s) | upper bound | best found |')
    P('|---|---|---|---|---|---|---|---|')
    for r in sorted(rows, key=lambda r: (r['case'], r['prefix'], r['part'])):
        P(f"| {r['case']} | {r['part']} | {r['prefix'] if r['prefix'] != '[]' else ''} | {r.get('verdict')} | {r['status']} | "
          f"{r['runtime']:.0f} | {r.get('objbound')} | {r.get('objval')} |")
    v = Counter(r.get('verdict') for r in rows)
    P('')
    P(f'Verdict counts: {dict(v)}')
    better = [r for r in rows if r.get('verdict') == 'BETTER_CONFIGURATION_FOUND']
    if better:
        P('')
        P('**A configuration above the target was reported. Verify it exactly with verify_config.py before claiming anything.**')
        for r in better:
            P(f"- case {r['case']} part {r['part']}: value {r['objval']}, points {r.get('points')}")
    unresolved = [r for r in rows if r.get('verdict') == 'UNRESOLVED']
    if unresolved:
        P('')
        P('Unresolved parts. Re-run each with a deeper split: copy its prefix below into the workflow input "prefix",')
        P('set "split" to a new list of triangles, and "parts" to the full range for that split.')
        for r in unresolved:
            split = json.loads(r['split']); part = r['part']
            prefix = json.loads(r['prefix']) + [[t, (part >> i) & 1] for i, t in enumerate(split)]
            P(f"- case {r['case']} part {part}: prefix = {json.dumps(prefix)}")
    # ---- completeness check: is every region of the case split covered by a PROVED leaf?
    groups = {}
    for r in rows:
        if r['case'] != 'boundary':
            continue
        key = json.dumps(sorted(json.loads(r['prefix'])))
        groups.setdefault(key, []).append(r)
    def covered(prefix, depth=0):
        key = json.dumps(sorted(prefix))
        if key not in groups or depth > 20:
            return False
        for split_json in set(r['split'] for r in groups[key]):
            split = json.loads(split_json)
            rs = {r['part']: r for r in groups[key] if r['split'] == split_json}
            ok = True
            for k in range(2 ** len(split)):
                if k in rs and rs[k].get('verdict') == 'PROVED':
                    continue
                child = prefix + [[t, (k >> i) & 1] for i, t in enumerate(split)]
                if not covered(child, depth + 1):
                    ok = False; break
            if ok:
                return True
        return False
    tgt_ok = len(set(r['cutoff'] for r in rows)) == 1 and len(set(r['n'] for r in rows)) == 1
    boundary_ok = covered([])
    vert_ok = any(r['case'] == 'vertices' and r.get('verdict') == 'PROVED' and r['prefix'] == '[]' for r in rows)
    P('')
    P(f'Boundary case fully covered by proved parts: {boundary_ok}')
    P(f'Corners-occupied case proved: {vert_ok}')
    P(f'All results use the same n and target: {tgt_ok}')
    if boundary_ok and vert_ok and tgt_ok and not better:
        P(f'**CERTIFIED (subject to the model assumptions in README): every configuration of n = {n} points in the unit right '
          f'triangle has minimum triangle area <= {target}.**')
    else:
        P('Not (yet) a complete certificate.')
    if md_path:
        open(md_path, 'w').write('\n'.join(lines) + '\n')

if __name__ == '__main__':
    main()
