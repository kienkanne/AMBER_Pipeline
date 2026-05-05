import os
import shutil
from pathlib import Path
from amber_pipeline.config_schema import RootConfig
from amber_pipeline.workflows.minimization import MinimizationWorkflow
from amber_pipeline.workflows.heating import HeatingWorkflow
from amber_pipeline.workflows.equilibration import EquilibrationWorkflow
from amber_pipeline.workflows.production import ProductionWorkflow
from amber_pipeline.utils.timing import timed
from amber_pipeline.utils.logging_utils import setup_logger
import logging

class Orchestrator:
    def __init__(self, cfg: RootConfig):
        self.cfg = cfg
        self.pid = os.getpid()
    def _working_dir(self) -> Path:
        return Path(self.cfg.common.scratch_dir) / f"Job_{self.pid}"

    def run(self, cleanup=True) -> None:
        wd = self._working_dir()
        wd.mkdir(parents=True, exist_ok=True)

        def _run_all():
            prmtop = Path(self.cfg.common.prmtop)
            inpcrd = Path(self.cfg.common.inpcrd)
            mask = str(self.cfg.common.mask)

            output_dir = Path(__file__).resolve().parents[2] / "outputs" / f"{name}_{self.pid}"
            output_dir.mkdir(parents=True, exist_ok=True)
            setup_logger(Path(output_dir) / "run.log")
            logger = logging.getLogger(__name__)

            logger.info("Starting pipeline")

            min_wf = MinimizationWorkflow(self.cfg.minimization)
            last_min = min_wf.run(prmtop, inpcrd, wd)
            logger.info("Minimization completed")

            heat_wf = HeatingWorkflow(self.cfg.heating)
            heat_wf.run(prmtop, mask, wd, last_min)
            logger.info("Heating completed")

            eq_wf = EquilibrationWorkflow(self.cfg.equilibration)
            last_eq = eq_wf.run(prmtop, mask, wd)
            logger.info("Equilibration completed")

            prod_wf = ProductionWorkflow(self.cfg.production)
            prod_wf.run(prmtop, mask, wd, last_eq)
            logger.info("Production completed")

            # Copy selected files to outputs
            name = os.path.basename(prmtop).split('.')[0]

            targeted_copy = ["*.out", "prod*.nc", "prod*.ncrst"]
            for target in targeted_copy:
                for file_path in wd.glob(f"{target}"):
                    shutil.copy2(file_path, output_dir)
                    
            # Optionally clean up scratch
            if cleanup:
                shutil.rmtree(wd)

        return timed("Orchestrator.run", _run_all)
