import os, sys, argparse
from dotenv import load_dotenv

THIS_SCRIPT = os.path.realpath(__file__)
BIN_LOCATION = os.path.dirname(THIS_SCRIPT)
BASE_LOCATION = os.path.dirname(BIN_LOCATION)
