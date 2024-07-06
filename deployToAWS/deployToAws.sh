#!/bin/sh
ssh -i /home/simon/Schreibtisch/Server/Produkt.pem ubuntu@ec2-51-20-249-18.eu-north-1.compute.amazonaws.com 'docker-compose down'
ssh -i /home/simon/Schreibtisch/Server/Produkt.pem ubuntu@ec2-51-20-249-18.eu-north-1.compute.amazonaws.com 'docker-compose stop'
ssh -i /home/simon/Schreibtisch/Server/Produkt.pem ubuntu@ec2-51-20-249-18.eu-north-1.compute.amazonaws.com 'docker-compose up --build -d'