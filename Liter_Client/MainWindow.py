import os
from .TLabel import TLabel
# from .TLineEdit import TLineEdit
from .TPushButton import TPushButton
from .RoundShadow import RoundShadow
from .TMessage import TMessage
from PyQt5.QtCore import Qt
from PyQt5.QtGui import (QColor, QFont)
from PyQt5.QtWidgets import (QFrame, QVBoxLayout, QHBoxLayout, QScrollArea, QWidget)


class MainWindow(RoundShadow):
    def __init__(self, connecter):
        super(MainWindow, self).__init__(820, 640, 16, 8, lambda x: 20*(1-x**0.5*0.3535), QColor(0, 0, 0, 255), 0.2, None, 'Liter')
        self.connecter = connecter
        self.connecter.setSignal(self.signal)
        self.tt = None
        self.initUI()

    def initUI(self):
        # 切换目录
        os.chdir(os.path.dirname(__file__))
        # 设置标题
        self.setWindowTitle('MainWindow')
        # 设置最小化按钮位置和大小 绑定事件
        minButton = TPushButton(img=['img/min1.png', 'img/min2.png', 'img/min2.png'], parent=self)
        minButton.setGeometry(759, 16, 26, 26)
        minButton.clicked.connect(self.showMinimized)
        # 设置关闭按钮位置和大小 绑定事件
        closeButton = TPushButton(img=['img/close1.png', 'img/close2.png', 'img/close2.png'], parent=self)
        closeButton.setGeometry(790, 16, 26, 26)
        closeButton.clicked.connect(self.close)

        # lab1 = TLabel(color=QColor(255, 0, 0, 155))
        massageWidget = QWidget()
        massageWidget.setWindowFlags(Qt.FramelessWindowHint)
        mwheight = 0
        for i in range(26, 250, 26):
            tm = TMessage({'text': '草'*i}, parent=massageWidget)
            tm.move(0, mwheight)
            mwheight += tm.height()
        massageWidget.setMinimumSize(615, mwheight)
        scroll2 = QScrollArea()
        scroll2.setWidget(massageWidget)
        scroll2.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll2.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll2.setFrameShape(QFrame.NoFrame)

        lab2 = TLabel((0, 16, 0, 0), color=QColor(0, 255, 0, 155))
        sendButton = TPushButton(r=(8, 8, 8, 8), color=[QColor(7, 188, 252), QColor(31, 200, 253), QColor(31, 200, 253)], parent=lab2)
        sendButton.setTitle((QColor(255, 255, 255), QFont('msyh', 11), '发送'))
        sendButton.clicked.connect(lambda: self.connecter.send(''))
        sendButton.setGeometry(505, 120, 100, 40)

        showbox = QVBoxLayout()
        topicbox = QVBoxLayout()
        hbox = QHBoxLayout()
        showbox.setSpacing(0)
        topicbox.setSpacing(0)
        hbox.setSpacing(0)

        # showbox.addWidget(lab1, 23)
        showbox.addWidget(scroll2, 23)
        showbox.addWidget(lab2, 9)

        topics = self.connecter.results.pop(0)
        topicWidget = QWidget()
        topicWidget.setWindowFlags(Qt.FramelessWindowHint)
        topicWidget.setMinimumSize(205, 275*len(topics))
        cnt = 0
        for topic in topics:
            t = TLabel(color=QColor(0, 0, 100+50*cnt, 155), text=(Qt.white, QFont('msyh', 11), topic['name']), parent=topicWidget)
            t.setGeometry(0, 275*cnt, 205, 275)
            cnt += 1

        scroll = QScrollArea()
        scroll.setWidget(topicWidget)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setFrameShape(QFrame.NoFrame)

        moreButton = TPushButton(r=(0, 0, 16, 0), color=[QColor(7, 188, 252), QColor(31, 200, 253), QColor(31, 200, 253)])
        moreButton.setTitle((QColor(255, 255, 255), QFont('msyh', 11), '更多'))
        moreButton.setMinimumSize(205, 45)

        topicbox.addWidget(scroll, 2)
        topicbox.addWidget(moreButton, 1)
        hbox.addLayout(showbox, 3)
        hbox.addLayout(topicbox, 1)
        hbox.setContentsMargins(0, 0, 0, 0)

        self.bglab.setLayout(hbox)
