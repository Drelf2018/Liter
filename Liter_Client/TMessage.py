from PyQt5.QtWidgets import (QLabel, QTextEdit)
from PyQt5.QtCore import (Qt, QRect)
from PyQt5.QtGui import (QPainter, QFont, QColor)
import math


class TMessage(QLabel):
    def __init__(self, massage, from_me=True, parent=None):
        super(TMessage, self).__init__(parent)
        # self.setPixmap(QPixmap('D:\\Code\\python\\TCP\\Liter\\Liter_Client\\img\\bg.jpg'))
        self.textedit = QTextEdit(self)
        self.textedit.setContextMenuPolicy(Qt.NoContextMenu)  # https://bbs.csdn.net/topics/391545518
        self.text = massage['text'].split('[img]')
        self.identity = '{} {}'.format(massage['from'], massage['time'])
        self.massage = massage
        self.initUI()

    def __str__(self):
        return self.textedit.toPlainText()

    def initUI(self):
        self.textedit.setMaximumWidth(530)
        self.textedit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textedit.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textedit.setGeometry(70, 35, 8, 25)
        self.textedit.setReadOnly(True)
        self.textedit.setStyleSheet(("border:0px;background:rgba(0,0,0,0);"))
        self.font = QFont('msyh')
        self.font.setPixelSize(20)
        self.textedit.setFont(self.font)
        self.setText()
        self.resize(615, self.textedit.height()+50)

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
        identity_pat.drawRoundedRect(QRect(10, 25, 50, 50), 25, 25)
        identity_pat.setPen(Qt.gray)
        font = QFont('msyh')
        font.setPixelSize(14)
        identity_pat.setFont(font)
        identity_pat.drawText(5, 17, self.identity)
