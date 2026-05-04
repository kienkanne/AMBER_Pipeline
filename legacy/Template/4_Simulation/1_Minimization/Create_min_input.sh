#!/usr/bin/bash
set -euo pipefail

#Prompt user
read -p "Enter number of minimization steps: " N

for ((i=1; i<=N; i++)); do
cat << EOF > "min$i.in"
Minimization step $i
&cntrl
  imin=1, 
  ncyc=1000, 
  maxcyc=5000, 
  ntpr=50, 
  cut=8, 
  iwrap=1, 
  ntr=1, 
  restraint_wt=5.0, 
  restraintmask='!@H=', 
/
EOF
done

echo "Created $N minimization input files"
