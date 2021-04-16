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
    def __init__(self, left, top, width, height, parent=None):
        super(TLineEdit, self).__init__(parent)
        self.setGeometry(left, top, width, height)
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
        pat.setPen(self.pen)
        pat.setRenderHint(pat.Antialiasing)
        pat.drawRoundedRect(QRect(5, 5, self.height()-10, self.height()-10), self.height()-5, self.height()-5)
        pat.drawLine(QPointF(0, self.height()), QPointF(self.width(), self.height()))

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
