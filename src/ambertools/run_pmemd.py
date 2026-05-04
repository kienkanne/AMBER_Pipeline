import os
import subprocess

def run_pmemd(mdin, prmtop, inpcrd, stepname):
    filename = os.path.basename(prmtop)
    name = filename.split('.')[0]  
    # Run pmemd command
    pmemd_cmd = f"pmemd -O -i {mdin} -o {stepname}.out -p {prmtop} -c {inpcrd} \
        -r {stepname}.ncrst -ref {stepname}.ncrst -x {stepname}.nc"
    result = subprocess.run(pmemd_cmd, capture_output=True, text=True, shell=True)

    if result.returncode != 0:
        print(f"PMEMD FAILED: {result.stderr}")
    else:
        print("PMEMD SUCCESS")