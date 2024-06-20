import argparse
import logging
import sys
import signal

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QHBoxLayout
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
        logging.info(f"Braindump started")

        super().__init__()

        self.config = BraindumpConfig.load_config()

        self.initUI()

        self.database = BraindumpDatabase(BraindumpConfig.db_file())

        self.email_worker = BraindumpEmailWorker(self.config)
        self.email_thread = QThread()
        self.email_worker.moveToThread(self.email_thread)

        self.email_worker.send_error.connect(self.handle_send_error)
        self.email_worker.emails_sent.connect(self.handle_emails_sent)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.start_email_thread)

        interval = self.config.getint("Email", "interval")
        logging.info(f"Email interval set to {interval}")
        self.timer.start(interval)

        self.email_thread.start()

    def start_email_thread(self):
        logging.debug(f"Started email thread")

        if not self.email_thread.isRunning():
            self.email_thread.start()
        self.email_worker.send_emails(self.database.get_unsent_notes())

    def initUI(self):
        self.setWindowTitle("Braindump")

        self.textEdit = BraindumpPlainTextEditor(self)

        font_family = self.config.get('Interface', 'font_family')
        font_size = self.config.getint('Interface', 'font_size')

        self.textEdit.setFont(QFont(font_family, font_size))
        self.textEdit.setStyleSheet(
            "QTextEdit { color: white; background-color: #282a36; border: 0px; padding: 20px; }"
        )
        self.textEdit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textEdit.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        layout = QVBoxLayout()
        layout.addWidget(self.textEdit)

        centralWidget = QWidget(self)
        centralWidget.setLayout(layout)
        centralWidget.setStyleSheet("background-color: #282a36;")

        hLayout = QHBoxLayout()
        hLayout.addStretch(1)
        hLayout.addWidget(centralWidget, 2)
        hLayout.addStretch(1)

        mainWidget = QWidget(self)
        mainWidget.setLayout(hLayout)
        mainWidget.setStyleSheet("background-color: #282a36;")
        self.setCentralWidget(mainWidget)

        self.showFullScreen()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_S and (event.modifiers() & Qt.ControlModifier):
            self.save_note()

    def save_note(self):
        body = self.textEdit.toPlainText()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        note_id = self.database.add_note(body, timestamp)
        logging.info(f"Saved note with id {note_id}")
        self.textEdit.clear()

    def handle_send_error(self, error_message, note_ids):
        note_ids_str = ",".join(str(note_id) for note_id in note_ids)

        if note_ids_str:
            logging.info(f"Problem sending notes {
                         error_message}: {note_ids_str}")

    def handle_emails_sent(self, note_ids):
        self.database.mark_notes_as_sent(note_ids)

        note_ids_str = ",".join(str(note_id) for note_id in note_ids)
        if note_ids_str:
            logging.info(f"Notes sent sucessfully: {note_ids_str}")

    def closeEvent(self, event):
        self.email_thread.quit()
        self.email_thread.wait()
        event.accept()


def signal_handler(sig, frame):
    logging.info("Exiting gracefully...")
    QApplication.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Braindump CLI")
    parser.add_argument(
        '--log-level',
        type=str,
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        default='INFO',
        help='Set the logging level'
    )
    args = parser.parse_args()

    app = QApplication(sys.argv)
    app.setStyleSheet("QMainWindow { background-color: #282a36; }")
    logging.basicConfig(
        filename=BraindumpConfig.log_file(),
        filemode="a",
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=getattr(logging, args.log_level),
    )

    signal.signal(signal.SIGINT, signal_handler)

    braindump = Braindump()

    sys.exit(app.exec_())
