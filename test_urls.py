#!/usr/bin/env python

from os import environ
import urllib3

EXPECTED_PATHS = [
    "/",
    "/about/",
    "/docs-guide/",
    "/docs-guide/add-content/",
    "/docs-guide/using-markdown/",
    "/docs-guide/using-github/"
]

http = urllib3.PoolManager()

for path in EXPECTED_PATHS:
    for port in ["4000", "4001"]:
        url = "http://{}:{}{}".format(environ.get("CONTAINER"), port, path)
        resp = http.request("GET", url)
        assert resp.status == 200, "Did not receive the expected response for {}".format(url)
