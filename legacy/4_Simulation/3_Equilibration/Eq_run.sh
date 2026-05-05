#!/usr/bin/bash
set -euo pipefail

: "${AMBERHOME:?AMBERHOME environment variable not set}"

N=${1:?Usage: $0 <number_of_eq_steps>}
prmtop=${2:?Usage: prmtop file}
ncrst=${3:?Usage: heat.ncrst file}

: > eq_run.log

SECONDS=0
echo "Step 1 started at $(date)" >> eq_run.log

pmemd.cuda -O -i eq1.in -o eq1.out -p "$prmtop" -c "$ncrst" -ref "$ncrst" -r eq1.ncrst -x eq1.nc

echo "Step 1 finished at $(date) | Duration: ${SECONDS}s" >> eq_run.log


for ((i=2; i<=N; i++)); do

SECONDS=0
echo "Step $i started at $(date)" >> eq_run.log

pmemd.cuda -O -i eq$i.in -o eq$i.out -p "$prmtop" -c "eq$((i-1)).ncrst" -ref "eq$((i-1)).ncrst" -r eq$i.ncrst -x eq$i.nc

echo "Step $i finished at $(date) | Duration: ${SECONDS}s" >> eq_run.log

done
