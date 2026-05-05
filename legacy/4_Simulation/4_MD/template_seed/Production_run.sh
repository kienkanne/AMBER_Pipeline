#!/usr/bin/bash
set -euo pipefail

: "${AMBERHOME:?AMBERHOME environment variable not set}"

N=${1:?Usage: $0 <number_of_production_runs>}
prmtop=${2:?Usage: prmtop file}
name="${prmtop%.prmtop}"
seed="1"
prefix="s${seed}_${name}"

: > "run_$prefix.log"

for ((i=1; i<=N; i++)); do

if [[ -f "${prefix}_${i}.ncrst" ]]; then
	continue
fi

SECONDS=0
echo "Step $i started at $(date)" >> "run_$prefix.log"

pmemd.cuda -O -i md.in \
	-o "${prefix}_${i}.out" \
	-p "$prmtop" \
	-c "${prefix}_$((i-1)).ncrst" \
	-ref "${prefix}_$((i-1)).ncrst" \
	-r "${prefix}_${i}.ncrst" \
	-x "${prefix}_${i}.nc" >> "${prefix}.log" 2>&1

echo "Step $i finished at $(date) | Duration: ${SECONDS}s" >> "run_$prefix.log"

done
