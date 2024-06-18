import configparser
import os

from PyQt5.QtCore import QDir
from PyQt5.QtWidgets import QMessageBox


class BraindumpConfig:
    def __init__(self):
        config_dir = os.path.join(os.environ["HOME"], ".braindump")

        if not QDir(config_dir).exists():
            QDir().mkpath(config_dir)

        self.config_file = os.path.join(config_dir, "braindump.ini")
        self.log_file = os.path.join(config_dir, "braindump.log")
        self.db_file = os.path.join(config_dir, "braindump.db")

        self.config = configparser.ConfigParser()

        if not os.path.exists(self.config_file):
            self.config["Email"] = {
                "sender_email": "your_email@example.com",
                "receiver_email": "receiver_email@example.com",
                "smtp_server": "smtp.example.com",
                "smtp_port": "587",
                "smtp_tls": "true",
                "smtp_ssl": "false",
                "username": "your_username",
                "password": "your_password",
            }
            with open(self.config_file, "w") as configfile:
                self.config.write(configfile)
            QMessageBox.information(
                None,
                "Configuration Created",
                f"The configuration file has been created at: {self.config_file}",
            )

        self.config.read(self.config_file)
