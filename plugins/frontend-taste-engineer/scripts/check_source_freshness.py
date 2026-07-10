#!/usr/bin/env python3
import sys
from tooling_core import main

if __name__ == "__main__":
    argv = ["--json-out" if value == "--output" else value for value in sys.argv[1:]]
    raise SystemExit(main(argv, default_command="check-freshness"))
