import os
from pathlib import Path
from string import Template

from src.config import TEMPLATE_DIR
from src.ambertools.run_pmemd import run_pmemd

with open(TEMPLATE_DIR / "rand_template.txt") as f:
    rand_template = f.read()

with open(TEMPLATE_DIR / "prod_template.txt") as f:
    prod_template = f.read()

def prod_seeds(prmtop, mask, working_dir, cfg, n_eq_runs):
    # Make sure the folder exists and contains the necessary files
    if not os.path.exists(working_dir):
        os.makedirs(working_dir)

    # Load equilibration parameters from config file
    num_seeds: int = cfg["num_seeds"]
    temp: float = cfg["temp"]
    dt: float = cfg["dt"]
    rand_time: float = cfg["rand_time"] # in ps
    prod_time: float = cfg["prod_time"] # in ps
    prod_freq: float = cfg["prod_freq"] # in ps
    cut: float = cfg["cut"]
    
    # Substitute parameters into the randomization template
    nstlim = int((rand_time) / dt) # convert time from ps to steps
    ntpr = ntwx = ntwr = int(nstlim // 1000) # print/write frequencies (every 1000 steps)

    rand_input = Template(rand_template).substitute(
        dt=dt,
        temp=temp,
        cut=cut,
        nstlim=nstlim,
        ntpr=ntpr,
        ntwx=ntwx,
        ntwr=ntwr,
        mask=mask
    )

    # Substitute parameters into the production template
    nstlim = int((prod_time) / dt) # convert time from ps to steps
    ntpr = ntwx = ntwr = int(nstlim // prod_freq) # print/write frequencies (every 1000 steps)

    prod_input = Template(prod_template).substitute(
        dt=dt,
        temp=temp,
        cut=cut,
        nstlim=nstlim,
        ntpr=ntpr,
        ntwx=ntwx,
        ntwr=ntwr,
        mask=mask
    )
  
    for i in range(1, num_seeds + 1):
        '''Randomization takes the output coordinates of the last equilibration step and resets the velocities.
        The output coordinates are saved as rand{seed}.ncrst'''
        ncrst = Path(working_dir) / f"eq{n_eq_runs}.ncrst"
        run_pmemd(rand_input, prmtop, ncrst, working_dir, f"seed{i}")

        '''Production run takes the output coordinates of the last equilibration step and runs for a long time. 
        The output coordinates are saved as prod{seed}.ncrst'''
        ncrst = Path(working_dir) / f"seed{i}.ncrst"
        run_pmemd(prod_input, prmtop, ncrst, working_dir, f"prod{i}")

        print ("Finished full run with seed {i}")