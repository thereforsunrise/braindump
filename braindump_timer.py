from braindump_widget import BraindumpWidget

from PyQt5.QtCore import QTimer

class BraindumpTimer(BraindumpWidget, QTimer):
    def __init__(self, config):
        super().__init__()

        self.timer_interval = self.seconds_to_milliseconds(int(config.file_storage_interval))
        self.start(self.timer_interval)

    def seconds_to_milliseconds(self, seconds):
        return seconds * 1000
