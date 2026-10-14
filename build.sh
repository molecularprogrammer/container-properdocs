#!/bin/bash -e

DIRECTORY=$(cd `dirname $0` && pwd)

docker build -t ghcr.io/molecularprogrammer/container-properdocs -f ${DIRECTORY}/Dockerfile .
