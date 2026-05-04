import subprocess

def run_pmemd(mdin, mdout, prmtop, inpcrd, ref, mdcrd):
    # Run pmemd command
    pmemd_cmd = f"pmemd -O -i {mdin} -o {mdout} -p {prmtop} -c {inpcrd} -r {ref} -x {mdcrd}"
    result = subprocess.run(pmemd_cmd, capture_output=True, text=True, shell=True)

    if result.returncode != 0:
        print(f"PMEMD FAILED: {result.stderr}")
    else:
        print("PMEMD SUCCESS")