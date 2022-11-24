# syntax=docker/dockerfile:1

FROM python:alpine

WORKDIR /python-docker

COPY pip-install/libraries requirements.txt
COPY redis-install/alpine-redis-install.sh /python-docker/alpine-redis-install.sh
RUN pip3 install -r requirements.txt
RUN chmod +x /python-docker/alpine-redis-install.sh
RUN sh /python-docker/alpine-redis-install.sh
COPY . .

CMD  redis-server --daemonize yes ; python3 filldb.py ; python3 application.py

