import os
import glob

BASE_DIR = os.path.dirname(os.path.dirname(__file__)) # このファイルの場所によって変更

def run():
    migration_files = glob.iglob('**/migrations/[0-9][0-9][0-9][0-9]*.py', recursive=True)
    for migration_file in migration_files:
        os.remove(os.path.join(BASE_DIR, migration_file))
        print(f"Deleted {migration_file}")