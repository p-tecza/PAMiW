# syntax=docker/dockerfile:1

FROM python:alpine

WORKDIR /python-docker

COPY pip-install/libraries requirements.txt
COPY redis-install/alpine-redis-install.sh redis-install-script
RUN pip3 install -r requirements.txt
RUN ./redis-install-script
COPY . .

CMD  redis-server --daemonize yes ; python3 filldb.py ; python3 application.py

