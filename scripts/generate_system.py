#!/usr/bin/env python3

from pathlib import Path
import sys

from amber_pipeline.config_schema import load_config
from amber_pipeline.system_generation import SystemGeneration

def main():
    cfg = load_config(Path(__file__).resolve().parents[1] / "configs" / "config.yaml")
    sg = SystemGeneration(cfg.tleap)
    sg.run()

if __name__ == "__main__":
    sys.exit(main())