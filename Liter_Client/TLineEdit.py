from PyQt5.QtCore import (Qt, QPointF, QRect)
from PyQt5.QtGui import (QPainter, QColor, QPen)
from PyQt5.QtWidgets import (QLineEdit, QWidget)


class EXEdit(QLineEdit):
    def __init__(self, parent=None):
        super(EXEdit, self).__init__(parent)

    def enterEvent(self, QMouseEvent):
        QMouseEvent.ignore()

    def mousePressEvent(self, QMouseEvent):
        QMouseEvent.ignore()

    def leaveEvent(self, QMouseEvent):
        QMouseEvent.ignore()

    def focusInEvent(self, focusEvent):
        '获得焦点事件'
        super(EXEdit, self).focusInEvent(focusEvent)
        self.parent().pen = self.parent().pen_style['press']
        self.parent().update()
        focusEvent.accept()

    def focusOutEvent(self, focusEvent):
        '失去焦点事件'
        super(EXEdit, self).focusOutEvent(focusEvent)
        self.parent().pen = self.parent().pen_style['leave']
        self.parent().update()
        focusEvent.accept()


class TLineEdit(QWidget):
    '自定义的只含底线的文本框'
    ACCOUNT = 0
    PASSWORD = 1

    def __init__(self, left, top, width, height, patten=None, parent=None):
        super(TLineEdit, self).__init__(parent)
        self.setGeometry(left, top, width, height)
        self.patten = patten
        self.Edit = EXEdit(self)  # 编辑框
        # 利用css代码取消边框和背景
        self.Edit.setStyleSheet(("border:0px;background:rgba(0,0,0,0);"))
        # 设置位置
        self.Edit.setGeometry(self.height(), 0.05*self.height(), self.width()-self.height()-5, 0.9*self.height())
        # 三种不同颜色的底画线
        self.pen_style = {
            'leave': QPen(QColor(229, 229, 229), 3),
            'enter': QPen(Qt.gray, 3),
            'press': QPen(QColor(18, 183, 245), 3)
        }
        self.pen = self.pen_style['leave']  # 初始画笔

    def change_icon(self, t):
        '修改图标'
        self.selectApply.setIcon(self.icon[t])
        self.update()

    def paintEvent(self, event):
        '绘制文本框'
        pat = QPainter(self)
        pat.setRenderHint(pat.Antialiasing)
        pat.setPen(self.pen)
        pat.drawLine(QPointF(0, self.height()), QPointF(self.width(), self.height()))
        x = int(self.height()/2)
        if self.patten == self.ACCOUNT:
            r1, r2 = int(self.height()/8), int(self.height()*3/16)
            h = int(self.height()-2*r1-r2)//2
            h1, h2 = h+r1, h+2*r1+r2
            pat.drawRoundedRect(QRect(x-r1, h1-r1, 2*r1, 2*r1), r1, r1)
            pat.drawArc(QRect(x-r2, h2-r2, 2*r2, 2*r2), 0, 180*16)
        elif self.patten == self.PASSWORD:
            r = 0.1611*self.height()
            pat.drawArc(QRect(x-r, x-1.65*r, 2*r, 2*r), 20*16, 160*16)
            pat.drawLine(QPointF(int(x-r), int(x-0.65*r)), QPointF(int(x-r), x))
            pat.drawRoundedRect(QRect(x-1.405*r, x, 2.811*r, 1.68*r), 0.38*r, 0.38*r)
        else:
            pat.drawLine(QPointF(0.75*x, x), QPointF(0.25*x, 0.5*x))
            pat.drawLine(QPointF(0.75*x, x), QPointF(0.25*x, 1.5*x))
            pat.drawLine(QPointF(1.25*x, x), QPointF(0.75*x, 0.5*x))
            pat.drawLine(QPointF(1.25*x, x), QPointF(0.75*x, 1.5*x))
            pat.drawLine(QPointF(1.75*x, x), QPointF(1.25*x, 0.5*x))
            pat.drawLine(QPointF(1.75*x, x), QPointF(1.25*x, 1.5*x))

    def enterEvent(self, QMouseEvent):
        '检测鼠标是否移动至文本框并变色'
        if not self.pen == self.pen_style['press']:
            self.pen = self.pen_style['enter']
        self.update()
        QMouseEvent.accept()

    def mousePressEvent(self, QMouseEvent):
        '按下文本框 变色'
        self.pen = self.pen_style['press']
        self.Edit.setFocus()
        self.update()
        QMouseEvent.accept()

    def leaveEvent(self, QMouseEvent):
        '未按下时移开鼠标变色'
        if self.pen == self.pen_style['enter']:
            self.pen = self.pen_style['leave']
        self.update()
        QMouseEvent.accept()

    def focusInEvent(self, focusEvent):
        '获得焦点事件'
        self.pen = self.pen_style['press']
        self.update()
        focusEvent.accept()

    def focusOutEvent(self, focusEvent):
        '失去焦点事件'
        self.pen = self.pen_style['leave']
        self.update()
        focusEvent.accept()
