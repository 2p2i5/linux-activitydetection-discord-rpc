#!/bin/bash

echo "getting list"

curl https://discord.com/api/v10/games/detectable -o detectable.json 

echo "done"

sleep 3