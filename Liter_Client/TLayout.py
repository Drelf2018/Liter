from PyQt5.QtWidgets import (QHBoxLayout, QVBoxLayout)
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt
from .TPath import RoundPath


class THBoxLayout(QHBoxLayout):
    def __init__(self, r=(0, 0, 0, 0), parent=None):
        super(THBoxLayout, self).__init__(parent)
        self.r = r

    def paintEvent(self, event):
        # 画笔设置不描边
        pat = QPainter(self)
        pat.setPen(Qt.NoPen)
        pat.setRenderHint(pat.Antialiasing)  # 抗锯齿
        pat.brush(Qt.black)
        # 喷漆
        path = RoundPath(self.rect(), self.r)
        pat.drawPath(path)
