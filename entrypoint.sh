#!/bin/bash

echo "Creating config file"
cp config.json.sample config.json

echo "Performing initial build of site"
python ./update.py

ROOT=$(cat config.json | jq '.site_root' | head -c -2 | tail -c +2)
SITE=$(cat config.json | jq '.private_site .root' | head -c -2 | tail -c +2)
BUILD=$(cat config.json | jq '.private_site .build' | head -c -2 | tail -c +2)

cd ${ROOT} && cd ${SITE} && cd ${BUILD}

http-server -p 4000
