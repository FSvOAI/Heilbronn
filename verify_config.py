#!/usr/bin/env python3
"""Exact check of a point configuration in the unit right triangle T = {x,y >= 0, x+y <= 1}.

Usage: python verify_config.py points.txt      (two numbers per line; decimals or fractions like 49/56)
Prints the exact minimum triangle area (area of T is 1/2) and the value normalised to a unit-area triangle.
Decimal inputs are converted with limit_denominator(10**6) and reported, so use exact fractions when possible.
"""
import sys, itertools
from fractions import Fraction as F

def parse(tok):
    return F(tok) if '/' in tok else F(tok).limit_denominator(10 ** 6)

pts = []
for line in open(sys.argv[1]):
    line = line.split('#')[0].strip()
    if not line:
        continue
    a, b = line.replace(',', ' ').split()[:2]
    pts.append((parse(a), parse(b)))
for (x, y) in pts:
    assert x >= 0 and y >= 0 and x + y <= 1, f'point {(x, y)} is outside the triangle'
best = None
for p, q, r in itertools.combinations(pts, 3):
    A = abs((q[0] - p[0]) * (r[1] - p[1]) - (r[0] - p[0]) * (q[1] - p[1])) / 2
    best = A if best is None else min(best, A)
print('n =', len(pts))
print('points (exact):', [(str(x), str(y)) for x, y in pts])
print('min area in T (area 1/2):', best, '=', float(best))
print('normalised to unit-area triangle:', 2 * best, '=', float(2 * best))
