FROM python:3.9-slim

# 1) System-Pakete aktualisieren & cron installieren
RUN apt-get update && apt-get install -y \
    cron \
    && rm -rf /var/lib/apt/lists/*

# 2) Arbeitsverzeichnis setzen
WORKDIR /usr/src/app

# 3) Python-Abhängigkeiten installieren
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 4) App-Code kopieren
COPY app/ ./

# 5) Cronjob einrichten
# Beispiel: alle 5 Minuten wird das Skript aufgerufen
# Alternativ kann man den Zeitplan in eine extra Datei auslagern (siehe "cronjob")
RUN echo "*/5 * * * * python /usr/src/app/main.py >> /var/log/cron.log 2>&1" > /etc/cron.d/app-cron
RUN chmod 0644 /etc/cron.d/app-cron

# Aktivieren des neu erstellten Cronjobs
RUN crontab /etc/cron.d/app-cron

# 6) Container soll im Vordergrund laufen, damit Docker nicht direkt beendet
CMD ["cron", "-f"]
