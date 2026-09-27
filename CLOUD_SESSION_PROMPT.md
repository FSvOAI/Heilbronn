# Prompt for the Claude cloud session (coordinator)

Paste everything between the lines into a new cloud session at claude.ai/code with the repository **FSvOAI/Claude** selected.

---

You are the coordinator of a computer-assisted proof attempt for Heilbronn's triangle problem with n = 9 points in the unit right triangle T = {x ≥ 0, y ≥ 0, x + y ≤ 1}. Everything is in this repository. Read `README_Heilbronn_GitHub_260927.md` first, then `heil_tri.py`, `summarize.py` and `run_parts.sh`.

**Goal.** Certify that no 9-point configuration in T has minimum triangle area above target = 0.027426211734693878, which is 43/1568 × (1 + 10⁻⁴). Cantrell's configuration (`cantrell_n9.txt`) attains exactly 43/1568, so a complete certificate proves it is optimal to within 10⁻⁴. The alternative outcome, a configuration above the target, would be a new record.

**Division of labour.**
- **GitHub Actions** (workflow `heilbronn-certify`, free on this public repository) does the heavy solving. It runs the 32 parts of the split on triangles (2,3,k), k = 4..8, plus the corners-occupied case. Each run's results are committed to the branch `results` under `results/run-<number>-n<n>/`.
- **You** coordinate and add compute on this VM (4 cores).

**Steps.**
1. **Set up and sanity check.** Run `pip install "gurobipy>=13,<14"` (add `--break-system-packages` if needed). Then run `bash run_parts.sh sanity7 7 0.04861597222222222 '[[2,3,4],[2,3,5],[2,3,6]]' '[]' 0.1 0 1 2 3 4 5 6 7 vertices`. Check that `python3 summarize.py results/cloud/sanity7` prints CERTIFIED; 7/144 is the known optimum for n = 7. Report the result to me.
2. **Check the n = 8 validation.** Run `git fetch origin results` and look for `results/run-*-n8/summary.md` on that branch. It must end with CERTIFIED, which reproduces a published result. If it is missing, try `gh run list --workflow heilbronn.yml`. If `gh` cannot reach Actions, ask me to look at the Actions tab. Tell me how long the n = 8 parts took; this is our timing calibration.
3. **Start n = 9.** Once n = 8 is certified, try `gh workflow run heilbronn.yml -f n=9 -f target=0.027426211734693878 -f split='[[2,3,4],[2,3,5],[2,3,6],[2,3,7],[2,3,8]]' -f parts='[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]' -f hours=5.5 -f run_vertices=true`. If you are not allowed to start workflows, give me these exact inputs to type into Actions › heilbronn-certify › Run workflow.
4. **While n = 9 runs, do an independent spot check.** When any n = 9 parts finish on GitHub, re-run two parts that GitHub reports as PROVED here with `run_parts.sh` and confirm that you get the same verdict.
5. **Refine unresolved parts.** When the n = 9 results arrive, run `summarize.py` over all n = 9 results together, from GitHub and from this VM. For each UNRESOLVED part, take the printed prefix and choose a new split of 3–4 triangles not already fixed, for example (0,3,k), (1,2,k), (0,2,k) or (1,3,k) with free points k. Run the easiest few of these sub-parts here with `run_parts.sh`. Give me, or start with `gh`, the workflow inputs for the rest; set run_vertices = false for refinements.
6. **Keep this session alive and save work.** Solver runs take hours. Check progress about every 10 minutes with short commands, and never make one command wait longer than 10 minutes. Commit your `results/cloud/` files to a branch named `cloud-results` and push after every finished part, so nothing is lost if this VM is reclaimed.
7. **Report after each milestone:** parts proved, unresolved and still running, and the total solver time. Never say "certified" unless `summarize.py` over the complete set of n = 9 results prints CERTIFIED. If any result says BETTER_CONFIGURATION_FOUND, verify the points exactly with `verify_config.py` before reporting it. The solver works in floating point, so a small excess can be round-off.

**Rules.**
- Do not change the mathematics in `heil_tri.py` or the target.
- Do not force-push, delete branches or delete results.
- Ask me before anything that costs money or changes repository settings.

---
