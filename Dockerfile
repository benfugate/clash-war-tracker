FROM python/slim

RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y cron

COPY requirements.txt .
RUN pip3 install -r requirements.txt && rm requirements.txt

COPY clash-cron /etc/cron.d/clash-cron
RUN chmod 0644 /etc/cron.d/clash-cron && \
    crontab /etc/cron.d/clash-cron

COPY src/ /clash-tracker/src/
COPY data/ /clash-tracker/data/
RUN chmod -R 777 /clash-tracker/data/
RUN mkdir -p /clash-tracker/data/errors/ /clash-tracker/data/backups/
COPY entrypoint.sh /
CMD ["/bin/sh", "/entrypoint.sh"]