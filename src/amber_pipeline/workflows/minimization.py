import os
from string import Template
from pathlib import Path

from amber_pipeline.ambertools.run_pmemd import run_pmemd

# Load template
with open(Path(__file__).resolve().parents[1] / "templates" / "min_template.txt") as f:
    min_template = f.read()

''' Minimization n runs. 
The first run takes the input coordinates.
Each subsequent run takes the output coordinates of the previous run. 
The output coordinates are saved as min{run}.ncrst'''

class MinimizationWorkflow:
    def __init__(self, cfg):
        self.cfg = cfg

    def run(self, prmtop: Path, inpcrd: Path, working_dir: Path) -> Path:
        working_dir.mkdir(parents=True, exist_ok=True)

        n_min_runs = self.cfg.n_min_runs
        ncyc = self.cfg.ncyc
        maxcyc = self.cfg.maxcyc
        cut = self.cfg.cut
        restraint = self.cfg.restraint

        last_ncrst = None
        for run in range(1, n_min_runs + 1):
            min_input = Template(min_template).substitute(
                ncyc=ncyc,
                maxcyc=maxcyc,
                cut=cut,
                restraint=restraint[run - 1],
            )
            if run == 1:
                run_pmemd(min_input, prmtop, inpcrd, working_dir, f"min{run}")
            else:
                ncrst = working_dir / f"min{run - 1}.ncrst"
                run_pmemd(min_input, prmtop, ncrst, working_dir, f"min{run}")
            last_ncrst = working_dir / f"min{run}.ncrst"

        return last_ncrst