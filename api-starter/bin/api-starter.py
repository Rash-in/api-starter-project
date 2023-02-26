#!/usr/bin/env python3

import os, sys
from dotenv import load_dotenv

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
APP_LOCATION = os.path.dirname(os.path.join(SCRIPT_PATH))

if __name__ == "__main__":
    # Local dev - argument=local - uses dotenv injected env variables
    if len(sys.argv) == 2 and sys.argv[1] == "local":
        BASE_LOCATION = os.path.dirname(APP_LOCATION)
        DOTENV_PATH = f"{BASE_LOCATION}/.env/Runtime/envs/api-starter.env"
        load_dotenv(DOTENV_PATH)
        os.system(f"python3 {APP_LOCATION}/main.py local >&1")
    # Server/K8S - argument=remote - uses CI injected env variables
    elif len(sys.argv) == 2 and sys.argv[1] == "remote":
        os.system(f"python3 {APP_LOCATION}/main.py remote >&1")
    # Bad Arguments - too few, too many, incorrect
    else:
        sys.exit(f"\nArguments not satisfied.\n\nArgs used:\n      {sys.argv}\n\nArgs required:\n      ['/path/to/bin/api-starter-project/api-starter/bin/api-starter.py', 'local']\n      ['/path/to/bin/api-starter-project/api-starter/bin/api-starter.py, 'remote']\n")
else:
    sys.exit("api-starter.py: Catchall scripting error. Something is wrong with script code.")