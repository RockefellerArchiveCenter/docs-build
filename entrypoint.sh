#!/bin/bash

echo "Creating config file"
cp config.json.sample config.json

echo "Performing initial build of site"
python ./update.py

cd /home/docs/private/build/

http-server -p 4000 . &

cd /home/docs/docs-build/ && inotifywait -m theme/ |
while read -e modify,attrib,move,create,delete -r directory events filename; do
  python ./update.py
done
