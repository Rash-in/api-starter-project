#!/usr/bin/env python3

import os, argparse
from dotenv import load_dotenv

parser = argparse.ArgumentParser(
    prog='start.py',
    description='Starts server with frontloaded dotenv file for local development.',
    epilog='''---'''
)
parser.add_argument('-d', '--dotenv_path', type=str, required=True, help='Path to dotenv file to load.')
parser.add_argument('-a', '--activate_path', type=str, required=True, help='Path to python virtual environment activate file.')
parser.add_argument('-p', '--app_path', type=str, required=True, help='Path to application file. i.e. main.py/app.py to start application.')
args = parser.parse_args()
dotenv_path = args.dotenv_path
activate_path = args.activate_path
app_path = args.app_path

def main():
    load_dotenv(dotenv_path)
    os.system(f". {activate_path} && python -B {app_path} >&1")

if __name__ == "__main__":
    main()