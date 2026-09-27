# Optional: run some Heilbronn parts on this PC's CPU (Intel Core Ultra 9, 24 cores) alongside GitHub.
# Usage (from any folder):
#   powershell -ExecutionPolicy Bypass -File "C:\Users\fsvo\OneDrive\Documents\Claude\Projects\Six Hills + The Week 100\Heilbronn_GitHub_260927\run_heilbronn_local.ps1" -N 9 -Parts "24,25,26,27,28,29,30,31"
# Tell GitHub NOT to run the same parts (edit the "parts" input there) so no compute is wasted.
param(
    [int]$N = 9,
    [string]$Target = "0.027426211734693878",
    [string]$Split = "[[2,3,4],[2,3,5],[2,3,6],[2,3,7],[2,3,8]]",
    [string]$Parts = "31",
    [string]$Prefix = "[]",
    [int]$Threads = 8,
    [double]$Hours = 10,
    [switch]$Vertices
)
# Always work in the folder that contains this script
Set-Location -Path $PSScriptRoot
# Python/pip print normal messages on stderr; do not treat those as fatal
$ErrorActionPreference = "Continue"
Write-Host "Working folder: $PSScriptRoot"
$pyCmd = $null; $pyArgs = @()
if (Get-Command py -ErrorAction SilentlyContinue) { $pyCmd = "py"; $pyArgs = @("-3") }
elseif (Get-Command python -ErrorAction SilentlyContinue) { $pyCmd = "python" }
else { Write-Host "Python not found. Install 64-bit Python 3.12 from https://www.python.org/downloads/ and re-run."; exit 1 }
if (-not (Test-Path ".venv\Scripts\python.exe")) { & $pyCmd @pyArgs -m venv .venv }
$vpy = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
& $vpy -m pip install --upgrade pip --quiet --disable-pip-version-check 2>&1 | Out-Host
& $vpy -m pip install "gurobipy>=13,<14" --quiet --disable-pip-version-check 2>&1 | Out-Host
if ($LASTEXITCODE -ne 0) { Write-Host "gurobipy installation failed"; exit 1 }
New-Item -ItemType Directory -Force -Path "local_results" | Out-Null
$secs = [int]($Hours * 3600)
if ($Vertices) {
    & $vpy heil_tri.py --n $N --case vertices --cutoff $Target --threads $Threads --timelimit $secs --out "local_results\result_vertices_0.json"
}
foreach ($p in $Parts.Split(",")) {
    $p = $p.Trim()
    Write-Host "=== part $p ==="
    & $vpy heil_tri.py --n $N --case boundary --cutoff $Target --split $Split --part $p --prefix $Prefix --threads $Threads --timelimit $secs --out "local_results\result_boundary_$p.json"
}
& $vpy summarize.py local_results
