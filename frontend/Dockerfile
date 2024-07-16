FROM node:18.7.0-alpine
WORKDIR /usr/src/app
COPY package.json /usr/src/app/
COPY . /usr/src/app/
RUN apk update && apk add bash
# RUN npm install --force --legacy-peer-deps