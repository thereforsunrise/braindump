import logging
import sys

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QHBoxLayout,
    QSpacerItem,
    QSizePolicy,
)
from PyQt5.QtCore import Qt, QTimer, QThread
from PyQt5.QtGui import QFont

from datetime import datetime

from braindump_config import BraindumpConfig
from braindump_database import BraindumpDatabase
from braindump_email_worker import BraindumpEmailWorker
from braindump_plain_text_editor import BraindumpPlainTextEditor


class Braindump(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

        self.config = BraindumpConfig()
        self.database = BraindumpDatabase(self.config.db_file)

        self.email_worker = BraindumpEmailWorker(self.config.config)
        self.email_thread = QThread()
        self.email_worker.moveToThread(self.email_thread)

        self.email_worker.send_error.connect(self.handle_send_error)
        self.email_worker.emails_sent.connect(self.handle_emails_sent)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.start_email_thread)
        self.timer.start(60000)

        self.email_thread.start()

    def start_email_thread(self):
        if not self.email_thread.isRunning():
            self.email_thread.start()
        self.email_worker.send_emails(self.database.get_unsent_notes())

    def initUI(self):
        self.setWindowTitle("Braindump")

        self.textEdit = BraindumpPlainTextEditor(self)
        self.textEdit.setFont(QFont("Monospace", 24))
        self.textEdit.setStyleSheet(
            "QTextEdit { color: white; background-color: black; padding: 20px; }"
        )
        self.textEdit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textEdit.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        layout = QVBoxLayout()
        layout.addWidget(self.textEdit)

        centralWidget = QWidget(self)
        centralWidget.setLayout(layout)
        centralWidget.setStyleSheet("background-color: black;")

        hLayout = QHBoxLayout()
        hLayout.addSpacerItem(
            QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        )
        hLayout.addWidget(centralWidget)
        hLayout.addSpacerItem(
            QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        )

        mainWidget = QWidget(self)
        mainWidget.setLayout(hLayout)
        mainWidget.setStyleSheet("background-color: black;")
        self.setCentralWidget(mainWidget)

        self.showFullScreen()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_S and (event.modifiers() & Qt.ControlModifier):
            self.save_note()

    def save_note(self):
        body = self.textEdit.toPlainText()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.database.add_note(body, timestamp)
        self.textEdit.clear()

    def handle_send_error(self, error_message, note_ids):
        note_ids_str = ",".join(str(note_id) for note_id in note_ids)

        logging.info(f"Problem sending notes {error_message}: {note_ids_str}")

    def handle_emails_sent(self, note_ids):
        self.database.mark_notes_as_sent(note_ids)

        note_ids_str = ",".join(str(note_id) for note_id in note_ids)
        logging.info(f"Notes sent sucessfully: {note_ids_str}")

    def closeEvent(self, event):
        self.email_thread.quit()
        self.email_thread.wait()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet("QMainWindow { background-color: black; }")
    braindump = Braindump()
    logging.basicConfig(
        filename=braindump.config.log_file,
        filemode="a",
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=logging.DEBUG,
    )
    sys.exit(app.exec_())
