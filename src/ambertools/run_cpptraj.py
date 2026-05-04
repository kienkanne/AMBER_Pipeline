import subprocess

def run_cpptraj(input_file):
    # Run cpptraj command
    cpptraj_cmd = f"cpptraj -i {input_file}"
    result = subprocess.run(cpptraj_cmd, capture_output=True, text=True, shell=True)

    if result.returncode != 0:
        print(f"CPPTRAJ FAILED: {result.stderr}")
    else:
        print("CPPTRAJ SUCCESS")