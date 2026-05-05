import argparse
from amber_pipeline.cli.common import add_config_arg
from amber_pipeline.config_schema import load_config

def main():
    parser = argparse.ArgumentParser(prog="myamber")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # run command
    run_parser = subparsers.add_parser("full_run", help="Full run from minmization to production")
    add_config_arg(run_parser)

    # validate command
    val_parser = subparsers.add_parser("generate_system", help="Generate prmtop and inpcrd using tleap")
    add_config_arg(val_parser)

    args = parser.parse_args()

    if args.command == "full_run":
        from amber_pipeline.orchestrator import Orchestrator

        cfg = load_config(args.config)
        Orchestrator(cfg).run()

    elif args.command == "generate_system":
        from amber_pipeline.system_generation import SystemGeneration
        
        cfg = load_config(args.config)
        SystemGeneration(cfg.tleap).run()
