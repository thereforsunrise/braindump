import configparser
import platform
import os

from PyQt5.QtCore import QDir
from PyQt5.QtWidgets import QMessageBox


class BraindumpConfig:
    @staticmethod
    def defaults():
        config = configparser.ConfigParser()
        config["Interface"] = {
            "font_family": "Monospace",
            "font_size": "24",
            "background_color": "#282a36",
            "foreground_color": "white"
        }
        config["Email"] = {
            "sender_email": "your_email@example.com",
            "receiver_email": "receiver_email@example.com",
            "smtp_server": "smtp.example.com",
            "smtp_port": "587",
            "smtp_tls": "true",
            "smtp_ssl": "false",
            "username": "your_username",
            "password": "your_password",
            "interval": 30000
        }

        return config

    @staticmethod
    def config_dir():
        if platform.system() == "Windows":
            return os.path.join(os.environ["USERPROFILE"], ".braindump")
        else:
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
        if not os.path.exists(BraindumpConfig.config_dir()):
            os.makedirs(BraindumpConfig.config_dir())

        config = BraindumpConfig.defaults()

        if not os.path.exists(BraindumpConfig.config_file()):
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
