#!/bin/bash

# This currently does not work because calling update.py without an event doesn't do anything.

if [ -z "$TRAVIS_CI" ]
then
  echo "Performing initial build of site"
  python ./update.py

  echo "Starting Apache"
  /usr/sbin/apachectl start

  echo "
Sites built successfully!
  Public site available at http://localhost:4000
  Private site available at http://localhost:4001
"

  inotifywait -e modify,move,create,delete -m theme/ -r |
  while read filename; do
    echo "Regenerating..."
    python ./update.py
done
else
  python ./update.py
fi
