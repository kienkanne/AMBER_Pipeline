from pathlib import Path
from string import Template

from amber_pipeline.ambertools.run_pmemd import run_pmemd

'''Randomization takes the output coordinates of the last equilibration step and resets the velocities.
The output coordinates are saved as rand{seed}.ncrst'''

'''Production run takes the output coordinates of the last equilibration step and runs for a long time. 
The output coordinates are saved as prod{seed}.ncrst'''

class ProductionWorkflow:
    def __init__(self, cfg):
        self.cfg = cfg

        with open(Path(__file__).resolve().parents[1] / "templates" / "rand_template.txt") as f:
            self.rand_template = f.read()

        with open(Path(__file__).resolve().parents[1] / "templates" / "prod_template.txt") as f:
            self.prod_template = f.read()

    def run(self, prmtop: Path, mask: str, working_dir: Path, last_eq_ncrst: Path) -> None:
        working_dir.mkdir(parents=True, exist_ok=True)

        num_seeds = self.cfg.num_seeds
        temp = self.cfg.temp
        dt = self.cfg.dt
        rand_time = self.cfg.rand_time
        prod_time = self.cfg.prod_time
        prod_freq = self.cfg.prod_freq
        cut = self.cfg.cut

        nstlim = int((rand_time) / dt)
        ntpr = ntwx = ntwr = int(nstlim // 1000) or 10000

        rand_input = Template(self.rand_template).substitute(
            dt=dt,
            temp=temp,
            cut=cut,
            nstlim=nstlim,
            ntpr=ntpr,
            ntwx=ntwx,
            ntwr=ntwr,
            mask=mask,
        )

        nstlim = int((prod_time) / dt)
        ntpr = ntwx = ntwr = int(nstlim // prod_freq) or 10000

        prod_input = Template(self.prod_template).substitute(
            dt=dt,
            temp=temp,
            cut=cut,
            nstlim=nstlim,
            ntpr=ntpr,
            ntwx=ntwx,
            ntwr=ntwr,
            mask=mask,
        )

        for i in range(1, num_seeds + 1):
            ncrst = last_eq_ncrst
            run_pmemd(rand_input, prmtop, ncrst, working_dir, f"seed{i}")

            ncrst = working_dir / f"seed{i}.ncrst"
            run_pmemd(prod_input, prmtop, ncrst, working_dir, f"prod{i}")

            print(f"Finished full run with seed {i}")