from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTextEdit, QMenu, QAction

from braindump_widget import BraindumpWidget


class BraindumpTextEdit(BraindumpWidget, QTextEdit):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setAlignment(Qt.AlignCenter)
        self.setFont(self.get_monospace_font(16))
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textChanged.connect(self.hide_vertical_scrollbar)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)
        self.paste_no_formatting_action = QAction(
            "Paste with No Formatting", self)
        self.paste_no_formatting_action.triggered.connect(
            self.pasteNoFormatting)
        self.standard_context_menu = self.createStandardContextMenu()

    def pasteNoFormatting(self):
        clipboard = QApplication.clipboard()
        text = clipboard.text()
        self.insertPlainText(text)

    def showContextMenu(self, pos):
        context_menu = self.createStandardContextMenu()
        context_menu.addSeparator()
        context_menu.addAction(self.paste_no_formatting_action)
        context_menu.exec_(self.mapToGlobal(pos))

    def hide_vertical_scrollbar(self):
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def createContextMenu(self):
        self.context_menu = QMenu(self)

        self.context_menu.addActions(
            self.context_menu.actions() +
            QApplication.instance().allWidgets()[0].createStandardContextMenu().actions())

        paste_without_formatting_action = QAction(
            "Paste Without Formatting", self)
        paste_without_formatting_action.triggered.connect(
            self.pasteWithoutFormatting)
        context_menu.addAction(paste_without_formatting_action)

        return context_menu

    def pasteWithoutFormatting(self):
        clipboard = QApplication.clipboard()
        text = clipboard.text()
        active_widget = QApplication.focusWidget()

        if isinstance(active_widget, QTextEdit):
            active_widget.insertPlainText(text)

    def contextMenuEvent(self, event):
        context_menu = self.createContextMenu()
        context_menu.exec_(event.globalPos())
