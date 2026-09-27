"""Heilbronn problem in the unit right triangle T = {x,y>=0, x+y<=1}: MIQCP certification model.

Follows Sudermann-Merx, arXiv:2607.15021 (model (1) + Proposition 1 / Corollary 1):
  * case 'boundary': p0,p1 on y=0 (x0<=x1, x0+x1<=1), p2 on x+y=1, p3 on x=0; free points p4.. sorted by x.
    Triangles among p0..p3 and (p0,p1,k) are positively oriented (set T+).
  * case 'vertices': the three corners of T are occupied; the other n-3 points free (sorted by x).
Certification mode: add z >= cutoff and prove INFEASIBLE (=> Delta_n < cutoff in this (sub)case).
Splitting: --split-tris lists orientation binaries to fix; --part p in [0, 2^d) selects the sign pattern.
"""
import argparse, itertools, json, time, sys

def build(n, case, cutoff, zub, split_tris, part, solver, threads, timelimit, cutmode='param', prefix=()):
    pts = list(range(n)); tris = list(itertools.combinations(pts, 3))
    if solver == 'gurobi':
        import gurobipy as gp
        from gurobipy import GRB
        m = gp.Model(); m.Params.OutputFlag = 1; m.Params.Threads = threads; m.Params.TimeLimit = timelimit
        m.Params.MIPGap = 5e-5; m.Params.MIPFocus = 2; m.Params.NonConvex = 2
        if cutoff is not None and cutmode == 'param': m.Params.Cutoff = cutoff
        if cutoff is not None and cutmode == 'bdstop': m.Params.BestBdStop = cutoff
        cont = lambda lb, ub, name: m.addVar(lb=lb, ub=ub, name=name)
        binv = lambda name: m.addVar(vtype=GRB.BINARY, name=name)
        addc = m.addConstr
    else:
        from pyscipopt import Model
        m = Model(); m.setParam('limits/time', timelimit); m.setParam('parallel/maxnthreads', threads)
        m.setParam('limits/gap', 1e-6)
        if cutoff is not None and cutmode == 'param': m.setObjlimit(cutoff)
        cont = lambda lb, ub, name: m.addVar(lb=lb, ub=ub, name=name)
        binv = lambda name: m.addVar(vtype='B', name=name)
        addc = m.addCons
    x, y = {}, {}
    free_start = 0
    if case == 'boundary':
        x[0] = cont(0, 1, 'x0'); y[0] = 0
        x[1] = cont(0, 1, 'x1'); y[1] = 0
        y[2] = cont(0, 1, 'y2'); x[2] = 1 - y[2]
        x[3] = 0; y[3] = cont(0, 1, 'y3')
        addc(x[0] <= x[1]); addc(x[0] + x[1] <= 1)
        free_start = 4
    else:  # vertices
        x[0], y[0] = 0, 0; x[1], y[1] = 1, 0; x[2], y[2] = 0, 1
        free_start = 3
    for i in pts[free_start:]:
        x[i] = cont(0, 1, f'x{i}'); y[i] = cont(0, 1, f'y{i}')
        addc(x[i] + y[i] <= 1)
        if i > free_start: addc(x[i - 1] <= x[i])
    z = cont(0, zub, 'z')
    if cutoff is not None and cutmode == 'constraint': addc(z >= cutoff)
    # signed area: linear in auxiliary product variables w[i,j] = x_i * y_j (the paper's substitution)
    W = {}
    def w(i, j):
        xi, yj = x[i], y[j]
        if isinstance(xi, (int, float)) or isinstance(yj, (int, float)):
            return xi * yj            # constant or linear term, no auxiliary needed
        if (i, j) not in W:
            W[i, j] = cont(0, 1, f'w{i}_{j}')
            addc(W[i, j] == xi * yj)
        return W[i, j]
    def A(i, j, k):
        return 0.5 * (w(i, j) - w(i, k) - w(j, i) + w(j, k) + w(k, i) - w(k, j))
    if case == 'boundary':
        tplus = set(t for t in tris if max(t) <= 3) | set((0, 1, k) for k in pts[4:])
    else:
        tplus = set()  # corners (0,0),(1,0),(0,1) ccw: triangle (0,1,2) positive; (0,1,k),(1,2,k),(0,2,k)?
        tplus.add((0, 1, 2))
        for k in pts[3:]:
            tplus.add((0, 1, k))   # k above y=0 -> positive
        # (0,2,k): points (0,0),(0,1),k with x_k>0 -> negative orientation; (1,2,k): k below hypotenuse -> positive
    tminus = set()
    if case == 'vertices':
        tminus = set((0, 2, k) for k in pts[3:])
        tplus |= set((1, 2, k) for k in pts[3:])
    fixed = {tuple(t): int(sg) for t, sg in prefix}
    for idx, t in enumerate(split_tris):
        fixed[tuple(t)] = (part >> idx) & 1
    nb = 0
    for t in tris:
        e = A(*t)
        if t in tplus: s = 1
        elif t in tminus: s = 0
        elif t in fixed: s = fixed[t]
        else: s = None
        if s == 1: addc(z <= e)
        elif s == 0: addc(z <= -e)
        else:
            b = binv(f'b{t[0]}_{t[1]}_{t[2]}'); nb += 1
            # z <= (2b-1) e  (bilinear in b and e; linearise with big-M since |e| <= 1/2)
            addc(z <= e + (1 - b))
            addc(z <= -e + b)
    if solver == 'gurobi':
        m.setObjective(z, GRB.MAXIMIZE)
    else:
        m.setObjective(z, 'maximize')
    return m, x, y, z, nb

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--n', type=int, default=9)
    ap.add_argument('--case', choices=['boundary', 'vertices'], default='boundary')
    ap.add_argument('--cutoff', type=float, default=None)
    ap.add_argument('--zub', type=float, default=0.5)
    ap.add_argument('--cutmode', choices=['bdstop','param','constraint'], default='bdstop')
    ap.add_argument('--split', type=str, default='[]', help='JSON list of triangles to split on')
    ap.add_argument('--part', type=int, default=0)
    ap.add_argument('--prefix', type=str, default='[]', help='JSON list of [[i,j,k], sign] orientations already fixed (for refining a hard part)')
    ap.add_argument('--solver', choices=['gurobi', 'scip'], default='gurobi')
    ap.add_argument('--threads', type=int, default=0)
    ap.add_argument('--timelimit', type=float, default=5.5 * 3600)
    ap.add_argument('--out', type=str, default='result.json')
    a = ap.parse_args()
    split = [tuple(t) for t in json.loads(a.split)]
    t0 = time.time()
    m, x, y, z, nb = build(a.n, a.case, a.cutoff, a.zub, split, a.part, a.solver, a.threads, a.timelimit, a.cutmode, json.loads(a.prefix))
    res = dict(vars(a)); res['binaries'] = nb
    if a.solver == 'gurobi':
        m.optimize()
        st = m.Status
        name = {2: 'OPTIMAL', 3: 'INFEASIBLE', 6: 'CUTOFF', 9: 'TIME_LIMIT', 4: 'INF_OR_UNBD', 15: 'BOUND_REACHED'}.get(st, str(st))
        res.update(status=name, runtime=m.Runtime, nodes=m.NodeCount,
                   objbound=(m.ObjBound if st in (2, 9, 6, 15) else None),
                   objval=(m.ObjVal if m.SolCount > 0 else None))
        if m.SolCount > 0:
            val = lambda v: v if isinstance(v, (int, float)) else v.getValue() if hasattr(v, 'getValue') else v.X
            res['points'] = [[float(val(x[i])), float(val(y[i]))] for i in range(a.n)]
    else:
        m.optimize(); st = m.getStatus()
        res.update(status=st.upper(), runtime=m.getSolvingTime(), nodes=m.getNNodes(),
                   objbound=(m.getDualbound() if st != 'infeasible' else None),
                   objval=(m.getObjVal() if m.getNSols() > 0 else None))
        if m.getNSols() > 0:
            sol = m.getBestSol()
            val = lambda v: float(v) if isinstance(v, (int, float)) else float(m.getSolVal(sol, v))
            res['points'] = [[val(x[i]), val(y[i])] for i in range(a.n)]
    res['wall'] = time.time() - t0
    # Verdict for certification: the (sub)case is PROVED if the solver's global upper bound is <= target.
    tgt = a.cutoff
    if tgt is not None:
        ob = res.get('objbound'); ov = res.get('objval')
        true_min = None
        if res.get('points'):
            pts = []
            for px, py in res['points']:   # clip solver round-off back into T before re-measuring
                px, py = max(px, 0.0), max(py, 0.0)
                if px + py > 1: s_ = px + py; px, py = px / s_, py / s_
                pts.append((px, py))
            true_min = min(abs((q[0]-p[0])*(r[1]-p[1]) - (r[0]-p[0])*(q[1]-p[1])) / 2
                           for p, q, r in itertools.combinations(pts, 3))
            res['recomputed_min_area'] = true_min
        if true_min is not None and true_min > tgt:
            res['verdict'] = 'BETTER_CONFIGURATION_FOUND'
        elif res['status'] in ('INFEASIBLE', 'CUTOFF') or (ob is not None and ob <= tgt):
            res['verdict'] = 'PROVED'
        else:
            res['verdict'] = 'UNRESOLVED'
    json.dump(res, open(a.out, 'w'), indent=1); print(json.dumps({k: res.get(k) for k in ('verdict', 'status', 'runtime', 'objval', 'objbound', 'binaries')}))

if __name__ == '__main__':
    main()
