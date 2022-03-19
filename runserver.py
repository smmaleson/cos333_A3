#!/usr/bin/env python

# ----------------------------------------------------------------------
# runserver.py
# Author: Shayna Maleson, Ellen Su
# ----------------------------------------------------------------------
from sys import exit, stderr
import argparse
from registrarapp import app
# --------------------------------------------------------------------
# set up argparse help section
parser = argparse.ArgumentParser(prog='regserver.py',
                 description='The registrar application')
parser.add_argument('port',
                    type=int, default="",
                    help='the port at which the server should listen')
args = parser.parse_args()
# ---------------------------------------------------------------------
def main():
    """open server"""
    try:
        app.run(host='0.0.0.0', port=args.port, debug=True)
    except Exception as ex:
        print(f'Unavailable port error: {ex}', file=stderr)
        exit(1)

if __name__ == '__main__':
    main()
