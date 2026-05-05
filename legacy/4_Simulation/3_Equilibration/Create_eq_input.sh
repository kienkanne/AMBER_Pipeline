#!/usr/bin/bash
set -euo pipefail

#Prompt user
read -p "Enter number of equilibration steps: " N

for ((i=1; i<=N; i++)); do
cat << EOF > "eq$i.in"
Equilibration step $i
&cntrl 
 imin=0, irest=0, ntx=1, 
 ntpr=10000, ntwx=10000, ntwr=10000, nstlim=250000, 
 dt=0.002, ntt=3, tempi=300, 
 temp0=300, gamma_ln=1.0, ig=-1, 
 ntp=1, ntc=2, ntf=2, cut=9, 
 ntb=2, iwrap=1, ioutfm=1, 
 ntr=1, restraint_wt=10, restraintmask='__MASK__'
/
EOF
done

echo "Created $N equilibration input files"
