#!/bin/sh
#docker pull simfed/frontend:latest
#docker pull simfed/backend:latest 

scp -i /home/simon/Schreibtisch/Server/Produkt.pem docker-compose.yml ubuntu@ec2-51-20-249-18.eu-north-1.compute.amazonaws.com:~
