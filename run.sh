#!/bin/bash

docker run -p8080:8080 -p8888:8888 \
       -v "$(pwd)":/root \
       --runtime=nvidia \
       --gpus all \
       --rm -it env3d-private-detector-app $1
