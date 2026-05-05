import os
import shutil
from pathlib import Path
from amber_pipeline.config_schema import RootConfig
from amber_pipeline.workflows.minimization import MinimizationWorkflow
from amber_pipeline.workflows.heating import HeatingWorkflow
from amber_pipeline.workflows.equilibration import EquilibrationWorkflow
from amber_pipeline.workflows.production import ProductionWorkflow
from amber_pipeline.utils.central_logging import setup_all_logs, central_run_stage

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

            name = os.path.basename(prmtop).split('.')[0]
            output_dir = Path(self.cfg.common.outputs_dir) / f"{name}_{self.pid}"
            output_dir.mkdir(parents=True, exist_ok=True)

            logs = setup_all_logs(
                "Dialanine_test",
                output_dir / "run.log",
                output_dir / "manifest.json",
                output_dir / "state.json"
            )

            min_wf = MinimizationWorkflow(self.cfg.minimization)
            last_min = central_run_stage(logs, "Minimization", min_wf.run, prmtop, inpcrd, wd)

            heat_wf = HeatingWorkflow(self.cfg.heating)
            last_heat = central_run_stage(logs, "Heating", heat_wf.run, prmtop, mask, wd, last_min)

            eq_wf = EquilibrationWorkflow(self.cfg.equilibration)
            last_eq = central_run_stage(logs, "Equilibration", eq_wf.run, prmtop, mask, wd, last_heat)

            prod_wf = ProductionWorkflow(self.cfg.production)
            central_run_stage(logs, "Production", prod_wf.run, prmtop, mask, wd, last_eq)
            
            # Copy selected files to outputs
            targeted_copy = ["*.out", "*.log", "*.json", "prod*.nc", "prod*.ncrst"]
            for target in targeted_copy:
                for file_path in wd.glob(f"{target}"):
                    shutil.copy2(file_path, output_dir)

            # Optionally clean up scratch
            if cleanup:
                shutil.rmtree(wd)
            
            (logger, manifest, state) = logs
            manifest.finalize(success=True)
            logger.info("Copied successfully. Pipeline completed")

            completed_run = output_dir.with_name(f"Success_{name}_{self.pid}")
            output_dir.rename(completed_run)

        return _run_all()
