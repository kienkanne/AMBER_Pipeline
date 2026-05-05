#!/bin/bash

: "${AMBERHOME:?AMBERHOME environment variable not set}"

N=${1:?Usage: $0 <number of trajectories>}
TOPO=${2:?Usage: $0 <prmtop file>}
name=${3:?Usage: $0 <complex name>}
mask="__MASK__"
seed="__SEED__"

prefix="${name}_s${seed}"

OUTTRAJ="MD_s${seed}.nc"
INPUT="combine_trajectories.in"

# Remove old input if it exists
rm -f $INPUT

# Write topology line
echo "parm $TOPO" >> $INPUT

# Add trajectories in numeric order
for i in $(seq 1 $N)
do
    if [ -f "${prefix}_${i}.nc" ]; then
        echo "trajin ${prefix}_${i}.nc" >> $INPUT
    fi
done

# Align and center frames
echo "autoimage" >> $INPUT
echo "rms first $mask" >> $INPUT

# Write output trajectory
echo "trajout $OUTTRAJ netcdf" >> $INPUT
echo "run" >> $INPUT

# Run cpptraj
cpptraj -i $INPUT

echo "Combined trajectory written to $OUTTRAJ"
