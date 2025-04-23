FROM node:20-alpine

WORKDIR /usr/src/app

COPY package*.json ./

RUN npm i --legacy-peer-deps

COPY . .

RUN npm run build

RUN npm install -g serve

CMD [ "serve", "-s", "dist", "-l", "3000" ]