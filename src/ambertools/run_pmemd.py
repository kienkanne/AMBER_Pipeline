import os
import subprocess
from pathlib import Path
from src.utils.timing import timed

AMBERHOME = os.environ.get("AMBERHOME")
if not AMBERHOME:
    raise RuntimeError("AMBERHOME environment variable not set")

def run_pmemd(mdin, prmtop, inpcrd, working_dir, stepname):
    def _run():
        # Write the input file
        mdin_path = Path(working_dir) / f"{stepname}.in"
        mdin_path.write_text(mdin)

        # Paths for output files
        out = Path(working_dir) / f"{stepname}.out"
        ncrst = Path(working_dir) / f"{stepname}.ncrst"
        nc = Path(working_dir) / f"{stepname}.nc"
        mdinfo = Path(working_dir) / f"{stepname}.info"
        
        # Main pmemd.cuda command
        pmemd_cmd = [
        "pmemd.cuda",
        "-AllowSmallBox",
        "-O",
        "-i", str(mdin_path),
        "-o", str(out),
        "-p", str(prmtop),
        "-c", str(inpcrd),
        "-ref", str(inpcrd),
        "-r", str(ncrst),
        "-x", str(nc),
        "-inf", str(mdinfo)
        ]
        result = subprocess.run(pmemd_cmd, capture_output=True, text=True)

        if result.returncode != 0:
            print(f"PMEMD FAILED: {result.stdout}")
            print(f"STDOUT: {result.stdout}")
            print(f"STDERR: {result.stderr}")
        else:
            print("PMEMD SUCCESS")
    # Track time
    return timed(stepname, _run)