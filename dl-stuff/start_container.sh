#!/bin/bash

CNAME="dl-ao"
cid=$(docker ps -aq -f name=${CNAME})

if [ ! -z $cid ]; then
  docker stop ${cid}
  docker rm ${cid}
fi

DL_PATH=$(pwd)

docker run -d --name ${CNAME} -p 7778:7778 -v ${DL_PATH}:/home/dev/dl-stuff guangyang/dl-box

