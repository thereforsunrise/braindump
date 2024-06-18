import configparser
import os

from PyQt5.QtCore import QDir
from PyQt5.QtWidgets import QMessageBox


class BraindumpConfig:
    @staticmethod
    def config_dir():
        return os.path.join(os.environ["HOME"], ".braindump")

    @staticmethod
    def config_file():
        return os.path.join(BraindumpConfig.config_dir(), "braindump.ini")

    @staticmethod
    def log_file():
        return os.path.join(BraindumpConfig.config_dir(), "braindump.log")

    @staticmethod
    def db_file():
        return os.path.join(BraindumpConfig.config_dir(), "braindump.db")

    @staticmethod
    def load_config():
        if not QDir(BraindumpConfig.config_dir()).exists():
            QDir().mkpath(BraindumpConfig.config_dir())

        config = configparser.ConfigParser()

        if not os.path.exists(BraindumpConfig.config_file()):
            config["Email"] = {
                "sender_email": "your_email@example.com",
                "receiver_email": "receiver_email@example.com",
                "smtp_server": "smtp.example.com",
                "smtp_port": "587",
                "smtp_tls": "true",
                "smtp_ssl": "false",
                "username": "your_username",
                "password": "your_password",
                "interval": "30000"
            }
            with open(BraindumpConfig.config_file(), "w") as configfile:
                config.write(configfile)
            QMessageBox.information(
                None,
                "Configuration Created",
                f"The configuration file has been created at: {
                    BraindumpConfig.config_file()}",
            )

        config.read(BraindumpConfig.config_file())

        return config
