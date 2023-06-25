FROM node:19-alpine

WORKDIR /app

COPY . .

RUN yarn
RUN yarn build

CMD [ "node", ".output/server/index.mjs" ]
