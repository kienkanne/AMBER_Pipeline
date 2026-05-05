import os
from pathlib import Path
from src.config_schema import RootConfig
from src.workflows.minimization import MinimizationWorkflow
from src.workflows.heating import HeatingWorkflow
from src.workflows.equilibration import EquilibrationWorkflow
from src.workflows.production_seeds import ProductionWorkflow
from src.utils.timing import timed

class Orchestrator:
    def __init__(self, cfg: RootConfig, job_id: str = None):
        self.cfg = cfg
        self.job_id = job_id or os.environ.get(cfg.common.job_id_env, "local")

    def _working_dir(self) -> Path:
        return Path(self.cfg.common.scratch_dir) / f"Job_{self.job_id}"

    def run(self) -> None:
        wd = self._working_dir()
        wd.mkdir(parents=True, exist_ok=True)

        def _run_all():
            prmtop = Path(self.cfg.common.prmtop)
            inpcrd = Path(self.cfg.common.inpcrd)
            mask = Path(self.cfg.common.mask)

            # Minimization
            min_wf = MinimizationWorkflow(self.cfg.minimization)
            last_min = min_wf.run(prmtop, inpcrd, wd)

            # Heating
            heat_wf = HeatingWorkflow(self.cfg.heating)
            heat_wf.run(prmtop, mask, wd, last_min)

            # Equilibration
            eq_wf = EquilibrationWorkflow(self.cfg.equilibration)
            last_eq = eq_wf.run(prmtop, mask, wd)

            # Production
            prod_wf = ProductionWorkflow(self.cfg.production)
            prod_wf.run(prmtop, mask, wd, last_eq)

        return timed("Orchestrator.run", _run_all)
