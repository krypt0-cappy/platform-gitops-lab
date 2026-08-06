import sys

from atlas.cli.aws import (
    run_regions,
    run_whoami,
)
from atlas.cli.help import print_usage
from atlas.cli.inventory import run_inventory


def main() -> None:

    arguments = sys.argv[1:]

    if not arguments:
        print_usage()
        return

    command = arguments[0]

    if command == "whoami":
        run_whoami()
        return

    if command == "regions":
        run_regions()
        return

    if command == "inventory":
        run_inventory(arguments[1:])
        return

    print(f"Unknown command: {command}")
    print_usage()

    sys.exit(1)
