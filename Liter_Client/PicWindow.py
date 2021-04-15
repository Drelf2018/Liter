from PyQt5.QtCore import (Qt, QRectF, QRect)
from PyQt5.QtGui import (QPainter, QPainterPath, QColor, QBrush)
from PyQt5.QtWidgets import QWidget
import numpy as np
from PIL import ImageQt


class PicWindow(QWidget):
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
    def __init__(self, img, parent=None):
        super(PicWindow, self).__init__(parent)
        im = img.convert('RGBA')
        alpha = im.split()[3]
        bgmask = alpha.point(lambda x: 255-x)
        im.paste((255, 255, 255), None, bgmask)
        self.img = ImageQt.ImageQt(im)
        self.alpha = alpha
        self.color = QColor(0, 0, 0, 255)
        # m_drag 用于判断是否可以移动窗口
        self.m_drag = False
        self.m_DragPosition = None
        # 扩散 圆角
        self.s = 8
        self.r = 5
        # 设置窗口大小为界面大小加上两倍阴影扩散距离
        self.resize(img.width+2*self.s, img.height+2*self.s)
        # 设置窗口无边框和背景透明
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)

    def paintEvent(self, event):
        # 画阴影
        shadow_pat = QPainter(self)
        shadow_pat.setRenderHint(shadow_pat.Antialiasing)

        for i in np.arange(0, self.s+0.2, 0.2):
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
            self.color.setAlpha(20*(1-i**0.5*0.3535))
            shadow_pat.setPen(self.color)
            shadow_pat.drawPath(shadow_path)

        brush = QBrush()
        brush.setTextureImage(self.img)
        shadow_pat.save()
        shadow_pat.translate(self.s, self.s)  # 移动画笔 https://tieba.baidu.com/p/3769108658
        shadow_pat.setPen(Qt.NoPen)
        shadow_pat.setBrush(brush)
        shadow_pat.drawRoundedRect(QRect(0, 0, self.width()-2*self.s, self.height()-2*self.s), self.r, self.r)
        shadow_pat.restore()

    def mousePressEvent(self, QMouseEvent):
        '鼠标点击 检测点击位置判断是否可移动\n清除所有文本框的选中状态'
        if QMouseEvent.button() == Qt.LeftButton:
            # 鼠标点击点的相对位置
            self.m_DragPosition = QMouseEvent.globalPos()-self.pos()
            # print((self.m_DragPosition.x(), self.m_DragPosition.y()))
            if self.s < self.m_DragPosition.y() < self.height() - self.s:
                self.m_drag = True

    def mouseMoveEvent(self, QMouseEvent):
        '按住标题栏可移动窗口'
        if self.m_drag:
            self.move(QMouseEvent.globalPos()-self.m_DragPosition)
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_drag = False
        QMouseEvent.accept()

    def keyPressEvent(self, keyEvent):
        if keyEvent.key() == Qt.Key_Escape:
            self.close()

    def mouseDoubleClickEvent(self, QMouseEvent):
        if QMouseEvent.buttons() == Qt.LeftButton:
            self.close()
