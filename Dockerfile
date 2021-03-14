### STAGE 1: Build ###

FROM node:10-alpine as builder

COPY webapp/package.json webapp/package-lock.json ./

RUN npm i && mkdir /ng-app && mv ./node_modules ./ng-app

WORKDIR /ng-app

COPY webapp /ng-app

RUN $(npm bin)/ng build --prod --output-path=dist


### STAGE 2: Setup ###

FROM python:latest

RUN mkdir /server
WORKDIR /server
COPY requirements.txt /server/
RUN python -m pip install -r /server/requirements.txt

COPY . /server
COPY --from=builder /ng-app/dist /server/static

CMD ["python", "app.py"]
