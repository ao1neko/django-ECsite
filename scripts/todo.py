import subprocess

def run():
    cmd = ["python3", "manage.py", "notes"]
    subprocess.run(cmd)