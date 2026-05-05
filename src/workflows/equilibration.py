import os
from string import Template
from pathlib import Path

from src.config import TEMPLATE_DIR
from src.ambertools.run_pmemd import run_pmemd

with open(TEMPLATE_DIR / "eq_template.txt") as f:
    eq_template = f.read()

def equilibrate(prmtop, mask, working_dir, cfg):
    # Load equilibration parameters from config file
    n_eq_runs: int = cfg["n_eq_runs"]
    dt: float = cfg["dt"]
    temp: float = cfg["temp"]
    eq_time: float = cfg["eq_time"] # in ps
    cut: float = cfg["cut"]
    restraint: list = cfg["restraint"]

    # Calculate variables for equilibration input template
    nstlim = int((eq_time) / dt) # convert time from ps to steps
    ntpr = ntwx = ntwr = int(nstlim // 1000) # print/write frequencies (every 1000 steps)

    # Make sure the folder exists and contains the necessary files
    if not os.path.exists(working_dir):
        os.makedirs(working_dir)

    '''Equilibration n runs.
    The first run takes the output coordinates of the heating run.
    Each subsequent run takes the output coordinates of the previous run.
    The output coordinates are saved as eq{run}.ncrst'''

    for run in range(1, n_eq_runs + 1):
        # Substitute parameters into the equilibration template
        eq_input = Template(eq_template).substitute(
            dt=dt,
            temp=temp,
            cut=cut,
            restraint=restraint[run - 1],
            nstlim=nstlim,
            ntpr=ntpr,
            ntwx=ntwx,
            ntwr=ntwr,
            mask=mask
        )
        if run == 1:
            ncrst = Path(working_dir) / f"heat.ncrst"
            run_pmemd(eq_input, prmtop, ncrst, working_dir, f"eq{run}")
        else:
            ncrst = Path(working_dir) / f"eq{run - 1}.ncrst"
            run_pmemd(eq_input, prmtop, ncrst, working_dir, f"eq{run}")

    print ("Equilibration completed")