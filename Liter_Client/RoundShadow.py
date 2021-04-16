from PyQt5.QtCore import (Qt, QRectF)
from PyQt5.QtGui import (QPainter, QColor, QPainterPath, QFont)
from PyQt5.QtWidgets import QWidget
from .TLabel import TLabel
from .TPushButton import TPushButton
from .TPath import RoundPath
import numpy as np
import os


class RoundShadow(QWidget):
    '''
    圆角边框类\n
    width, height 去掉边框后界面的长宽\n
    r 界面圆角半径\n
    s 阴影扩散范围\n
    alpha 阴影可见度变化函数\n
    color 颜色\n
    space 自变量(距离界面距离，取值[0-s])每次增加距离\n
    img 背景图片
    '''
    def __init__(self, width, height, r=16, s=8, alpha=lambda i: 20*(1-i**0.5*0.3535), color=QColor(0, 0, 0, 255), space=0.2, img=None, title=None, parent=None):
        super(RoundShadow, self).__init__(parent)
        self.r = r
        self.s = s
        self.alpha = alpha
        self.color = color
        self.space = space
        self.img = img
        self.title = title
        # m_drag 用于判断是否可以移动窗口
        self.m_drag = False
        self.m_DragPosition = None
        # 设置窗口大小为界面大小加上两倍阴影扩散距离
        self.resize(width+2*s, height+2*s)
        # 设置窗口无边框和背景透明
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        # 切换目录
        os.chdir(os.path.dirname(__file__))
        # 设置最小化按钮位置和大小 绑定事件
        self.minButton = TPushButton(img=['img/min1.png', 'img/min2.png', 'img/min2.png'], parent=self)
        self.minButton.setGeometry(self.width()-2*self.s-60, 16, 26, 26)
        self.minButton.clicked.connect(self.showMinimized)
        # 设置关闭按钮位置和大小 绑定事件
        self.closeButton = TPushButton(img=['img/close1.png', 'img/close2.png', 'img/close2.png'], parent=self)
        self.closeButton.setGeometry(self.width()-2*self.s-30, 16, 26, 26)
        self.closeButton.clicked.connect(self.close)
        # 设置圆角背景图片
        self.bglab = TLabel((0, self.r, self.r, 0), img=img, parent=self)
        self.bglab.setGeometry(self.s, self.s+40, width, height-40)

    def setTitle(self, title):
        self.title = title
        self.update()

    def paintEvent(self, event):
        # 画阴影
        shadow_pat = QPainter(self)
        shadow_pat.setRenderHint(shadow_pat.Antialiasing)

        for i in np.arange(0, self.s+self.space, self.space):
            '''
            i 表示距离界面的距离\n
            扩散距离为 s 因此 i 的取值从[0-s]
            每次生成一个可见度不同的圆角矩形
            随着 i 的增大 alpha 函数值下降可使阴影渐变
            '''
            shadow_path = QPainterPath()
            shadow_path.setFillRule(Qt.WindingFill)
            ref = QRectF(self.s-i, self.s-i, self.width()-(self.s-i)*2, self.height()-(self.s-i)*2)
            shadow_path.addRoundedRect(ref, self.r, self.r)
            self.color.setAlpha(self.alpha(i))
            shadow_pat.setPen(self.color)
            shadow_pat.drawPath(shadow_path)
        # 画圆角标题栏
        round_pat = QPainter(self)
        round_pat.setRenderHint(round_pat.Antialiasing)  # 抗锯齿
        round_pat.setPen(Qt.transparent)  # 透明
        round_pat.setBrush(QColor(187, 222, 255))  # 蓝色笔刷
        title_path = RoundPath(QRectF(self.s, self.s, self.width()-2*self.s, 40), (self.r, 0, 0, self.r))
        round_pat.drawPath(title_path)
        # 画图标和标题
        x, y = self.r+8, self.r+23
        icon_pat = QPainter(self)
        icon_pat.setRenderHint(icon_pat.Antialiasing)  # 抗锯齿
        icon_pat.setFont(QFont('微软雅黑', 18, QFont.Bold))
        icon_pat.setPen(QColor(0, 0, 0, 25))  # 黑笔
        icon_pat.drawText(x-3, y+3, 'Liter')  # 画阴影
        icon_pat.setPen(QColor(0, 0, 0, 75))  # 黑笔
        icon_pat.drawText(x-2, y+2, 'Liter')  # 画阴影
        icon_pat.setPen(QColor(0, 0, 0, 125))  # 黑笔
        icon_pat.drawText(x-1, y+1, 'Liter')  # 画阴影
        icon_pat.setPen(Qt.white)  # 白笔
        icon_pat.drawText(x, y, 'Liter')  # 画字体
        # 画标题
        if self.title:
            if isinstance(self.title, tuple):
                color, font, text = self.title
            else:
                color = Qt.white
                font = QFont('微软雅黑', 14, QFont.Bold)
                text = self.title
            title_pat = QPainter(self)
            title_pat.setRenderHint(title_pat.Antialiasing)  # 抗锯齿
            title_pat.setFont(font)
            if color == Qt.white:
                title_pat.setPen(QColor(0, 0, 0, 25))  # 黑笔
                title_pat.drawText(QRectF(self.s-3, self.s+1, self.width()-2*self.s, 40), Qt.AlignCenter, text)  # 画阴影
                title_pat.setPen(QColor(0, 0, 0, 75))  # 黑笔
                title_pat.drawText(QRectF(self.s-2, self.s, self.width()-2*self.s, 40), Qt.AlignCenter, text)  # 画阴影
                title_pat.setPen(QColor(0, 0, 0, 125))  # 黑笔
                title_pat.drawText(QRectF(self.s-1, self.s-1, self.width()-2*self.s, 40), Qt.AlignCenter, text)  # 画阴影
            title_pat.setPen(color)  # 白笔
            title_pat.drawText(QRectF(self.s, self.s-2, self.width()-2*self.s, 40), Qt.AlignCenter, text)  # 画字体

    def mousePressEvent(self, QMouseEvent):
        '鼠标点击 检测点击位置判断是否可移动\n清除所有文本框的选中状态'
        if QMouseEvent.button() == Qt.LeftButton:
            # 鼠标点击点的相对位置
            self.m_DragPosition = QMouseEvent.globalPos()-self.pos()
            # print((self.m_DragPosition.x(), self.m_DragPosition.y()))
            if self.m_DragPosition.y() <= 39 + self.s:
                self.m_drag = True

    def mouseMoveEvent(self, QMouseEvent):
        '按住标题栏可移动窗口'
        if self.m_drag:
            self.move(QMouseEvent.globalPos()-self.m_DragPosition)
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_drag = False
        QMouseEvent.accept()
