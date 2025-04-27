import subprocess

def run_script(script_name):
    try:
        result = subprocess.run(['python', script_name], check=True, text=True, capture_output=True)
        print(f"Output of {script_name}:\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_name}:\n{e.stderr}")

if __name__ == "__main__":
    scripts = [
        'scripts/parse_to_db/1_1.py',
        'scripts/parse_to_db/1_2.py',
        'scripts/parse_to_db/1_3.py',
        'scripts/parse_to_db/1_4.py',
        'scripts/parse_to_db/1_5.py',
        'scripts/parse_to_db/1_6.py',
        'scripts/parse_to_db/1_7.py',
        'scripts/parse_to_db/1_8.py',
    ]

    for script in scripts:
        run_script(script)
