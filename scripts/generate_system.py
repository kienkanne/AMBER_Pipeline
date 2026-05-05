#!/usr/bin/env python3

from pathlib import Path
import sys

from src.config_schema import load_config
from src.workflows.system_generation import System_Generation

def main():
    cfg = load_config(Path(__file__).resolve().parents[1] / "configs" / "config.yaml")
    sg = System_Generation(cfg.tleap)
    sg.run()

if __name__ == "__main__":
    sys.exit(main())