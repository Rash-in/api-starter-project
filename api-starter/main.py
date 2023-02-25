import os, sys, argparse
from pathlib import Path
from dotenv import load_dotenv

sys.dont_write_bytecode = True

parser = argparse.ArgumentParser(
    prog='main.py',
    description='''API-Starter. Used as a test repo for playing with FastAPI architecture.''',
    epilog='''---'''
)
parser.add_argument('-d', '--dotenv_path', type=Path, help='Absolute path to dotenv file. Ends with filename. /path/to/file/api-starter.env')
args = parser.parse_args()

if args.dotenv_path:
    dotenv_exists = os.path.exists(args.dotenv_path)
    print(f"Dotenv Exists: {dotenv_exists}")

def main():
    print(f"Arguments: {args}")

if __name__ == "main":
    main()