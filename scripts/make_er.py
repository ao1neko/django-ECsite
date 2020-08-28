import subprocess

def run():
    cmd = ["python3", "manage.py", "graph_models", "-a", "-o","graph.png"]
    subprocess.run(cmd)