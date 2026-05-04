import os
from string import Template

from src.config import TEMPLATE_DIR
from src.ambertools.run_pmemd import run_pmemd
from configs.config_loader import load_config

with open(TEMPLATE_DIR / "heat_template.txt") as f:
    heat_template = f.read()

def heat(prmtop, mask, input_folder, cfg, minsteps):
    # Find the number of minimization steps from the config file to determine which minimization output to use as the input for heating

    # Load heating parameters from config file
    dt: float = cfg["dt"]
    temp1: float = cfg["temp1"]
    temp2: float = cfg["temp2"]
    heat_time1: float = cfg["heat_time1"] # in ps
    heat_time2: float = cfg["heat_time2"] # in ps
    total_heat_time: float = cfg["total_heat_time"] # in ps
    cut: float = cfg["cut"]
    restraint: float = cfg["restraint"] # only 1 step of heating, so only 1 restraint value

    # Calculate variables for heat input template
    nstlim = int((total_heat_time * 1000) / dt) # convert time from ps to steps
    ntpr, ntwx, ntwr = nstlim // 1000, nstlim // 1000, nstlim // 1000 # print/write frequencies (every 1000 steps)

    # Make sure the folder exists and contains the necessary files
    if not os.path.exists(input_folder):
        os.makedirs(input_folder)

    '''Heating takes the output coordinates of the last minimization step.
    There is only 1 heating step, so the output coordinates are saved as heat.ncrst'''

    heat_input = Template(heat_template).substitute(
        dt=dt,
        temp1=temp1,
        temp2=temp2,
        heat_time1=heat_time1,
        heat_time2=heat_time2,
        cut=cut,
        restraint=restraint[0],
        nstlim=nstlim,
        ntpr=ntpr,
        ntwx=ntwx,
        ntwr=ntwr,
        istep1=int((heat_time1 * 1000) / dt), # convert time from ps to steps
        istep2=int((heat_time2 * 1000) / dt), # convert time from ps to steps
        mask=mask
    )

    run_pmemd(heat_input, prmtop, f"{input_folder} / min{minsteps}.ncrst", "heat")

    print ("Heating completed")