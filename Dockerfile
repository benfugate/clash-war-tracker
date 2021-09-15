FROM php:7.4-apache

RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y python3 python3-dev python3-pip cron
RUN pip3 install typing aiohttp coc.py

RUN mv "$PHP_INI_DIR/php.ini-production" "$PHP_INI_DIR/php.ini"

COPY clash-cron /etc/cron.d/clash-cron
RUN chmod 0644 /etc/cron.d/clash-cron && \
    crontab /etc/cron.d/clash-cron

COPY www/ /var/www/html/
COPY src/ /clash-tracker/
RUN mkdir -p /clash-tracker/errors/ /clash-tracker/backups/
COPY entrypoint.sh /
CMD ["/bin/sh", "/entrypoint.sh"]