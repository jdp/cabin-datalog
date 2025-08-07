#!/bin/bash
# Depends on MITRE Datalog or equivalent interpreter for datalog command
# https://datalog.sourceforge.net/
set -eu
diff <(python path.py | sort) <(datalog path.dl | sort)
diff <(python cli.py path.dl | sort) <(datalog path.dl | sort)
