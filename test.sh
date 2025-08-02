#!/bin/bash
set -eu
diff <(python path.py | sort) <(datalog path.dl | sort)
diff <(python cli.py path.dl | sort) <(datalog path.dl | sort)
