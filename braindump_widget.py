from PyQt5.QtGui import QFont, QFontDatabase


class BraindumpWidget:
    def get_monospace_font(self, font_size):
        font_id = QFontDatabase.addApplicationFont(
            ":/fonts/Inconsolata-Regular.ttf")

        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        else:
            font_family = "monospace"

        font = QFont(font_family, font_size)
        return font
