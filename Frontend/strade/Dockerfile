
FROM node:alpine AS development


WORKDIR /app


COPY package*.json ./

# Installieren Sie die Abhängigkeiten
RUN npm install --legacy-peer-deps

# Kopieren Sie den Rest des Anwendungscodes in den Container
COPY .. .

# Exponieren Sie den Port, auf dem die App läuft
EXPOSE 3000

# Starten Sie die Anwendung
CMD ["npm", "start"]