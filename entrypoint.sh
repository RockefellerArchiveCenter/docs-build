#!/bin/bash

echo "Creating config file"
cp config.json.sample config.json

echo "Performing initial build of site"
python ./update.py

cd /home/docs/private/build/

http-server -p 4000 . &

cd /home/docs/docs-build/ && inotifywait -e modify,move,create,delete -m theme/ |
while read -r directory events filename; do
  echo "Regenerating..."
  python ./update.py
done
