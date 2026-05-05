#!/usr/bin/bash
set -euo pipefail

: "${AMBERHOME:?AMBERHOME environment variable not set}"
: "${SCHRODINGER:?SCHRODINGER environment variable not set}"

# Input PDB file from command line
pdb="$1"

# Convert PDB file into XYZ file
xyz="${pdb%.pdb}.xyz"
$SCHRODINGER/utilities/obabel -i pdb "$pdb" -o xyz -O "$xyz" -h > obabel.log 2>&1

# Output Gaussian input file
gfile="${xyz%.xyz}.gjf"

# Prompt user for Gaussian options
read -p "Enter charge: " charge
read -p "Enter multiplicity: " mult

# Gaussian header
cat << EOF > "$gfile"
%chk=${xyz%.xyz}.chk
%nprocshared=8
%mem=8GB
#P HF/6-31G* 
# Gfinput IOP(6/7=3) iop(6/33=2) iop(6/42=6) iop(6/50=1) Pop=full Pop=SaveESP Pop=MK Density Test SCF=QC 
# Units(Ang,Deg) 

Generated from $xyz

$charge $mult
EOF

# Append coordinates (skip first 2 lines of XYZ)
tail -n +3 "$xyz" >> "$gfile"

# End with blank line (required)
echo "" >> "$gfile"


echo "Generated Gaussian input file: $gfile"
echo "Review, then run:"
echo "nohup g16 $gfile > ${gfile%.gjf}.log &"
