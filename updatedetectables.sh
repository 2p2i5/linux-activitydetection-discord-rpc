#!/bin/bash

echo "getting list"
echo " "

curl https://discord.com/api/v10/games/detectable -o detectable.json 

echo " "
echo "done"

sleep 1