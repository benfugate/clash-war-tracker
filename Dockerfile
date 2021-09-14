FROM chvb/docker-apache-php

RUN add-apt-repository ppa:deadsnakes/ppa && apt-get update && \
    apt-get -y upgrade && apt-get install -y python3.6

RUN curl -s https://bootstrap.pypa.io/get-pip.py | python3.6
RUN python3.6 -m pip install typing aiohttp coc.py

COPY clash-cron /etc/cron.d/clash-cron
RUN chmod 0644 /etc/cron.d/clash-cron && \
    crontab /etc/cron.d/clash-cron

COPY . /config/