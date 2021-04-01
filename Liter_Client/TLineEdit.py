from PyQt5.QtCore import (Qt, QPointF)
from PyQt5.QtGui import (QPainter, QColor, QPen, QFont)
from PyQt5.QtWidgets import (QLineEdit, QAction)


class TLineEdit(QLineEdit):
    def __init__(self, icon: list, parent=None):
        super(TLineEdit, self).__init__(parent)
        self.pen_style = {
            'gray': QPen(QColor(229, 229, 229), 3),
            'dark': QPen(Qt.gray, 3),
            'blue': QPen(QColor(18, 183, 245), 3)
        }
        self.icon = icon
        self.pen = self.pen_style['gray']
        self.selectApply = QAction(self)
        self.selectApply.setIcon(icon[0])
        self.addAction(self.selectApply, self.LeadingPosition)
        self.setFont(QFont('msyh', 15, QFont.Bold))

    def change_icon(self, t):
        self.selectApply.setIcon(self.icon[t])

    def paintEvent(self, event):
        # super(TLineEdit, self).paintEvent(event)
        self.setStyleSheet(("border:0px solid pink"))
        pat = QPainter(self)
        pat.setPen(self.pen)
        pat.setRenderHint(pat.Antialiasing)
        pat.drawLine(QPointF(9, self.height()), QPointF(self.width()-6, self.height()))

    def enterEvent(self, QMouseEvent):
        self.pen = self.pen_style['dark']
        QMouseEvent.accept()

    def mousePressEvent(self, QMouseEvent):
        '鼠标点击 检测点击位置判断是否可移动'
        self.pen = self.pen_style['blue']
        self.selectApply.setIcon(self.icon[1])
        QMouseEvent.accept()

    def leaveEvent(self, QMouseEvent):
        if self.pen == self.pen_style['dark']:
            self.pen = self.pen_style['gray']
        QMouseEvent.accept()
