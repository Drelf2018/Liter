from PyQt5.QtWidgets import (QLabel, QTextEdit)
from PyQt5.QtCore import (Qt, QRect)
from PyQt5.QtGui import (QPainter, QFont, QColor)
import math
import os


class TMessage(QLabel):
    def __init__(self, massage: str, parent=None):
        super(TMessage, self).__init__(parent)
        self.textedit = QTextEdit(self)
        # self.textedit.moveCursor(QTextCursor.End)
        self.text = massage['text'].split('[img]')
        # self.text = ['你在干嘛', '吃了吗', '我好想你呀', '为什么不理我明明我这么关心你你却对我不搭理为什么为什么为什么']
        self.initUI()

    def initUI(self):
        os.chdir(os.path.dirname(__file__))
        # self.setPixmap(QPixmap('img\\bg.jpg'))
        self.textedit.setMaximumWidth(530)
        self.textedit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textedit.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textedit.setGeometry(70, 40, 8, 25)
        self.textedit.setStyleSheet(("border:0px;background:rgba(0,0,0,0);"))
        self.font = QFont('msyh')
        self.font.setPixelSize(20)
        self.textedit.setFont(self.font)
        self.setText()
        self.resize(615, self.textedit.height()+60)

    def setText(self):
        magic = 20
        maxWidth = 0
        maxHeight = 0
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
        super(TMessage, self).paintEvent(event)
        bubble_pat = QPainter(self)
        bubble_pat.setPen(Qt.NoPen)
        bubble_pat.setBrush(QColor(210, 210, 210))
        bubble_pat.setRenderHint(bubble_pat.Antialiasing)
        tr = self.textedit.rect()
        tr.moveTo(self.textedit.pos())
        tr.setTop(tr.top()-5)
        bubble_pat.drawRoundedRect(tr, 16, 16)

        identity_pat = QPainter(self)
        identity_pat.setPen(Qt.red)
        identity_pat.setBrush(Qt.gray)
        identity_pat.setRenderHint(identity_pat.Antialiasing)
        identity_pat.drawRoundedRect(QRect(10, 30, 50, 50), 25, 25)
        identity_pat.setPen(Qt.gray)
        identity_pat.setFont(QFont('msyh', 8))
        identity_pat.drawText(5, 22, '【管理员】Drelf 2021/04/12 23:36')
