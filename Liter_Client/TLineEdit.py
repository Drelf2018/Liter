from PyQt5.QtCore import (Qt, QPointF)
from PyQt5.QtGui import (QPainter, QColor, QPen, QFont)
from PyQt5.QtWidgets import (QLineEdit, QAction)


class TLineEdit(QLineEdit):
    '自定义的只含底线的文本框'
    def __init__(self, icon: list, parent=None):
        super(TLineEdit, self).__init__(parent)
        # 三种不同颜色的底画线
        self.pen_style = {
            'gray': QPen(QColor(229, 229, 229), 3),
            'dark': QPen(Qt.gray, 3),
            'blue': QPen(QColor(18, 183, 245), 3)
        }
        # 文本框前图标 类型为列表 可放置多个
        self.icon = icon
        self.pen = self.pen_style['gray']
        # 为文本框绑定图标
        self.selectApply = QAction(self)
        self.selectApply.setIcon(icon[0])
        # LeadingPosition 表示图标在左侧
        self.addAction(self.selectApply, self.LeadingPosition)
        # 设置字体字高 微软雅黑
        self.setFont(QFont('msyh', 16))

    def change_icon(self, t):
        '修改图标'
        self.selectApply.setIcon(self.icon[t])
        self.update()

    def paintEvent(self, event):
        '绘制文本框'
        super(TLineEdit, self).paintEvent(event)
        # 利用css代码取消边框和背景
        self.setStyleSheet(("border:0px;background:rgba(0,0,0,0);"))
        # 在文本框底部画线
        pat = QPainter(self)
        pat.setPen(self.pen)
        pat.setRenderHint(pat.Antialiasing)
        pat.drawLine(QPointF(9, self.height()), QPointF(self.width()-5, self.height()))

    def enterEvent(self, QMouseEvent):
        '检测鼠标是否移动至文本框并变色'
        if not self.pen == self.pen_style['blue']:
            self.pen = self.pen_style['dark']
        QMouseEvent.accept()

    def mousePressEvent(self, QMouseEvent):
        '按下文本框 变色'
        self.pen = self.pen_style['blue']
        self.selectApply.setIcon(self.icon[1])
        # QMouseEvent.accept()

    def leaveEvent(self, QMouseEvent):
        '未按下时移开鼠标变色'
        if self.pen == self.pen_style['dark']:
            self.pen = self.pen_style['gray']
        QMouseEvent.accept()
