import os
from string import Template
from pathlib import Path

from src.ambertools.run_pmemd import run_pmemd

# Load template
with open(Path(__file__).resolve().parents[1] / "templates" / "eq_template.txt") as f:
    eq_template = f.read()

'''Equilibration n runs.
The first run takes the output coordinates of the heating run.
Each subsequent run takes the output coordinates of the previous run.
The output coordinates are saved as eq{run}.ncrst'''

class EquilibrationWorkflow:
    def __init__(self, cfg):
        self.cfg = cfg

    def run(self, prmtop: Path, mask: str, working_dir: Path) -> Path:
        working_dir.mkdir(parents=True, exist_ok=True)

        n_eq_runs = self.cfg.n_eq_runs
        dt = self.cfg.dt
        temp = self.cfg.temp
        eq_time = self.cfg.eq_time
        cut = self.cfg.cut
        restraint = self.cfg.restraint

        nstlim = int((eq_time) / dt)
        ntpr = ntwx = ntwr = int(nstlim // 1000) or 1000

        last_ncrst = None
        for run in range(1, n_eq_runs + 1):
            eq_input = Template(eq_template).substitute(
                dt=dt,
                temp=temp,
                cut=cut,
                restraint=restraint[run - 1],
                nstlim=nstlim,
                ntpr=ntpr,
                ntwx=ntwx,
                ntwr=ntwr,
                mask=mask,
            )
            if run == 1:
                ncrst = working_dir / f"heat.ncrst"
                run_pmemd(eq_input, prmtop, ncrst, working_dir, f"eq{run}")
            else:
                ncrst = working_dir / f"eq{run - 1}.ncrst"
                run_pmemd(eq_input, prmtop, ncrst, working_dir, f"eq{run}")

            last_ncrst = working_dir / f"eq{run}.ncrst"

        return last_ncrst