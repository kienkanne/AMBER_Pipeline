#!/usr/bin/bash
set -euo pipefail

: "${AMBERHOME:?AMBERHOME environment variable not set}"

prmtop=${1:?Usage: prmtop file}
ncrst=${2:?Usage: eq_.ncrst file}
name="${prmtop%.prmtop}"
seed="1"
prefix="s${seed}_${name}"

: > "rand_${prefix}.log"

SECONDS=0
echo "Started at $(date)" >> "rand_${prefix}.log"

pmemd.cuda -O -i rand.in \
	-o "rand_${prefix}.out" \
	-p "$prmtop" \
	-c "$ncrst" \
	-ref "$ncrst" \
	-r "${prefix}_0.ncrst" \
	-x "rand_${prefix}.nc" >> "rand_${prefix}.log" 2>&1

#Create ${prefix}_0.ncrst to be consistent with the main run script

echo "Finished at $(date) | Duration: ${SECONDS}s" >> "rand_${prefix}.log"

