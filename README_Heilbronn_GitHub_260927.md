# Heilbronn's triangle problem, 9 points in a triangle — GitHub certification run (27 Sep 2026)

Folder: `C:\Users\fsvo\OneDrive\Documents\Claude\Projects\Six Hills + The Week 100\Heilbronn_GitHub_260927\`

## Acronyms and abbreviations

| Term | Meaning |
|---|---|
| Δₙ | Largest possible minimum triangle area for n points in the unit right triangle T (area ½) |
| CI | Continuous Integration (GitHub Actions is GitHub's CI service; here it is just rented compute) |
| CPU | Central Processing Unit |
| JSON | JavaScript Object Notation (plain-text data format used for inputs and results) |
| MIQCP / MINLP | Mixed-Integer Quadratically Constrained Program / Mixed-Integer Nonlinear Program |
| MIP gap | Relative distance between the best solution found and the proven upper bound |
| SCIP | Free, open-source MINLP solver (fallback to Gurobi) |
| T | The unit right triangle {x ≥ 0, y ≥ 0, x + y ≤ 1} |
| YAML | Text format of the GitHub workflow file |

## Goal and why it would be new

- David Cantrell's 2006 configuration of 9 points (exact rationals on a 1/56 grid, file `cantrell_n9.txt`) has minimum triangle area **43/1568** in T, i.e. 43/784 for a unit-area triangle. `verify_config.py cantrell_n9.txt` confirms this in exact arithmetic.
- Optimality is proven only for n ≤ 8: n = 7 and n = 8 by Sudermann-Merx, arXiv:2607.15021 (July 2026). The public record table at math.tejstead.com lists n = 9 as "record", not proven.
- This pipeline tries to prove that **no 9-point configuration beats 43/1568 by more than a factor 1 + 10⁻⁴**. That is the same certification standard (10⁻⁴ gap) as the n ≤ 8 results, and would be the first optimality certificate for n = 9. If the solver finds a better configuration instead, that is a new record, which is also new knowledge.

## Method

- **Model:** model (1) of arXiv:2607.15021, re-implemented in `heil_tri.py`.
  - Maximise the minimum triangle area z, with one orientation binary per triple and products x_i·y_j as auxiliary variables.
  - The paper's Proposition 1 and Corollary 1 put p0 and p1 on the bottom edge, p2 on the hypotenuse and p3 on the left edge, with x0 ≤ x1 and x0 + x1 ≤ 1.
  - The other points are sorted by x.
  - A separate model covers the case where all three corners are occupied.
- **Splitting:** the orientation of triangles (p2, p3, pk) is fixed in all 2^d combinations, and each combination runs as its own GitHub job. A job is PROVED when Gurobi's upper bound drops to or below the target (Gurobi `BestBdStop`). A job that runs out of time is UNRESOLVED; `summarize.py` then prints the input needed to split it further.
- **Completeness check:** `summarize.py` states CERTIFIED only when every region of the split tree, plus the corners case, is PROVED for the same n and target.
- **Tested locally:** n = 7 reproduces the known optimum 7/144 and certifies it (8 parts plus the corners case, 42 s of solver time on 2 cores). n = 5 (optimum 3/2 − √2) is also reproduced with the free SCIP solver.

## Running it on GitHub

1. **Create a repository** on github.com (empty, no README).
   - **Public:** standard runners are free and have 4 cores each. Your code and results are visible to everyone.
   - **Private:** runners have 2 cores, and minutes are billed to your credit, roughly $0.006–0.012 per job-minute depending on runner size (see the pricing page). One full wave of 33 jobs × 5.5 h costs about $65–130.
   - Your plan runs at most 20 jobs at once on the Free plan.
2. **Upload this folder.** The workflow is shipped as `workflow_heilbronn.yml` because my tools cannot write into a `.github` folder on your PC; GitHub needs it at `.github/workflows/heilbronn.yml`.
   - Either run `push_to_github.ps1 -RepoUrl https://github.com/<you>/<repo>.git` (needs Git). It puts the workflow in the right place for you.
   - Or use the web page: "Add file › Upload files" for the other files, then "Add file › Create new file", name it `.github/workflows/heilbronn.yml`, and paste in the contents of `workflow_heilbronn.yml`.
3. **Validation run (n = 8, known answer, about an hour):** open Actions › heilbronn-certify › Run workflow, keep the defaults and start it.
   - This re-proves the published n = 8 result.
   - It also tells you how long parts take on GitHub's machines.
   - The "summary" job must end with **CERTIFIED**.
4. **Main run (n = 9):** start it again with these inputs:
   - n = `9`
   - target = `0.027426211734693878` (that is 43/1568 × 1.0001)
   - split = `[[2,3,4],[2,3,5],[2,3,6],[2,3,7],[2,3,8]]`
   - parts = `[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]`
   - hours = `5.5`
5. **Unresolved parts:** open the run's Summary page. For each unresolved part, copy the printed `prefix`, choose a new split (for example `[[0,3,4],[0,3,5],[1,2,4],[1,2,5]]`), and run the workflow again with that prefix, the new split and parts = all of 0..2^d−1. Set run_vertices = false for these reruns.
6. **Collect the results:** every run also commits its results to the branch `results`, under `results/run-<number>-n<n>/`. Check out that branch, or download the `summary` artifacts, and run `python summarize.py results` over all of them. It checks completeness across all runs.

**Using the laptop too.** `run_heilbronn_local.ps1` runs chosen parts on the laptop's CPU while its GPU does the Ramsey search. Remove those part numbers from the GitHub "parts" input so nothing runs twice.

## The Claude cloud session: coordinator, paid for by your cloud-session credits

- **Its role:** GitHub does the heavy solving for free. A Claude Code cloud session at claude.ai/code, running on this repository, does the rest:
  - checks the n = 8 validation;
  - starts or requests the n = 9 run;
  - independently re-checks a sample of parts;
  - refines unresolved parts, running some itself on its 4-core VM with `run_parts.sh`;
  - saves its own results to the branch `cloud-results`.
- **Its instructions:** the full prompt is in `CLOUD_SESSION_PROMPT.md`.
- **Keeping it alive:** the session must keep checking on its runs, because an idle cloud session is shut down and its running work is lost.

## What a CERTIFIED result means, and its limits

- **What it depends on:**
  - The certificate depends on the boundary-structure result (Proposition 1) of arXiv:2607.15021, which is recent and not yet peer-reviewed.
  - It also depends on the numerical global optimiser. Floating-point tolerances are about 10⁻⁶ absolute, and the target includes a 10⁻⁴ relative margin.
- **The precise claim:** Δ₉ ≤ (43/1568)(1 + 10⁻⁴). Combined with Cantrell's configuration, Δ₉ equals 43/1568 up to 10⁻⁴. That is exactly the standard used for the published n ≤ 8 certificates.
- **Before announcing it:**
  - Keep all logs.
  - Have a second person re-run a sample of parts.
  - Contact the organisers and the arXiv author.
- **Timing is uncertain:** in the paper, n = 7 → 8 took about 100 times longer (22.6 s → 2324 s). If n = 9 grows similarly, the whole proof could need tens of machine-hours, so it may not finish during the hackathon. Partial results (how many parts are proved) are still worth recording.
- **Licence:** the Gurobi licence that installs with `pip install gurobipy` is size-limited and marked "for non-production use only". The n = 9 model fits within the size limit. Check that your use qualifies; otherwise use a free academic Gurobi licence, or set solver = `scip` (free, but slower).
