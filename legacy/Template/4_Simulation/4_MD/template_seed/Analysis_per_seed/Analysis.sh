#!/bin/bash

: "${AMBERHOME:?AMBERHOME environment variable not set}"

prmtop=${1:?Usage: $0 <prmtop file>}
trajin=${2:?Usage: $0 <combined trajectory file>}
name=${3:?Usage: $0 <system suffix>}
mask="__MASK__"
seed="__SEED__"

suffix="${name}_s${seed}"

cpptraj > analysis_log.txt 2>&1 << EOF

# Input topology and trajectory
parm $prmtop
trajin $trajin

# RMS analysis
rmsd first ${mask}@CA out rmsd_${suffix}.out
atomicfluct out rmsf_bb_${suffix}.dat @CA,C,N byres

# Hydrogen bonds analysis
# --- Protein–Protein hydrogen bonds ---
hbond ProtProt $mask out PP_hbvtime_${suffix}.dat avgout PP_avg_${suffix}.dat

# --- Protein–Water hydrogen bonds ---
hbond All $mask solventdonor :WAT solventacceptor :WAT@O out All_hbvtime_${suffix}.dat solvout PW_avg_${suffix}.dat bridgeout Bridge_avg_${suffix}.dat

# --- Backbone-only protein hydrogen bonds ---
hbond BB_Prot ${mask}@C,O,N,H avgout BB_avg_${suffix}.dat series uuseries BB_series_${suffix}.dat

# --- Create time-series counts ---
create PW_hbvtime_${suffix}.dat All[UV]
create Bridge_hbvtime_${suffix}.dat All[Bridge]
create BB_hbvtime_${suffix}.dat BB_Prot[UU]

# Secondary structure analysis
secstruct out ss_per_res_${suffix}.dat sumout summary_ss_${suffix}.dat totalout total_${suffix}.out

run
quit

EOF

echo "Analysis completed"
