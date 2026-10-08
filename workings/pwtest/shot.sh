#!/bin/bash
# usage: ./shot.sh <outname> [extra query params]
OUT=${1:-shots}
Q=${2:-""}
cd /tmp/pwtest
TARGET="file:///home/user/Codebase/ass-bench/figure.html?t=1${Q}" \
  .venv/bin/python -c "
import sys
sys.argv=['shot','/home/user/Codebase/ass-bench/figure.html','/tmp/$OUT']
exec(open('/tmp/pwtest/shot.py').read())
"
