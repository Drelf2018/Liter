from PyQt5.QtWidgets import (QLabel, QTextEdit)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import (QImage, QBrush, QPainter, QFont, QPixmap, QTextCursor)
from .TPath import RoundPath
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
        self.setPixmap(QPixmap('img\\bg.jpg'))
        self.textedit.setMaximumWidth(535)
        self.textedit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textedit.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textedit.setGeometry(70, 30, 8, 25)
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
            maxHeight += math.ceil(magic*len(t)/maxWidth)
        maxWidth += 10
        print(maxWidth, maxHeight)
        print(self.textedit.verticalScrollBar().pageStep())
        self.textedit.resize(maxWidth, 25*maxHeight+10)
