import os

from src.ambertools import run_pmemd
from configs.config_loader import load_config

cfg = load_config("production_seeds_inputs.yaml")
eq_steps = cfg["eq_steps"]

prmtop = ""
num_seeds = 1 # number of times to repeat the full run with different random seeds from the last equilibration step
rand_in = ""
prod_in = ""

def minimize(input_folder):
    # Make sure the folder exists and contains the necessary files
    if not os.path.exists(input_folder):
        os.makedirs(input_folder)

    for i in range(1, num_seeds + 1):
        '''Randomization takes the output coordinates of the last equilibration step and resets the velocities.
        The output coordinates are saved as rand{seed}.ncrst'''
        run_pmemd(rand_in, prmtop, f"{input_folder} / eq{eq_steps}.ncrst", f"seed{i}")

        '''Production run takes the output coordinates of the last equilibration step and runs for a long time. 
        The output coordinates are saved as prod{seed}.ncrst'''
        run_pmemd(prod_in, prmtop, f"{input_folder} / seed{i}.ncrst", f"prod{i}")

        print ("Finished full run with seed {i}")