#!/bin/bash
docker-compose up -d front
docker-compose up -d back
sleep 5
docker-compose up -d loadbal
echo "Done...."
echo "The containers are:"
docker ps