#!/bin/bash -e

DIRECTORY=$(cd "`dirname "$0"`" && pwd)

docker run --rm -it -v ${DIRECTORY}:/workspace ghcr.io/molecularprogrammer/container-properdocs properdocs build
