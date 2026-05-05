import subprocess
import os

AMBERHOME = os.environ.get("AMBERHOME")
if not AMBERHOME:
    raise RuntimeError("AMBERHOME environment variable not set")

def run_cpptraj(input_file):

    cpptraj_cmd = ["cpptraj", "-i", input_file]
    result = subprocess.run(cpptraj_cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"CPPTRAJ FAILED: {result.stderr}")
    else:
        print("CPPTRAJ SUCCESS")