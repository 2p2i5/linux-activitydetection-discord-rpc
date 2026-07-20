#!/bin/bash

echo "Starting program and updating..."
echo " "

./updatedetectables.sh

source ./venv/bin/activate && python3 main.py

sleep 2