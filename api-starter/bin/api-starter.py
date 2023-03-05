#!/usr/bin/env python3

import os, argparse
from dotenv import load_dotenv

parser = argparse.ArgumentParser(
    prog='api-starter.py',
    description='OpenAPI 3.0.2 server used for testing api routing.',
    epilog='''---'''
)
parser.add_argument('-d', '--dotenv_path', type=str, required=False, help='Path to dotenv file to load. If none present runs app without like a remote deploy.')
args = parser.parse_args()
dotenv_path = args.dotenv_path

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
APP_LOCATION = os.path.dirname(os.path.join(SCRIPT_PATH))

def main(dotenv_path:str):
    if not dotenv_path:
        os.system(f"python3 {APP_LOCATION}/main.py -e remote >&1")
    else:
        load_dotenv(dotenv_path)
        os.system(f"python3 {APP_LOCATION}/main.py -e local >&1")

if __name__ == "__main__":
    main(dotenv_path=dotenv_path)