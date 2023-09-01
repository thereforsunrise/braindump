#!/usr/bin/env python3

import os
from os import path

import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTextEdit, QDateTimeEdit, QPlainTextEdit, QLabel, QFrame, QCalendarWidget, QMenu, QAction
from PyQt5.QtCore import Qt, QDate, QDateTime, QTime, QStandardPaths, QTimer, QFile, QTextStream, QObject, QEvent
from PyQt5.QtGui import QKeyEvent, QTextCursor

from braindump_widget import BraindumpWidget
from braindump_textedit import BraindumpTextEdit
from braindump_timer import BraindumpTimer
from braindump_datetimeedit import BraindumpDateTimeEdit
from braindump_config import BraindumpConfig
from braindump_selector import BraindumpSelector


class BraindumpApp(QWidget):
    def __init__(self):
        super().__init__()

        self.config = BraindumpConfig()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Braindump')

        self.page_content_textedit = BraindumpTextEdit()
        self.date_time_edit = BraindumpDateTimeEdit()
        self.timer = BraindumpTimer(self.config)
        self.selector = BraindumpSelector(self.config)

        self.timer.timeout.connect(self.save_file_for_date)
        self.date_time_edit.dateTimeChanged.connect(self.load_file_for_date)
        self.selector.currentIndexChanged.connect(self.load_journal)

        self.current_directory = os.path.join(
            self.config.file_storage_directory, self.selector.currentText())

        self.load_file_for_date(self.date_time_edit.dateTime())

        layout = QVBoxLayout()
        self.setLayout(layout)

        layout.addWidget(self.selector)
        layout.addWidget(self.date_time_edit)
        layout.addWidget(self.page_content_textedit)

        self.page_content_textedit.setFocus()

    def keyPressEvent(self, event: QKeyEvent):
        modifiers = QApplication.keyboardModifiers()
        if modifiers == (Qt.ControlModifier | Qt.ShiftModifier):
            if event.key() == Qt.Key_B:
                self.save_file_for_date()
                self.goto_previous_date()
            elif event.key() == Qt.Key_F:
                self.save_file_for_date()
                self.goto_next_date()
            elif event.key() == Qt.Key_P:
                self.save_file_for_date()
                self.goto_current_date()
            elif event.key() == Qt.Key_S:
                self.save_file_for_date()

    def save_file_for_date(self):
        selected_date = self.date_time_edit.date()
        filename = self.get_file_path(selected_date)
        content = self.page_content_textedit.toPlainText()
        with open(filename, 'w') as file:
            file.write(content)

    def load_journal(self):
        self.current_directory = os.path.join(
            self.config.file_storage_directory, self.selector.currentText())

        self.load_file_for_date(self.date_time_edit.dateTime())

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

    def goto_previous_date(self):
        current_date = self.date_time_edit.dateTime()
        new_date = current_date.addDays(-1)
        self.date_time_edit.setDateTime(new_date)

    def goto_next_date(self):
        current_date = self.date_time_edit.dateTime()
        new_date = current_date.addDays(1)
        self.date_time_edit.setDateTime(new_date)

    def goto_current_date(self):
        self.date_time_edit.setDateTime(
            QDateTime(QDate.currentDate(), QTime(0, 0, 0)))

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
        directory = os.path.join(
            self.current_directory, year, month)
        filename = os.path.join(directory, day + '.txt')
        os.makedirs(directory, exist_ok=True)
        return filename

    def get_monospace_font(self, font_size):
        font_id = QFontDatabase.addApplicationFont(
            ":/fonts/Inconsolata-Regular.ttf")

        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        else:
            font_family = "monospace"

        font = QFont(font_family, font_size)
        return font


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def load_stylesheet(filename):
    style_file = QFile(filename)
    if style_file.open(QFile.ReadOnly | QFile.Text):
        stream = QTextStream(style_file)
        stylesheet = stream.readAll()
        return stylesheet


if __name__ == '__main__':
    app = QApplication(sys.argv)
    stylesheet_path = resource_path('styles/braindump.qss')
    app.setStyleSheet(load_stylesheet(stylesheet_path))
    window = BraindumpApp()
    window.showFullScreen()
    sys.exit(app.exec_())
