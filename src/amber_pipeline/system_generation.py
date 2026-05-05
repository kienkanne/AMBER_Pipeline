import os
import re
from string import Template
from pathlib import Path

from amber_pipeline.ambertools.run_tleap import run_tleap

def parse_volume(tleap_output):
    match = re.search(r"Volume:\s+([\d.]+)\s+A\^3", tleap_output)
    if not match:
        raise ValueError("Volume not found in tleap output")
    return float(match.group(1))

class SystemGeneration():
    def __init__(self, cfg):
        self.cfg = cfg
        with open(Path(__file__).resolve().parents[0] / "templates" / "tleap_template.txt") as f:
            self.tleap_template = f.read()

    def run(self):
        protein_pdb = self.cfg.protein_pdb
        working_dir = self.cfg.working_dir

        filename = os.path.basename(protein_pdb)
        name = filename.split('.')[0]  

        forcefield = self.cfg.forcefield
        water_model = self.cfg.water_model
        box_type = self.cfg.box_type
        box_size = self.cfg.box_size

        tleap_input = Template(self.tleap_template).substitute(
            protein_pdb=protein_pdb,
            forcefield=forcefield,
            water_model=water_model,
            box_model_solvate=f"solvate{box_type}",
            water_model_box=f"{water_model.upper()}BOX",
            box_size=box_size,
            working_dir=working_dir,
            name=name,
            n_ions=0  # Placeholder, will be updated after parsing volume
        )

        stdout = run_tleap(tleap_input)

        # Calculate ions based on volume from tleap output
        volume_A3 = parse_volume(stdout)
        volume_L = volume_A3 * 1e-27
        N_pairs = 0.15 * 6.022e23 * volume_L
        n_ions = round(N_pairs)

        # Rerun tleap with the calculated number of ions
        tleap_input_with_ions = Template(self.tleap_template).substitute(
            protein_pdb=protein_pdb,
            forcefield=forcefield,
            water_model=water_model,
            box_model_solvate=f"solvate{box_type}",
            water_model_box=f"{water_model.upper()}BOX",
            box_size=box_size,
            working_dir=working_dir,
            name=name,
            n_ions=n_ions
        )

        run_tleap(tleap_input_with_ions)

        return True
        