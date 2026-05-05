#!/usr/bin/bash
set -euo pipefail

: "${AMBERHOME:?AMBERHOME environment variable not set}"

N=${1:?Usage: $0 <number_of_min_steps>}
prmtop=${2:?Usage: prmtop file}
inpcrd=${3:?Usage: inpcrd file}

: > min_run.log

SECONDS=0
echo "Step 1 started at $(date)" >> min_run.log

pmemd.cuda -O -i min1.in -o min1.out -p "$prmtop" -c "$inpcrd" -ref "$inpcrd" -r min1.ncrst -x min1.nc

echo "Step 1 finished at $(date) | Duration: ${SECONDS}s" >> min_run.log


for ((i=2; i<=N; i++)); do

SECONDS=0
echo "Step $i started at $(date)" >> min_run.log

pmemd.cuda -O -i min$i.in -o min$i.out -p "$prmtop" -c "min$((i-1)).ncrst" -ref "min$((i-1)).ncrst" -r min$i.ncrst -x min$i.nc

echo "Step $i finished at $(date) | Duration: ${SECONDS}s" >> min_run.log

done
