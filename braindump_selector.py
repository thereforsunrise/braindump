import os

from braindump_widget import BraindumpWidget

from PyQt5.QtWidgets import QLineEdit, QComboBox


class BraindumpSelector(BraindumpWidget, QComboBox):
    def __init__(self, config):
        super().__init__()
        self.setFont(self.get_monospace_font(16))

        for directory in self.list_directories(config.notebooks_base_directory):
            self.addItem(directory)

    def list_directories(self, directory_path):
        directories = [
            d for d in os.listdir(directory_path) if os.path.isdir(
                os.path.join(
                    directory_path, d))]
        return directories

    def showPopup(self):
        pass
