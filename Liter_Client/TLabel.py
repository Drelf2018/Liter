from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import (QImage, QBrush, QPainter)
from TPath import RoundPath
import cv2


class TLabel(QLabel):
    '''
    带圆角的展示框\n
    r 圆角半径，类型为列表，从左上开始逆时针顺序\n
    img 要展示的图片
    '''
    def __init__(self, r: list, img=None, color=Qt.white, parent=None):
        super(TLabel, self).__init__(parent)
        self.r = r
        self.img = img
        self.color = color
        if img:
            src = cv2.imread(img)  # opencv读取图片
            img = cv2.GaussianBlur(src, (0, 0), 10)  # 高斯模糊
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # opencv读取的bgr格式图片转换成rgb格式
            self.img = QImage(img[:], img.shape[1], img.shape[0], img.shape[1] * 3, QImage.Format_RGB888)  # pyqt5转换成自己能放的图片格式

    def paintEvent(self, event):
        # 画笔设置不描边
        pat = QPainter(self)
        pat.setPen(Qt.NoPen)
        brush = QBrush()
        # 画刷为图片 若不存在为纯色
        if self.img:
            self.img = QImage(self.img).scaled(self.width(), self.height())
            brush.setTextureImage(self.img)
        else:
            brush = QBrush(self.color)
        # 喷漆
        pat.setBrush(brush)
        path = RoundPath(self.rect(), self.r[0], self.r[1], self.r[2], self.r[3])
        pat.drawPath(path)
