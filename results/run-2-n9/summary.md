# Heilbronn triangle certification summary: n = 9, target = 0.027426211734693878

| case | part | prefix | verdict | status | runtime (s) | upper bound | best found |
|---|---|---|---|---|---|---|---|
| boundary | 0 |  | UNRESOLVED | TIME_LIMIT | 19800 | 0.027767733409468625 | 0.02742345411558178 |
| boundary | 1 |  | PROVED | BOUND_REACHED | 8296 | 0.027426169964296067 | 0.022851075365847857 |
| boundary | 2 |  | PROVED | BOUND_REACHED | 1476 | 0.02742615953221971 | 0.024656114757285866 |
| boundary | 3 |  | PROVED | BOUND_REACHED | 1983 | 0.02742606034858934 | 0.021862689203362474 |
| boundary | 4 |  | PROVED | BOUND_REACHED | 3545 | 0.027426187591618315 | 0.026190774043193032 |
| boundary | 5 |  | PROVED | BOUND_REACHED | 722 | 0.027425817838500316 | 0.025240524823889998 |
| boundary | 6 |  | PROVED | BOUND_REACHED | 1116 | 0.027425944008069632 | 0.02497808785744937 |
| boundary | 7 |  | PROVED | BOUND_REACHED | 5775 | 0.027426009089405047 | 0.023451728082932072 |
| boundary | 8 |  | UNRESOLVED | TIME_LIMIT | 19800 | 0.027791772369286864 | 0.026438825054787063 |
| boundary | 9 |  | PROVED | BOUND_REACHED | 1171 | 0.02742581680574013 | 0.02549580916473676 |
| boundary | 10 |  | PROVED | BOUND_REACHED | 3134 | 0.027426009282646494 | 0.02544851217032705 |
| boundary | 11 |  | PROVED | BOUND_REACHED | 1288 | 0.027426209782408964 | 0.02485622183537727 |
| boundary | 12 |  | PROVED | BOUND_REACHED | 2830 | 0.02742612345671842 | 0.024758918579011007 |
| boundary | 13 |  | PROVED | BOUND_REACHED | 3073 | 0.02742589031423176 | 0.02567487178275245 |
| boundary | 14 |  | PROVED | BOUND_REACHED | 4887 | 0.02742593406630463 | 0.025674871773097768 |
| boundary | 15 |  | PROVED | BOUND_REACHED | 12848 | 0.027426192310569874 | 0.02475188661446996 |
| boundary | 16 |  | PROVED | BOUND_REACHED | 3243 | 0.027426059043536496 | 0.025639742802876866 |
| boundary | 17 |  | PROVED | BOUND_REACHED | 2082 | 0.027425580165775332 | 0.024834884910087007 |
| boundary | 18 |  | PROVED | BOUND_REACHED | 2729 | 0.027426185344513705 | 0.02549109295069976 |
| boundary | 19 |  | PROVED | BOUND_REACHED | 781 | 0.027425273221417995 | 0.02479869565905891 |
| boundary | 20 |  | PROVED | BOUND_REACHED | 7602 | 0.02742616458937996 | 0.025648309952204632 |
| boundary | 21 |  | PROVED | BOUND_REACHED | 2769 | 0.027425955660418305 | 0.02613767046710833 |
| boundary | 22 |  | PROVED | BOUND_REACHED | 2051 | 0.02742602730190061 | 0.025674874161698353 |
| boundary | 23 |  | PROVED | BOUND_REACHED | 6506 | 0.027426149835670852 | 0.0261904592804199 |
| boundary | 24 |  | PROVED | BOUND_REACHED | 4688 | 0.027426121475569606 | 0.02567486947717036 |
| boundary | 25 |  | PROVED | BOUND_REACHED | 5873 | 0.027426166850133608 | 0.02564781680783235 |
| boundary | 26 |  | PROVED | BOUND_REACHED | 3322 | 0.027426200201101553 | 0.02564873238972201 |
| boundary | 27 |  | PROVED | BOUND_REACHED | 10442 | 0.027426210565045437 | 0.02643952708562713 |
| boundary | 28 |  | PROVED | BOUND_REACHED | 7866 | 0.027426186024848174 | 0.026438859827066535 |
| boundary | 29 |  | UNRESOLVED | TIME_LIMIT | 19800 | 0.027805170387733003 | 0.027423461345311845 |
| boundary | 30 |  | UNRESOLVED | TIME_LIMIT | 19800 | 0.031026828570523562 | 0.027423461400342106 |
| boundary | 31 |  | UNRESOLVED | TIME_LIMIT | 19800 | 0.03183075623995534 | 0.027423462028306374 |
| vertices | 0 |  | PROVED | BOUND_REACHED | 1375 | 0.027425453952285156 | 0.0239265479801289 |

Verdict counts: {'UNRESOLVED': 5, 'PROVED': 28}

Unresolved parts. Re-run each with a deeper split: copy its prefix below into the workflow input "prefix",
set "split" to a new list of triangles, and "parts" to the full range for that split.
- case boundary part 0: prefix = [[[2, 3, 4], 0], [[2, 3, 5], 0], [[2, 3, 6], 0], [[2, 3, 7], 0], [[2, 3, 8], 0]]
- case boundary part 29: prefix = [[[2, 3, 4], 1], [[2, 3, 5], 0], [[2, 3, 6], 1], [[2, 3, 7], 1], [[2, 3, 8], 1]]
- case boundary part 30: prefix = [[[2, 3, 4], 0], [[2, 3, 5], 1], [[2, 3, 6], 1], [[2, 3, 7], 1], [[2, 3, 8], 1]]
- case boundary part 31: prefix = [[[2, 3, 4], 1], [[2, 3, 5], 1], [[2, 3, 6], 1], [[2, 3, 7], 1], [[2, 3, 8], 1]]
- case boundary part 8: prefix = [[[2, 3, 4], 0], [[2, 3, 5], 0], [[2, 3, 6], 0], [[2, 3, 7], 1], [[2, 3, 8], 0]]

Boundary case fully covered by proved parts: False
Corners-occupied case proved: True
All results use the same n and target: True
Not (yet) a complete certificate.
