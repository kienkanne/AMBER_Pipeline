import subprocess
import os

AMBERHOME = os.environ.get("AMBERHOME")
if not AMBERHOME:
    raise RuntimeError("AMBERHOME environment variable not set")

def run_tleap(tleap_input: str) -> str:
    result = subprocess.run(
        ["tleap", "-f", "-"],
        input=tleap_input,
        capture_output=True,
        text=True,
        check=True
    )

    if result.returncode != 0:
        raise RuntimeError(f"tleap failed:\n{result.stderr}\n{result.stdout}")

    return result.stdout