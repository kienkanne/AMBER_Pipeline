#!/usr/bin/bash
set -euo pipefail

: "${AMBERHOME:?AMBERHOME environment variable not set}"

#Input Gaussian log file
log="$1"
name="${log%.log}"

#Input ligand residue name
read -p "Enter residue name: " residue

#Fit RESP charges to generate mol2 file
antechamber -i "$log" -fi gout -o "${name}.mol2" -fo mol2 -c resp -s 2 -rn "$residue" > antechamber_mol2.log 2>&1

#Fit RESP charges to generate prepi file
antechamber -i "$log" -fi gout -o "${name}.prepi" -fo prepi -c resp -s 2 -rn "$residue" > antechamber_prepi.log 2>&1

#Generate missing force field parameters
parmchk2 -i "${name}.mol2" -f mol2 -o "${name}.frcmod" > parmchk2.log 2>&1

echo "Parameterization completed"
