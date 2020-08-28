import subprocess

def run():
    cmd = ["python3", "manage.py", "show_urls", "--format", "aligned", "--force-color"]
    subprocess.run(cmd)