import subprocess

def run():
    cmd = ["python3", "manage.py", "reset_db"]
    subprocess.run(cmd)