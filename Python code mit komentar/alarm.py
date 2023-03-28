# Importiere das smtplib-Modul, um E-Mails über das Simple Mail Transfer Protocol (SMTP) zu senden.
import smtplib
# Importiere das datetime-Modul, um Datum und Uhrzeit abzurufen.
import datetime
# Importiere die EmailMessage-Klasse, um E-Mail-Nachrichtenobjekte zu erstellen.
from email.message import EmailMessage


# Definiere die Alarm-Klasse.
class Alarm:
    # Initialisiere die Klasse mit den benötigten Attributen.
    def __init__(self, soft_limit, hard_limit, message_text, log_file_path):
        self.soft_limit = soft_limit
        self.hard_limit = hard_limit
        self.message_text = message_text
        self.log_file_path = log_file_path
        self.log_file = "alarm_log.txt"

    # Definiere eine Methode, um den aktuellen Wert mit den Grenzwerten zu vergleichen.
    def check_value(self, current_value, network_name):
        # Wenn der aktuelle Wert größer als das soft_limit ist, führe die log_warning-Methode aus.
        if current_value > self.soft_limit:
            self.log_warning(current_value, network_name, self.log_file_path)

            # Wenn der aktuelle Wert größer als das hard_limit ist, führe die send_email-Methode aus.
            if current_value > self.hard_limit:
                self.send_email(current_value, network_name)

    # Definiere eine Methode, um eine Warnung in der Log-Datei zu protokollieren.
    def log_warning(self, current_value, network_name, log_file_path=None):
        # Hole den aktuellen Zeitstempel im Format "Jahr-Monat-Tag Stunde:Minute:Sekunde".
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Erstelle einen formatierten Log-Eintrag mit dem Zeitstempel, Netzwerknamen, der Nachricht und dem aktuellen
        # Wert.
        log_entry = f"{timestamp} Warning: {network_name}, {self.message_text}, {current_value}\n"

        # Wenn kein Log-Dateipfad angegeben wurde, verwende den Standardwert des Attributs log_file.
        if log_file_path is None:
            log_file_path = self.log_file

        # Öffne die Log-Datei im Append-Modus und füge den Log-Eintrag hinzu.
        with open(log_file_path, "a") as f:
            f.write(log_entry)

    # Definiere eine Methode, um eine E-Mail zu senden.
    def send_email(self, current_value, network_name):
        # Hole den aktuellen Zeitstempel im Format "Jahr-Monat-Tag Stunde:Minute:Sekunde".
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Erstelle den Betreff der E-Mail mit dem Netzwerknamen.
        email_subject = f"Hard limit exceeded on {network_name}"
        # Erstelle den Textkörper der E-Mail mit dem Zeitstempel, Netzwerknamen, der Nachricht und dem aktuellen Wert.
        email_body = f"{timestamp}, {network_name}, {self.message_text}, {current_value}"

        # Erstelle ein neues EmailMessage-Objekt.
        msg = EmailMessage()
        # Setze den Inhalt der E-Mail-Nachricht auf den Textkörper.
        msg.set_content(email_body)
        # Setze die E-Mail-Betreffzeile.
        msg["Subject"] = email_subject
        # Setze die Absenderadresse der E-Mail.
        msg["From"] = "tt9197396@gmail.com"
        # Setze die Empfängeradresse der E-Mail.
        msg["To"] = "tt9197396@gmail.com"

        # Verbinde mit dem SMTP-Server über SSL auf Port 465.
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            # Melde dich am SMTP-Server mit der E-Mail-Adresse und dem Passwort an.
            server.login("tt9197396@gmail.com", "aakxnkugwmxmfmtb")
            # Sende die erstellte E-Mail-Nachricht über den SMTP-Server.
            server.send_message(msg)
