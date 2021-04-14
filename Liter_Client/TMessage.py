from PyQt5.QtWidgets import (QLabel, QTextEdit)
from PyQt5.QtCore import (Qt, QRect)
from PyQt5.QtGui import (QPainter, QFont, QColor, QPen)
import math


class TMessage(QLabel):
    '单条消息'
    def __init__(self, massage, from_me=True, parent=None):
        super(TMessage, self).__init__(parent)
        self.textedit = QTextEdit(self)  # 放置消息的文本框
        self.textedit.setContextMenuPolicy(Qt.NoContextMenu)  # 禁用右键菜单 https://bbs.csdn.net/topics/391545518
        self.text = massage['text'].split('[img]')  # 裁剪出消息
        self.identity = '{}{} {}'.format('√' if massage['from_me'] else '×', massage['from'], massage['time'])  # 发消息人的身份
        self.massage = massage  # 保存整条消息备用
        self.initUI()

    def __str__(self):
        return self.textedit.toPlainText()

    def initUI(self):
        self.textedit.setMaximumWidth(530)  # 限制宽度最大值
        # 不显示滚动条
        self.textedit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textedit.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textedit.setGeometry(70, 35, 8, 25)  # 初始位置以及大小
        self.textedit.setReadOnly(True)  # 只读
        self.textedit.setStyleSheet(("border:0px;background:rgba(0,0,0,0);"))  # 取消背景
        self.font = QFont('msyh')  # 字体
        self.font.setPixelSize(20)
        self.textedit.setFont(self.font)
        self.setText()  # 放入文字
        self.resize(615, self.textedit.height()+50)  # 放入文字后调整组件大小

    def setText(self):
        magic = 20  # 字体像素值
        maxWidth = 0  # 最大宽度
        maxHeight = 0  # 最大高度
        for t in self.text:
            if magic*len(t) <= self.textedit.maximumWidth():
                maxWidth = max(maxWidth, magic*len(t))
            else:
                maxWidth = self.textedit.maximumWidth()
            self.textedit.append(t)
        for t in self.text:
            maxHeight += math.ceil(len(t)/26)
        maxWidth += 10
        maxHeight = 23*maxHeight+10
        self.textedit.resize(maxWidth, maxHeight)

    def paintEvent(self, event):
        '绘制消息框'
        super(TMessage, self).paintEvent(event)
        # 气泡
        bubble_pat = QPainter(self)
        bubble_pat.setPen(QPen(QColor(205, 156, 177), 2))
        bubble_pat.setBrush(QColor(238, 252, 255))
        bubble_pat.setRenderHint(bubble_pat.Antialiasing)
        tr = self.textedit.rect()
        tr.moveTo(self.textedit.pos())
        tr.setTop(tr.top()-5)
        bubble_pat.drawRoundedRect(tr, 10, 10)
        # 个人信息
        identity_pat = QPainter(self)
        identity_pat.setPen(Qt.red)
        identity_pat.setBrush(QColor(229, 229, 229))
        identity_pat.setRenderHint(identity_pat.Antialiasing)
        identity_pat.drawRoundedRect(QRect(10, 25, 50, 50), 25, 25)  # 头像
        identity_pat.setPen(Qt.gray)
        font = QFont('msyh', 10, QFont.Bold)
        font.setPixelSize(14)
        identity_pat.setFont(font)
        identity_pat.drawText(5, 17, self.identity)  # 昵称
