#!/usr/bin/env bash
# Run Heilbronn parts in the background on this machine (e.g. a Claude cloud session VM, 4 cores).
# Usage:
#   bash run_parts.sh <label> <n> <target> '<split-json>' '<prefix-json>' <hours> <part> [<part> ...]
#   use the word "vertices" as a part to run the corners-occupied case.
# Example:
#   bash run_parts.sh check9 9 0.027426211734693878 '[[2,3,4],[2,3,5],[2,3,6],[2,3,7],[2,3,8]]' '[]' 3 5 17
# Results: results/cloud/<label>/result_*.json, logs log_*.txt, and a DONE file when all parts finished.
set -e
cd "$(dirname "$0")"
label=$1; n=$2; target=$3; split=$4; prefix=$5; hours=$6; shift 6
out="results/cloud/$label"; mkdir -p "$out"
python3 -c "import gurobipy" 2>/dev/null || python3 -m pip install -q "gurobipy>=13,<14" || python3 -m pip install -q --break-system-packages "gurobipy>=13,<14"
secs=$(python3 -c "print(int(float('$hours')*3600))")
cat > "$out/job.sh" <<JOB
for p in $*; do
  if [ "\$p" = vertices ]; then
    python3 heil_tri.py --n $n --case vertices --cutoff $target --threads \$(nproc) --timelimit $secs --out $out/result_vertices_0.json > $out/log_vertices.txt 2>&1
  else
    python3 heil_tri.py --n $n --case boundary --cutoff $target --split '$split' --part \$p --prefix '$prefix' --threads \$(nproc) --timelimit $secs --out $out/result_boundary_\$p.json > $out/log_\$p.txt 2>&1
  fi
done
echo ALL_DONE > $out/DONE
JOB
nohup bash "$out/job.sh" > /dev/null 2>&1 &
echo "Started in background (pid $!). Progress: ls $out ; tail -n 2 $out/log_*.txt ; python3 summarize.py $out"
