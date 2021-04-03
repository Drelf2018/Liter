from PyQt5.QtCore import (Qt, QRectF, pyqtSignal)
from PyQt5.QtGui import (QPainter, QColor, QPainterPath)
from PyQt5.QtWidgets import QWidget
from .TLineEdit import TLineEdit
from .TLabel import TLabel
from .TPath import RoundPath
import numpy as np


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
    _signal = pyqtSignal()

    def __init__(self, width, height, r, s, alpha, color, space, img=None, parent=None):
        super(RoundShadow, self).__init__(parent)
        self.r = r
        self.s = s
        self.alpha = alpha
        self.color = color
        self.space = space
        self.img = img
        # m_drag 用于判断是否可以移动窗口
        self.m_drag = False
        self.m_DragPosition = None
        # 设置窗口大小为界面大小加上两倍阴影扩散距离
        self.resize(width+2*s, height+2*s)
        # 设置窗口无边框和背景透明
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        # 设置圆角背景图片
        self.bglab = TLabel([0, self.r, self.r, 0], img=img, parent=self)
        self.bglab.setGeometry(self.s, self.s+40, width, height-40)
        self._signal.connect(self.close)

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
        round_pat.setBrush(QColor(187, 222, 251))  # 灰色笔刷
        title_path = RoundPath(QRectF(self.s, self.s, self.width()-2*self.s, 40), self.r, 0, 0, self.r)
        round_pat.drawPath(title_path)

    def mousePressEvent(self, QMouseEvent):
        '鼠标点击 检测点击位置判断是否可移动\n清楚所有文本框的选中状态'
        if QMouseEvent.button() == Qt.LeftButton:
            # 鼠标点击点的相对位置
            self.m_DragPosition = QMouseEvent.globalPos()-self.pos()
            print((self.m_DragPosition.x(), self.m_DragPosition.y()))
            if self.m_DragPosition.y() <= 40 + self.s:
                self.m_drag = True

        LineEdit = self
        while LineEdit and not isinstance(LineEdit, TLineEdit):
            LineEdit = LineEdit.childAt(QMouseEvent.x(), QMouseEvent.y())
        LineEdits = self.findChildren(TLineEdit)
        for le in LineEdits:
            if not le == LineEdit:
                le.clearFocus()
                le.pen = le.pen_style['gray']
                le.change_icon(0)
        QMouseEvent.accept()

    def mouseMoveEvent(self, QMouseEvent):
        '按住标题栏可移动窗口'
        if self.m_drag:
            self.move(QMouseEvent.globalPos()-self.m_DragPosition)
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_drag = False
        QMouseEvent.accept()
