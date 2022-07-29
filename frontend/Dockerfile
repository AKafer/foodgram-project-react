# build env
FROM node:13.12.0-alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm config set strict-ssl false
RUN npm install
COPY . ./
RUN npm run build
CMD cp -r build result_build
