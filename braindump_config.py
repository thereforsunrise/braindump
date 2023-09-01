import os
import configparser

from braindump_widget import BraindumpWidget

from PyQt5.QtCore import QStandardPaths


class BraindumpConfig:
    def __init__(self):
        config_dir = QStandardPaths.writableLocation(
            QStandardPaths.ConfigLocation)
        self.config_file_path = os.path.join(config_dir, 'braindump.ini')
        self.config = configparser.ConfigParser()
        self.config.read(self.config_file_path)
        self.notebooks_base_directory = self.config.get(
            'Settings', 'notebooks_base_directory', fallback='default_directory')
        self.save_interval = self.config.get(
            'Settings', 'save_interval', fallback='30')
