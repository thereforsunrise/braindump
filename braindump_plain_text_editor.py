from PyQt5.QtWidgets import QTextEdit


class BraindumpPlainTextEditor(QTextEdit):
    def insertFromMimeData(self, source):
        self.insertPlainText(source.text())
