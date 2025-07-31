#!/bin/bash
set -eu
diff <(python path.py | sort) <(datalog path.dl | sort)
