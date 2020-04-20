#!/bin/bash

echo "Creating config files"
cp config.json.sample config.json

if [ ! -f .gitmodules ]; then
  cp .gitmodules-dev .gitmodules
fi

if [ -z "$TRAVIS_CI" ]
then
  echo "Performing initial build of site"
  python ./update.py

  echo "Starting Apache"
  /usr/sbin/httpd

  inotifywait -e modify,move,create,delete -m theme/ -r |
  while read filename; do
    echo "Regenerating..."
    python ./update.py
done
else
  python ./update.py
fi
