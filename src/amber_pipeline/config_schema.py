from pydantic import BaseModel
from typing import List, Optional
from pathlib import Path

class CommonConfig(BaseModel):
    prmtop: Path
    inpcrd: Path
    mask: str
    outputs_dir: str
    scratch_dir: str
    job_id_env: Optional[str] = "JOB_ID"

class TleapConfig(BaseModel):
    protein_pdb: Path
    working_dir: Path
    forcefield: str
    water_model: str
    box_type: str
    box_size: float

class MinimizationConfig(BaseModel):
    n_min_runs: int
    ncyc: int
    maxcyc: int
    cut: float
    restraint: List[float]

class HeatingConfig(BaseModel):
    dt: float
    temp1: float
    heat_time1: float
    temp2: float
    heat_time2: float
    total_heat_time: float
    cut: float
    restraint: float

class EquilibrationConfig(BaseModel):
    n_eq_runs: int
    dt: float
    temp: float
    eq_time: float
    cut: float
    restraint: List[float]

class ProductionConfig(BaseModel):
    num_seeds: int
    temp: float
    dt: float
    rand_time: float
    prod_time: float
    prod_freq: float
    cut: float

class RootConfig(BaseModel):
    common: CommonConfig
    tleap: TleapConfig
    minimization: MinimizationConfig
    heating: HeatingConfig
    equilibration: EquilibrationConfig
    production: ProductionConfig

def load_config(path):
    import yaml
    with open(path) as f:
        data = yaml.safe_load(open(path))
    return RootConfig.model_validate(data)
