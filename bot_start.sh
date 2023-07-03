#!/bin/bash

cd /path/to/discord-util-bot

# update local repo
git fetch
git pull origin

# Start the Python script and kill it every 24hs
timeout -k 24h 24h python main.py &
