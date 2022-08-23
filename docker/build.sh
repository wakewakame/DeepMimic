#!/bin/bash
set -eu
docker build -t deepmimic . --network host
docker run -d -it --name deepmimic deepmimic
docker exec -it deepmimic /bin/bash

