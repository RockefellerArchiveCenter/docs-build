#!/bin/bash

echo "Creating config file"
cp config.json.sample config.json

echo "Performing initial build of site"
python ./update.py

cd /home/docs/private/build/

echo "Starting server"
python -m SimpleHTTPServer 4000
