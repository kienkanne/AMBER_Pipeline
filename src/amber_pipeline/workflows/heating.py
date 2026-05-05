from string import Template
from pathlib import Path

from amber_pipeline.ambertools.run_pmemd import run_pmemd

# Load template
with open(Path(__file__).resolve().parents[1] / "templates" / "heat_template.txt") as f:
    heat_template = f.read()

'''Heating takes the output coordinates of the last minimization step.
There is only 1 heating step, so the output coordinates are saved as heat.ncrst'''

class HeatingWorkflow:
    def __init__(self, cfg):
        self.cfg = cfg

    def run(self, prmtop: Path, mask: str, working_dir: Path, last_min_ncrst: Path):
        working_dir.mkdir(parents=True, exist_ok=True)

        dt = self.cfg.dt
        temp1 = self.cfg.temp1
        temp2 = self.cfg.temp2
        heat_time1 = self.cfg.heat_time1
        heat_time2 = self.cfg.heat_time2
        total_heat_time = self.cfg.total_heat_time
        cut = self.cfg.cut
        restraint = self.cfg.restraint

        nstlim = int((total_heat_time) / dt)
        ntpr = ntwx = ntwr = int(nstlim // 1000) or 10000

        heat_input = Template(heat_template).substitute(
            dt=dt,
            temp1=temp1,
            temp2=temp2,
            heat_time1=heat_time1,
            heat_time2=heat_time2,
            cut=cut,
            restraint=restraint,
            nstlim=nstlim,
            ntpr=ntpr,
            ntwx=ntwx,
            ntwr=ntwr,
            istep1=int((heat_time1) / dt),
            istep2=int((heat_time2) / dt),
            mask=mask,
        )

        run_pmemd(heat_input, prmtop, last_min_ncrst, working_dir, "heat")

        return working_dir / "heat.ncrst"