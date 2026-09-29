#!/usr/bin/env python3
"""Compare the default split choice with an adaptive one (4 unfixed triangles of smallest |area| in the region's
incumbent points) on a few open VM regions. Uses heil_tri.py unchanged via the driver's solve()."""
import json, sys, os, itertools, time
sys.path.insert(0, '/home/user/Claude/heilbronn-cloud-results/tools')
import split_until_proved_260927 as D
T = D.T
leaves, out, k = sys.argv[1], sys.argv[2], int(sys.argv[3])
os.makedirs(out, exist_ok=True)
L = [l for l in json.load(open(leaves)) if l['reason'] == 'UNRESOLVED' and l['case'] == 'boundary']
def area(p, t):
    (a, b), (c, d), (e, f) = (p[i] for i in t)
    return ((c - a) * (f - b) - (e - a) * (d - b)) / 2
def adaptive(region, pts, size=4):
    fixed = {tuple(t) for t, s in region}
    cand = [t for t in itertools.combinations(range(D.N), 3) if t not in fixed and t not in D.TPLUS]
    return [list(t) for t in sorted(cand, key=lambda t: abs(area(pts, t)))[:size]]
done = 0
for l in L:
    if done >= k: break
    src = l.get('file') or l.get('source')
    try:
        pts = json.load(open(src))['points']
    except Exception:
        continue
    if not pts: continue
    region = [[list(t), int(s)] for t, s in l['region']]
    for mode, sp in (('default', D.choose_split(region)), ('adaptive', adaptive(region, pts))):
        t0 = time.time(); res = [D.solve('/home/user/heil', out, region, sp, p, 60) for p in range(16)]
        pr = sum(r['verdict'] == 'PROVED' for r in res)
        bad = [r for r in res if r['verdict'] == 'BETTER_CONFIGURATION_FOUND']
        print(f'region bound/target {(l.get("best_bound") or 0)/T:.3f} {mode:8s} split {D.compact(sp)}: proved {pr}/16, '
              f'solver {sum(r["runtime"] for r in res):.0f} s, max open bound/target '
              f'{max([r["objbound"]/T for r in res if r["verdict"]!="PROVED"] or [0]):.3f}{" BETTER!" if bad else ""}', flush=True)
    done += 1
