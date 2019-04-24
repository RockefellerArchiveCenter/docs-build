#!/bin/bash

echo "Creating config file"
cp config.json.sample config.json

echo "Performing initial build of site"
python ./update.py

cd /var/www/internal/

http-server -p 4000
