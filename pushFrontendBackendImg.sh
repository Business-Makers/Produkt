#!/bin/sh
docker login

docker build -t simfed/frontend:latest "$(pwd)/Frontend/strade/"

docker push simfed/frontend:latest 

docker build -t simfed/backend:latest "$(pwd)/Backend/Server/"

docker push simfed/backend:latest 