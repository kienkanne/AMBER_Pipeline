import subprocess
import os
import re
from string import Template

from src.config import TEMPLATE_DIR

AMBERHOME = os.environ.get("AMBERHOME")
if not AMBERHOME:
    raise RuntimeError("AMBERHOME environment variable not set")

with open(TEMPLATE_DIR / "tleap_template.txt") as f:
    tleap_template = f.read()

# Volume parsing function to calculate number of ions for 0.15 M solution
def parse_volume(tleap_output):
    match = re.search(r"Volume:\s+([\d.]+)\s+A\^3", tleap_output)
    if not match:
        raise ValueError("Volume not found in tleap output")
    return float(match.group(1))

# Run tleap twice: first to get volume and calculate ions, then with ions
def run_tleap(protein_pdb, cfg):
    # Extract parameters from config
    forcefield = cfg["forcefield"]
    water_model = cfg["water_model"]
    box_type = cfg["box_type"]
    box_size = cfg["box_size"]

    # Extract the base name of the protein PDB file without extension
    filename = os.path.basename(protein_pdb)
    name = filename.split('.')[0]   

    # Substitute parameters into the tleap template
    tleap_input = Template(tleap_template).substitute(
        protein_pdb=protein_pdb,
        forcefield=forcefield,
        water_model=water_model,
        box_model_solvate=f"solvate{box_type}",
        water_model_box=f"{water_model.upper()}BOX",
        box_size=box_size,
        name=name,
        n_ions=0  # Placeholder, will be updated after parsing volume
    )

    # Run tleap command
    print (f"Running TLEAP with input:\n{tleap_input}")
    result = subprocess.run(
        ["tleap", "-f", "-"],
        input=tleap_input,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print("TLEAP FAILED")
        print("STDOUT:\n", result.stdout)
        print("STDERR:\n", result.stderr)
    else:
        print("TLEAP NO IONS SUCCESS")

    # Calculate ions based on volume from tleap output
    volume_A3 = parse_volume(result.stdout)
    volume_L = volume_A3 * 1e-27
    N_pairs = 0.15 * 6.022e23 * volume_L
    n_ions = round(N_pairs)

    # Rerun tleap with the calculated number of ions
    tleap_input_with_ions = Template(tleap_template).substitute(
        protein_pdb=protein_pdb,
        forcefield=forcefield,
        water_model=water_model,
        box_model_solvate=f"solvate{box_type}",
        water_model_box=f"{water_model.upper()}BOX",
        box_size=box_size,
        name=name,
        n_ions=n_ions
    )

    result_with_ions = subprocess.run(
        ["tleap", "-f", "-"],
        input=tleap_input_with_ions,
        capture_output=True,
        text=True
    )

    if result_with_ions.returncode != 0:
        print("TLEAP FAILED")
        print("STDOUT:\n", result_with_ions.stdout)
        print("STDERR:\n", result_with_ions.stderr)
    else:
        print("TLEAP WITH IONS SUCCESS")