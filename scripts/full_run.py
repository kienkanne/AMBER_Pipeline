import os
from pathlib import Path

from src.config import DATA_DIR, OUTPUTS_DIR, CONFIGS_DIR, SCRATCH_DIR
from configs.config_loader import load_config
from src.workflows.minimization import minimize
from src.workflows.heating import heat
from src.workflows.equilibration import equilibrate
from src.workflows.production_seeds import prod_seeds
from src.utils.timing import timed
def full_run():
    def _run():
        # Test inputs
        prmtop = Path(DATA_DIR) / "ALA.prmtop"
        inpcrd = Path(DATA_DIR) / "ALA_001.ncrst"
        mask = ":1-3"

        JOB_ID = os.environ.get("JOB_ID", "test1")
        working_dir = Path(SCRATCH_DIR) / f"Job_{JOB_ID}"

        # Minimization
        cfg_min = load_config(CONFIGS_DIR / "minimization_inputs.yaml")
        minimize(prmtop, inpcrd, working_dir, cfg_min)

        # Find the number of minimization steps to determine which output to use as the input for heating
        n_min_runs = cfg_min["n_min_runs"]

        # Heating
        cfg_heat = load_config(CONFIGS_DIR / "heating_inputs.yaml")
        heat(prmtop, mask, working_dir, cfg_heat, n_min_runs)

        # Equilibration
        cfg_eq = load_config(CONFIGS_DIR / "equilibration_inputs.yaml")
        equilibrate(prmtop, mask, working_dir, cfg_eq)

        # Find the number of equilibration steps to determine which output to use as the input for randomization
        n_eq_runs = cfg_eq["n_eq_runs"]
        # Production with multiple seeds

        cfg_prod = load_config(CONFIGS_DIR / "prod_run_inputs.yaml")
        prod_seeds(prmtop, mask, working_dir, cfg_prod, n_eq_runs)

        # Copy necessary files only to output
        ### =================================

        print ("Completed")
    # Track time
    return timed("Full_run", _run)

if __name__ == "__main__":
    full_run()

