from braindump_widget import BraindumpWidget

from PyQt5.QtWidgets import QDateTimeEdit
from PyQt5.QtCore import QDateTime, QTime, QDate


class BraindumpDateTimeEdit(BraindumpWidget, QDateTimeEdit):
    def __init__(self):
        super().__init__()
        self.setDisplayFormat('ddd d MMMM yy')
        self.setCalendarPopup(True)
        self.setFont(self.get_monospace_font(16))

        today = QDate.currentDate()
        midnight = QTime(0, 0, 0)
        self.setDateTime(QDateTime(today, midnight))
