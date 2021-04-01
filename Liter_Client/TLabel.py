from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import (Qt, QRectF)
from PyQt5.QtGui import (QImage, QBrush, QPainter)
from TPath import RoundPath


class TLabel(QLabel):
    def __init__(self, r: list, img=None, parent=None):
        super(TLabel, self).__init__(parent)
        self.r = r
        if img:
            self.img = img

    def paintEvent(self, event):
        pat = QPainter(self)
        pat.setPen(Qt.NoPen)
        brush = QBrush()
        if self.img:
            self.img = QImage(self.img).scaled(self.width(), self.height())
            brush.setTextureImage(self.img)
        else:
            brush = QBrush(Qt.white)
        pat.setBrush(brush)
        path = RoundPath(QRectF(0, 0, self.width(), self.height()), self.r[0], self.r[1], self.r[2], self.r[3])
        pat.drawPath(path)
