#!/bin/bash

echo "updating detectables, make sure updatedetectables.sh is executable"
echo " "

./updatedetectables.sh

echo " "
echo "running program"
echo " "

source ./venv/bin/activate && python3 main.py