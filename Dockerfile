FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    cron \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./

# 2) Cronjob einrichten
# Beispiel: alle 5 Minuten wird das Skript aufgerufen
# Alternativ kann man den Zeitplan in eine extra Datei auslagern (siehe "cronjob")
RUN echo "*/5 * * * * python /usr/src/app/main.py >> /var/log/cron.log 2>&1" > /etc/cron.d/app-cron
RUN chmod 0644 /etc/cron.d/app-cron
RUN crontab /etc/cron.d/app-cron

CMD ["cron", "-f"]
