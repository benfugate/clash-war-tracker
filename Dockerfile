FROM php:7.4-apache

RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y python3 python3-dev python3-pip cron

COPY requirements.txt .
RUN pip3 install -r requirements.txt && rm requirements.txt

RUN mv "$PHP_INI_DIR/php.ini-production" "$PHP_INI_DIR/php.ini"

COPY clash-cron /etc/cron.d/clash-cron
RUN chmod 0644 /etc/cron.d/clash-cron && \
    crontab /etc/cron.d/clash-cron

COPY www/ /var/www/html/
COPY src/ /clash-tracker/src/
COPY data/ /clash-tracker/data/
RUN chmod -R 777 /clash-tracker/data/
RUN mkdir -p /clash-tracker/data/errors/ /clash-tracker/data/backups/
COPY entrypoint.sh /
CMD ["/bin/sh", "/entrypoint.sh"]