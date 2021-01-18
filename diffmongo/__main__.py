#!/usr/bin/env python
"""The main entry point. Invoke as `diffmongo' or `python -m diffmongo`.

"""
import sys


def main():
    try:
        from .core import cli
        exit_status = cli()
    except KeyboardInterrupt:
        print("Ctrl-C pressed. Aborting")
    sys.exit(0)


if __name__ == '__main__':
    main()
