import subprocess
import os

AMBERHOME = os.environ.get("AMBERHOME")
if not AMBERHOME:
    raise RuntimeError("AMBERHOME environment variable not set")

def run_pdb4amber(input):
    filename = os.path.basename(input)
    name = filename.split('.')[0]
    # Run pdb4amber command, adding hydrogens with --reduce and skipping water molecules with --dry
    pdb4amber_cmd = f"pdb4amber -i {input} -o {name}.processed.pdb --reduce --dry"
    result = subprocess.run(pdb4amber_cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"PDB4AMBER FAILED: {result.stderr}")
    else:
        print("PDB4AMBER SUCCESS")