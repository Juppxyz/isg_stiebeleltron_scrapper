import os
import mysql.connector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def scrape_and_store():
    # MySQL-Verbindungskonfiguration aus Umgebungsvariablen
    db_config = {
        "host":     os.environ.get("MYSQL_HOST", "172.17.0.2"),
        "user":     os.environ.get("MYSQL_USER", "root"),
        "password": os.environ.get("MYSQL_PASSWORD", "Start123"),
        "database": os.environ.get("MYSQL_DB", "stiebel_eltron")
    }

    # Verbindung zur Datenbank herstellen
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Tabelle erstellen (falls nicht vorhanden)
    create_table_query = """CREATE TABLE IF NOT EXISTS stiebel_eltron.prozessdaten (id INT AUTO_INCREMENT PRIMARY KEY, `key` VARCHAR(255) NOT NULL, `value` VARCHAR(255) NOT NULL);"""
    cursor.execute(create_table_query)
    conn.commit()

    # Selenium Remote WebDriver konfigurieren
    # Name & Port kommen ebenfalls aus einer Umgebungsvariable, fallback: "http://selenium:4444/wd/hub"
    selenium_url = "http://selenium:4444/wd/hub"

    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Falls gewünscht
    driver = webdriver.Remote(
        command_executor=selenium_url,
        options=chrome_options
    )

    try:
        # Beispiel: Für das Ziel-URL ebenfalls eine ENV-Variable oder Fallback
        target_url = os.environ.get("TARGET_URL", "http://192.168.0.100/?s=1,1")
        print(f"Lade Webseite: {target_url}")
        driver.get(target_url)

        tables = driver.find_elements(By.CLASS_NAME, "info")
        data_list = []
        for table in tables:
            rows = table.find_elements(By.TAG_NAME, "tr")
            for row in rows:
                columns = row.find_elements(By.TAG_NAME, "td")
                data = [col.text for col in columns]

                if len(data) >= 2:  # Sicherstellen, dass mindestens zwei Spalten vorhanden sind
                    print(data)
                    data_list.append((data[0], data[1]))

        # Daten in MySQL einfügen
        if data_list:
            insert_query = "INSERT INTO prozessdaten (`key`, `value`) VALUES (%s, %s)"
            cursor.executemany(insert_query, data_list)
            conn.commit()
            print("Daten erfolgreich in MySQL gespeichert.")

    finally:
        # Schließe den WebDriver
        driver.quit()
        # Verbindung schließen
        cursor.close()
        conn.close()

if __name__ == "__main__":
    scrape_and_store()
