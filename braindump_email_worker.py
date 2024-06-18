import smtplib
import sqlite3

from PyQt5.QtCore import pyqtSignal, QObject

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class BraindumpEmailWorker(QObject):
    send_error = pyqtSignal(str, list)
    emails_sent = pyqtSignal(list)

    def __init__(self, config):
        super().__init__()

        self.load_config(config)

    def load_config(self, config):
        self.sender_email = config.get("Email", "sender_email")
        self.receiver_email = config.get("Email", "receiver_email")
        self.smtp_server = config.get("Email", "smtp_server")
        self.smtp_port = config.getint("Email", "smtp_port")
        self.smtp_tls = config.getboolean("Email", "smtp_tls")
        self.smtp_ssl = config.getboolean("Email", "smtp_ssl")
        self.username = config.get("Email", "username")
        self.password = config.get("Email", "password")

    def send_emails(self, notes):
        try:
            if not notes:
                self.emails_sent.emit([])
                return

            note_ids = []
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                if self.smtp_tls:
                    server.starttls()

                if self.smtp_ssl:
                    server = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port)

                server.login(self.username, self.password)

                for note in notes:
                    note_id, body, timestamp = note
                    message = MIMEMultipart()
                    message["From"] = self.sender_email
                    message["To"] = self.receiver_email
                    message["Subject"] = f"{timestamp}"

                    message.attach(MIMEText(body, "plain"))

                    server.sendmail(
                        self.sender_email, self.receiver_email, message.as_string()
                    )
                    note_ids.append(note_id)

            self.emails_sent.emit(note_ids)
        except Exception as e:
            self.send_error.emit(str(e), note_ids)
