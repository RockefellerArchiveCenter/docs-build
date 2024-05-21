#!/bin/bash


echo "Performing initial build of site"
python ./update.py

echo "Starting Apache"
/usr/sbin/apachectl start

echo "
Site built successfully!
Public site available at http://localhost:4000
"

inotifywait -e modify,move,create,delete -m theme/ -r |
while read filename; do
  echo "Regenerating..."
  python ./update.py
done

fi
