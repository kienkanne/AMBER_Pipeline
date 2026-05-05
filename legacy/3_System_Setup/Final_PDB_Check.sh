#!/usr/bin/bash
set -euo pipefail

: "${AMBERHOME:?AMBERHOME environment variable not set}"

prmtop="$1"
inpcrd="$2"
name="${prmtop%.prmtop}"

# Generate a 0ns PDB of the simulation you're about to run. This is necessary to make sure tLeap ran properly. Always visualize your structure in Chimera or VMD before running MD. 
# Create cpptraj input file
cat > cpptraj.in << EOF

parm "$prmtop"
trajin "$inpcrd"

autoimage
trajout "${name}_solv.pdb"
go
EOF

cpptraj -i cpptraj.in > cpptraj.log

echo "Created ${name}_solv.pdb"
