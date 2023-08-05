#!/usr/bin/env python3

import configparser
import os
import sys

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QDateTimeEdit, QPlainTextEdit, QLabel, QFrame, QCalendarWidget, QMenu, QAction
from PyQt5.QtCore import Qt, QDate, QDateTime, QTime, QStandardPaths, QTimer, QFile, QTextStream
from PyQt5.QtGui import QFont, QFontDatabase, QKeyEvent, QTextCursor

class BraindumpApp(QWidget):
    def __init__(self):
        super().__init__()

        config_dir = QStandardPaths.writableLocation(QStandardPaths.ConfigLocation)
        self.config_file_path = os.path.join(config_dir, 'braindump.ini')
        self.config = configparser.ConfigParser()
        self.config.read(self.config_file_path)
        self.file_storage_directory = self.config.get('Settings', 'file_storage_directory', fallback='default_directory')
        self.file_storage_interval = self.config.get('Settings', 'file_storage_interval', fallback='30')

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Braindump')

        self.timer = QTimer(self)
        self.timer_interval = self.seconds_to_milliseconds(int(self.file_storage_interval))
        self.timer.timeout.connect(self.save_file_for_date)
        self.timer.start(self.timer_interval)

        layout = QVBoxLayout()

        self.page_content_textedit = QTextEdit()
        self.page_content_textedit.setAlignment(Qt.AlignCenter)
        self.page_content_textedit.setFont(self.get_monospace_font(16))
        self.page_content_textedit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.page_content_textedit.textChanged.connect(self.hide_vertical_scrollbar)

        self.date_time_edit = QDateTimeEdit()
        self.date_time_edit.setDisplayFormat('ddd d MMMM yy')
        self.date_time_edit.setCalendarPopup(True)
        self.date_time_edit.setFont(self.get_monospace_font(16))

        today = QDate.currentDate()
        midnight = QTime(0, 0, 0)
        self.date_time_edit.setDateTime(QDateTime(today, midnight))

        self.date_time_edit.dateTimeChanged.connect(self.load_file_for_date)
        layout.addWidget(self.date_time_edit)
        layout.addWidget(self.page_content_textedit)

        self.setLayout(layout)

        self.load_file_for_date(self.date_time_edit.dateTime())

        self.page_content_textedit.setFocus()

    def hide_vertical_scrollbar(self):
        self.page_content_textedit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def render_html(self):
        markdown_text = self.textEdit.toPlainText()
        html_text = markdown.markdown(markdown_text)
        self.webView.setHtml(html_text)

    def get_monospace_font(self, font_size):
        font_id = QFontDatabase.addApplicationFont(":/fonts/Inconsolata-Regular.ttf")

        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        else:
            font_family = "monospace"

        font = QFont(font_family, font_size)
        return font

    def seconds_to_milliseconds(self, seconds):
        return seconds * 1000

    def keyPressEvent(self, event: QKeyEvent):
        modifiers = QApplication.keyboardModifiers()
        if modifiers == (Qt.ControlModifier | Qt.ShiftModifier):
            if event.key() == Qt.Key_B:
                self.save_file_for_date()
                self.goto_previous_date()
            elif event.key() == Qt.Key_F:
                self.save_file_for_date()
                self.goto_next_date()
            elif event.key() == Qt.Key_G:
                self.show_calendar()
            elif event.key() == Qt.Key_P:
                self.save_file_for_date()
                self.goto_current_date()
            elif event.key() == Qt.Key_S:
                self.save_file_for_date()

    def goto_previous_date(self):
        current_date = self.date_time_edit.dateTime()
        new_date = current_date.addDays(-1)
        self.date_time_edit.setDateTime(new_date)

    def goto_next_date(self):
        current_date = self.date_time_edit.dateTime()
        new_date = current_date.addDays(1)
        self.date_time_edit.setDateTime(new_date)

    def goto_current_date(self):
        self.date_time_edit.setDateTime(QDateTime(QDate.currentDate(), QTime(0, 0, 0)))

    def load_file_for_date(self, selected_datetime):
        selected_date = selected_datetime.date()
        filename = self.get_file_path(selected_date)
        try:
            with open(filename, 'r') as file:
                content = file.read()
            self.page_content_textedit.setPlainText(content)
        except FileNotFoundError:
            self.page_content_textedit.setPlainText("")
            self.save_file_for_date()

        cursor = self.page_content_textedit.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.page_content_textedit.setTextCursor(cursor)

    def save_file_for_date(self):
        selected_date = self.date_time_edit.date()
        filename = self.get_file_path(selected_date)
        content = self.page_content_textedit.toPlainText()
        with open(filename, 'w') as file:
            file.write(content)

    def get_file_path(self, selected_date):
        year = selected_date.toString('yyyy')
        month = selected_date.toString('MM')
        day = selected_date.toString('dd')
        directory = os.path.join(self.file_storage_directory, year, month)
        filename = os.path.join(directory, day + '.txt')
        os.makedirs(directory, exist_ok=True)
        return filename

    def show_calendar(self):
        calendar_widget = QCalendarWidget(self)
        calendar_widget.setWindowFlags(Qt.Popup)
        calendar_widget.setGeometry(200, 200, 300, 200)
        calendar_widget.clicked.connect(self.handle_calendar_selection)
        calendar_widget.show()

    def handle_calendar_selection(self, date):
        selected_date = date.toString("yyyy-MM-dd")

def loadStylesheet(filename):
    style_file = QFile(filename)
    if style_file.open(QFile.ReadOnly | QFile.Text):
        stream = QTextStream(style_file)
        stylesheet = stream.readAll()
        return stylesheet

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(loadStylesheet("braindump.qss"))
    window = BraindumpApp()
    window.showFullScreen()
    sys.exit(app.exec_())
