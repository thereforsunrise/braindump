from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTextEdit

from braindump_widget import BraindumpWidget

class BraindumpTextEdit(BraindumpWidget, QTextEdit):
    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignCenter)
        self.setFont(self.get_monospace_font(16))
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textChanged.connect(self.hide_vertical_scrollbar)

    def hide_vertical_scrollbar(self):
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
