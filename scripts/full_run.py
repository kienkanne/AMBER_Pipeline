#!/usr/bin/env python3

from pathlib import Path
import sys

from amber_pipeline.config_schema import load_config
from amber_pipeline.orchestrator import Orchestrator

def main():
    cfg = load_config(Path(__file__).resolve().parents[1] / "configs" / "config.yaml")
    orch = Orchestrator(cfg)
    orch.run()

if __name__ == "__main__":
    sys.exit(main())
