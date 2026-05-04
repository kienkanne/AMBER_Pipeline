#!/usr/bin/bash
set -euo pipefail

: "${AMBERHOME:?AMBERHOME environment variable not set}"

: > heat_run.log

prmtop=${1:?Usage: prmtop file}
ncrst=${2:?Usage: min_.ncrst file}

SECONDS=0
echo "Heating started at $(date)" >> heat_run.log

pmemd.cuda -O -i heat.in -o heat.out -p "$prmtop" -c "$ncrst" -ref "$ncrst" -r heat.ncrst -x heat.nc

echo "Heating finished at $(date) | Duration: ${SECONDS}s" >> heat_run.log

done
