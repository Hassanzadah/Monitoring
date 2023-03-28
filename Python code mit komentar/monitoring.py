# Importiere das `socket` Modul für Netzwerkverbindungen
import socket
# Importiere das `sys` Modul für Systemfunktionen
import sys
# Importiere das `argparse` Modul für das Parsen von Kommandozeilenargumenten
import argparse
# Importiere das `time` Modul für Zeitfunktionen
import time
# Importiere das `psutil` Modul für System- und Prozessinformationen
import psutil
# Importiere die `Alarm` Klasse aus dem alarm Modul
from alarm import Alarm


# Definiere eine Methode, welche den Prozentsatz des verwendeten Festplattenspeichers zurückgibt
def get_disk_space():
    return psutil.disk_usage('/').percent


# Definiere eine Methode, welche die Anzahl der laufenden Prozesse zurückgibt
def get_number_of_processes():
    return len(psutil.pids())


def main(args):
    # Weise die übergebenen Argumente entsprechenden Variablen zu
    metric = args.function
    soft_limit = args.softLimit
    hard_limit = args.hardLimit
    message_text = args.messageText
    interval = args.interval
    iterations = args.iterations
    use_interval = args.useInterval
    log_file_path = args.logFile

    # Erstelle ein Alarm-Objekt
    alarm = Alarm(soft_limit, hard_limit, message_text, log_file_path)

    # Initialisiere einen Zähler für die Anzahl der Durchläufe
    counter = 0

    # Wiederhole den Prozess so lange, entweder wie kein Intervall verwendet wird oder die maximale Anzahl der
    # Iterationen noch nicht erreicht ist
    while not use_interval or (iterations is None or counter < iterations):
        # Prüfe, welche Metrik verwendet werden soll und rufe die entsprechende Funktion auf
        if metric == "disk_space":
            current_value = get_disk_space()
        elif metric == "processes":
            current_value = get_number_of_processes()
        else:
            print("Invalid metric.")
            # Beende das Programm, wenn die Metrik ungültig ist
            sys.exit(1)

        # Ermittele den Hostnamen des Systems
        network_name = socket.gethostname()
        # Überprüfe den aktuellen Wert der Metrik und löse ggf. einen Alarm aus
        alarm.check_value(current_value, network_name)

        # Wenn das Intervall im Skript verwendet wird, wartet das Skript für die angegebene Zeit und erhöht den Zähler
        if use_interval:
            time.sleep(interval)
            counter += 1
        else:
            # Beende die Schleife, wenn kein Intervall im Skript verwendet wird
            break


def parse_arguments():
    parser = argparse.ArgumentParser(description="Monitoring script")
    # Füge die unterstützten Argumente und deren Optionen zum ArgumentParser hinzu
    parser.add_argument("--function", choices=["disk_space", "processes"], required=True,
                        help="Function to monitor")
    parser.add_argument("--softLimit", type=int, required=True, help="Soft limit for the selected function")
    parser.add_argument("--hardLimit", type=int, required=True, help="Hard limit for the selected function")
    parser.add_argument("--messageText", type=str, required=True, help="Message text for the alarm")
    parser.add_argument("--interval", type=int, default=60, help="Interval between checks in seconds")
    parser.add_argument("--iterations", type=int, default=None, help="Number of iterations to run before stopping ("
                                                                     "None for infinite)")
    parser.add_argument("--useInterval", action="store_true", help="Use script interval instead of Task Scheduler "
                                                                   "interval")
    parser.add_argument("--logFile", type=str, default=None, help="Path to the log file")

    # Parse die Argumente und gibe sie zurück
    return parser.parse_args()


if __name__ == "__main__":
    # Rufe die parse_arguments Funktion auf, um die Argumente zu parsen
    arguments = parse_arguments()
    # Rufe die main Funktion mit den geparsten Argumenten auf
    main(arguments)
