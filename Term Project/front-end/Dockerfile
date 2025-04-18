FROM node:22-alpine

WORKDIR /app

COPY package.json /app/package.json
COPY package-lock.json /app/package-lock.json

RUN npm clean-install

COPY . /app
RUN npm run build

RUN npm install -g serve

EXPOSE 3000

ENTRYPOINT ["serve", "-s", "build"]