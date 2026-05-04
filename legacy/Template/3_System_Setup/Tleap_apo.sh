#!/usr/bin/bash
set -euo pipefail

: "${AMBERHOME:?AMBERHOME environment variable not set}"

pro="$1"
name="${pro%.pdb}"

# Create tleap input file
tleap -f - > tleap.log 2>&1 << EOF
# Load force fields
source leaprc.protein.ff19SB
source leaprc.water.tip3p

# Load protein
COM = loadpdb "$pro"

# Solvate system
solvateOct COM TIP3PBOX 12.0

# Add salt and neutralize the system. This is about 0.15M
addIonsRand COM Na+ 0
addIonsRand COM Cl- 0
addIonsRand COM Na+ 78 
addIonsRand COM Cl- 78

saveamberparm COM "${name}.prmtop" "${name}.inpcrd"
quit
EOF

echo "System created successfully"
