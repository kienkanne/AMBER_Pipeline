import os
from string import Template
from pathlib import Path

from src.config import TEMPLATE_DIR
from src.ambertools.run_pmemd import run_pmemd

with open(TEMPLATE_DIR / "min_template.txt") as f:
    min_template = f.read()

def minimize(prmtop, inpcrd, working_dir, cfg):
    # Load minimization parameters from config file
    n_min_runs: int = cfg["n_min_runs"]
    ncyc: int = cfg["ncyc"]
    maxcyc: int = cfg["maxcyc"]
    cut: float = cfg["cut"]
    restraint: list = cfg["restraint"]

    # Make sure the folder exists and contains the necessary files
    if not os.path.exists(working_dir):
        os.makedirs(working_dir)

    ''' Minimization n runs. 
    The first run takes the input coordinates.
    Each subsequent run takes the output coordinates of the previous run. 
    The output coordinates are saved as min{run}.ncrst'''

    for run in range(1, n_min_runs + 1):
        # Substitute parameters into the minimization template
        min_input = Template(min_template).substitute(
            ncyc=ncyc,
            maxcyc=maxcyc,
            cut=cut,
            restraint=restraint[run - 1],
        )
        if run == 1:
            run_pmemd(min_input, prmtop, inpcrd, working_dir, "min1")
        else:
            ncrst = Path(working_dir) / f"min{run - 1}.ncrst"
            run_pmemd(min_input, prmtop, ncrst, working_dir, f"min{run}")

    print ("Minimization completed")