#!/usr/bin/bash

set -euo pipefail

: "${AMBERHOME:?AMBERHOME environment variable not set}"

# Set i-o variables
input="$1"
output="system.pdb"

# Clean the PDB file to make AMBER-compatiable
pdb4amber -i "$input" -o "$output" --reduce > pdb4amber.log 2>&1

# Separates the components of the output file
grep "^ATOM" "$output" > protein.pdb
grep "^HETATM" "$output" | grep -v "HOH" > ligand.pdb
grep "HOH" "$output" > water.pdb

echo "Cleaning completed"
