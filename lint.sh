#!/bin/bash

echo "Running black ..."

command -v black >/dev/null 2>&1 || { echo >&2 "Black is not installed, aborting lint."; exit 1; }
black src/subrina/*.py 

echo "Running ruff ..."

command -v ruff >/dev/null 2>&1 || { echo >&2 "Ruff is not installed, aborting lint."; exit 1; }
ruff src/subrina/*.py