#!/bin/bash

cid=$(docker ps -aq -f name=dl)

if [ ! -z $cid ]; then
  docker stop dl
  docker rm dl
fi

docker run -d --name dl -p 7778:7778 -v ~/HackMode/dl-stuff:/home/dev/dl-stuff guangyang/dl-box

