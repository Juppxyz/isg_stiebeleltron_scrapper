FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    cron \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./

# 1) Cronjob in Datei schreiben
RUN echo "*/5 * * * * /usr/local/bin/python /usr/src/app/main.py >> /var/log/cron.log 2>&1" > /etc/cron.d/app-cron

# 2) Berechtigungen setzen
RUN chmod 0644 /etc/cron.d/app-cron

# 3) Cron-Job installieren
RUN crontab /etc/cron.d/app-cron

# 4) Container im Vordergrund laufen lassen
CMD ["cron", "-f"]
