#!/usr/bin/bash
set -euo pipefail

: "${AMBERHOME:?AMBERHOME environment variable not set}"

#Input ligand file
file="$1"
ftype="$2"
name="${file%.${ftype}}"

#Generate AM1-BCC charges to generate prepi file
antechamber -i "$file" -fi "$ftype" -o "${name}.prepi" -fo prepi -c bcc -s 2 -rn "$name" > antechamber.log 2>&1

#Generate missing force field parameters
parmchk2 -i "${name}.prepi" -f prepi -o "${name}.frcmod" > parmchk2.log 2>&1

echo "Parameterization completed"
