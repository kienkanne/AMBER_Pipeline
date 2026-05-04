#!/bin/bash

for N in 2 3 4 5 6 8 10
do

cpptraj << EOF

parm ../prmtop
trajin ../md_all.nc
strip :Na+,Cl-,WAT

cluster c1 \
 kmeans clusters $N randompoint maxit 500 \
 rms :1-198@C,N,O,CA,CB \
 sieve 10 random \
 out cnumvtime${N}.dat \
 summary summary${N}.dat \
 info info${N}.dat \
 cpopvtime cpopvtime${N}.agr normframe \
 repout rep${N} repfmt pdb \
 singlerepout singlerep${N}.nc singlerepfmt netcdf \
 avgout avg${N} avgfmt pdb

run

EOF

done
