import os
import subprocess
from pathlib import Path
from amber_pipeline.utils.timing import timed

AMBERHOME = os.environ.get("AMBERHOME")
if not AMBERHOME:
    raise RuntimeError("AMBERHOME environment variable not set")

def run_pmemd(mdin, prmtop, inpcrd, working_dir, stepname):
    def _run():

        mdin_path = Path(working_dir) / f"{stepname}.in"
        mdin_path.write_text(mdin)

        out = Path(working_dir) / f"{stepname}.out"
        ncrst = Path(working_dir) / f"{stepname}.ncrst"
        nc = Path(working_dir) / f"{stepname}.nc"
        mdinfo = Path(working_dir) / f"{stepname}.info"
        
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
        result = subprocess.run(pmemd_cmd, capture_output=True, text=True, check=True)

        stdout = working_dir / f"stdout_{stepname}.log"
        stderr = working_dir / f"stderr_{stepname}.log"

        for path, txt in [(stdout, result.stdout), (stderr, result.stderr)]:
            if txt is not None:
                with open (path, "w") as file:
                    file.write(txt)

        if result.returncode != 0:
            raise RuntimeError(f"pmemd failed step={stepname}: {result.stderr}\n{result.stdout}")
        else:
            print("PMEMD SUCCESS")
    # Track time per step
    return timed(stepname, _run)