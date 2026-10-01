# Heilbronn n = 9 certification attempt: retired (1 Oct 2026)

Full path: `heilbronn-cloud-results/RETIREMENT_261001.md` in FSvOAI/heilbronn, branch `cloud-results`.

## Acronyms and abbreviations

| Term | Meaning |
|---|---|
| n | Number of points |
| T | The triangle x ≥ 0, y ≥ 0, x + y ≤ 1 |
| UTC | Coordinated Universal Time |
| VM | Virtual Machine (the cloud session's 4-core computer) |

## Decision

On 1 Oct 2026 at about 14:45 UTC the user asked to terminate and retire the project because of the compute cost. All work was stopped:

- VM refinement driver stopped (STOP file written, processes ended); hourly push loop stopped.
- Hourly health-check routine and the daily check-in deleted.
- GitHub Actions driver runs 2-13 cancelled (HTTP 202 for all 12). Runs that had finished regions saved them to the `results` branch before ending.
- Nothing was deleted: all results, branches and tools remain in FSvOAI/heilbronn.

## What was established

- n = 7 sanity check: CERTIFIED; n = 7 negative control (target below the optimum) correctly not certified.
- n = 8: CERTIFIED (GitHub run 1, 17 of 17 parts, 2.54 h solver time).
- n = 9: NOT CERTIFIED.
  - Corners case and 27 of the 32 boundary parts proved.
  - Parts 0, 8, 29, 30 and 31 (four of them contain Cantrell's configuration) only partly proved.
  - Final combiner run (14:59 UTC, 1 Oct): 246,553 n = 9 result rows kept, 227,104 PROVED, 19,449 UNRESOLVED; 3,110 open leaves (2,581 unresolved, 529 missing).
  - No configuration better than 43/1568 was found anywhere (no BETTER row for n = 9).
- Why it stopped converging: near Cantrell's value the solver's bounds shrink very slowly as regions are split, so the number of open regions grew with each refinement round (136, 205, 293, 1,957 GitHub regions), and the driver workflow needed about 2 h per region.

## Where everything is

- Status log: `heilbronn-cloud-results/STATUS_260928.md`.
- Final combiner report: `heilbronn-cloud-results/final_combine_report_261001.md`.
- GitHub results: FSvOAI/heilbronn branch `results` (`run-*`, `batch-*`, `driver-*` folders).
- VM results: `heilbronn-cloud-results/cc31/` and the other result folders on branch `cloud-results`.
- Tools: `heilbronn-cloud-results/tools/` and, in the repository, `.github/workflows/heilbronn-batch.yml`, `.github/workflows/heilbronn-driver.yml`, `tools/split_until_proved.py`.
