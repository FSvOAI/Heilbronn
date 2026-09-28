for p in 5 19; do
  if [ "$p" = vertices ]; then
    python3 heil_tri.py --n 9 --case vertices --cutoff 0.027426211734693878 --threads $(nproc) --timelimit 19800 --out results/cloud/spot9_p5_p19/result_vertices_0.json > results/cloud/spot9_p5_p19/log_vertices.txt 2>&1
  else
    python3 heil_tri.py --n 9 --case boundary --cutoff 0.027426211734693878 --split '[[2,3,4],[2,3,5],[2,3,6],[2,3,7],[2,3,8]]' --part $p --prefix '[]' --threads $(nproc) --timelimit 19800 --out results/cloud/spot9_p5_p19/result_boundary_$p.json > results/cloud/spot9_p5_p19/log_$p.txt 2>&1
  fi
done
echo ALL_DONE > results/cloud/spot9_p5_p19/DONE
