import os
from .TLabel import TLabel
# from .TLineEdit import TLineEdit
from .TPushButton import TPushButton
from .RoundShadow import RoundShadow
from PyQt5.QtGui import (QColor, QFont)
from PyQt5.QtWidgets import (QHBoxLayout, QVBoxLayout)


class MainWindow(RoundShadow):
    def __init__(self, connecter):
        super(MainWindow, self).__init__(820, 640, 16, 8, lambda x: 20*(1-x**0.5*0.3535), QColor(0, 0, 0, 255), 0.2, None, 'Liter')
        self.connecter = connecter
        self.connecter.setSignal(self.signal)
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

        lab1 = TLabel([0, 0, 0, 0], color=QColor(255, 0, 0, 155))
        lab2 = TLabel([0, 16, 0, 0], color=QColor(0, 255, 0, 155))
        lab3 = TLabel([0, 0, 16, 0], color=QColor(0, 0, 255, 155))
        sendButton = TPushButton(r=[8, 8, 8, 8], color=[QColor(7, 188, 252), QColor(31, 200, 253), QColor(31, 200, 253)], parent=lab2)
        sendButton.setTitle((QColor(255, 255, 255), QFont('msyh', 11), '发送'))
        sendButton.clicked.connect(lambda: self.connecter.send(''))
        sendButton.setGeometry(505, 120, 100, 40)
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        vbox.setSpacing(0)
        hbox.setSpacing(0)

        vbox.addWidget(lab1, 23)
        vbox.addWidget(lab2, 9)

        hbox.addLayout(vbox, 3)
        hbox.addWidget(lab3, 1)
        hbox.setContentsMargins(0, 0, 0, 0)

        self.bglab.setLayout(hbox)
