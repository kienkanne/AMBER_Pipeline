import subprocess

def run_tleap(tleap_input: str) -> str:
    result = subprocess.run(
        ["tleap", "-f", "-"],
        input=tleap_input,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(f"tleap failed:\n{result.stderr}\n{result.stdout}")

    return result.stdout