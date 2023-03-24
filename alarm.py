import smtplib
import datetime
from email.message import EmailMessage


class Alarm:
    def __init__(self, soft_limit, hard_limit, message_text, log_file_path):
        self.soft_limit = soft_limit
        self.hard_limit = hard_limit
        self.message_text = message_text
        self.log_file_path = log_file_path
        self.log_file = "alarm_log.txt"

    def check_value(self, current_value, network_name):
        if current_value > self.soft_limit:
            self.log_warning(current_value, network_name, self.log_file_path)

            if current_value > self.hard_limit:
                self.send_email(current_value, network_name)

    def log_warning(self, current_value, network_name, log_file_path=None):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} Warning: {network_name}, {self.message_text}, {current_value}\n"

        if log_file_path is None:
            log_file_path = self.log_file

        with open(log_file_path, "a") as f:
            f.write(log_entry)

    def send_email(self, current_value, network_name):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        email_subject = f"Hard limit exceeded on {network_name}"
        email_body = f"{timestamp}, {network_name}, {self.message_text}, {current_value}"

        msg = EmailMessage()
        msg.set_content(email_body)
        msg["Subject"] = email_subject
        msg["From"] = "afschar376@gmail.com"
        msg["To"] = "afschar376@gmail.com"

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login("afschar376@gmail.com", "faexaganmnlfjykq")
            server.send_message(msg)
