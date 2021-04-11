from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import (QImage, QBrush, QPainter)
from .TPath import RoundPath


class TPushButton(QPushButton):
    '''
    r 按钮圆角半径\n
    img 按钮处于三种状态时图片\n
    color 不选用 img 时三种状态下颜色\n
    '''
    def __init__(self, r=(0, 0, 0, 0), img=None, color=[Qt.gray, Qt.white, Qt.blue], parent=None):
        super(TPushButton, self).__init__(parent)
        self.r = r
        self.img = img
        self.color = color
        self.choice = 0
        self.text = None

    def setTitle(self, text: tuple):
        self.text = text

    def enterEvent(self, QMouseEvent):
        self.choice = 1

    def mousePressEvent(self, QMouseEvent):
        self.choice = 2
        super(TPushButton, self).mousePressEvent(QMouseEvent)

    def mouseReleaseEvent(self, QMouseEvent):
        self.choice = 1
        super(TPushButton, self).mouseReleaseEvent(QMouseEvent)

    def leaveEvent(self, QMouseEvent):
        self.choice = 0

    def paintEvent(self, event):
        # 画笔设置不描边
        pat = QPainter(self)
        pat.setPen(Qt.NoPen)
        brush = QBrush()
        pat.setRenderHint(pat.Antialiasing)  # 抗锯齿
        # 画刷为图片 若不存在为纯色
        if self.img:
            self.img[self.choice] = QImage(self.img[self.choice]).scaled(self.width(), self.height())
            brush.setTextureImage(self.img[self.choice])
        else:
            brush = QBrush(self.color[self.choice])
        # 喷漆
        pat.setBrush(brush)
        path = RoundPath(self.rect(), self.r)
        pat.drawPath(path)
        # 文字
        if self.text:
            color, font, text = self.text
            pat.setPen(color)
            pat.setFont(font)
            pat.drawText(self.rect(), Qt.AlignCenter, text)
