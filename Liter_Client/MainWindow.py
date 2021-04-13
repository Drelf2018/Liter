import os
from .TLabel import TLabel
from .TPushButton import TPushButton
from .RoundShadow import RoundShadow
from .TMessage import TMessage
from .TScrollArea import TScrollArea
from PyQt5.QtCore import (Qt, pyqtSignal)
from PyQt5.QtGui import (QColor, QFont)
from PyQt5.QtWidgets import (QFrame, QVBoxLayout, QHBoxLayout, QWidget)


class MainWindow(RoundShadow):
    update_signal = pyqtSignal(list)  # 更新消息的信号

    def __init__(self, connecter):
        super(MainWindow, self).__init__(820, 640, 16, 8, lambda x: 20*(1-x**0.5*0.3535), QColor(0, 0, 0, 255), 0.2, None, 'Liter')
        self.connecter = connecter  # 与服务端的连接器
        self.massageWidget = QWidget()  # 消息框
        self.topicWidget = QWidget()  # 话题框
        self.update_signal.connect(self.change_massage)  # 连接槽函数
        self.connecter.setSignal('/update', self.update_signal)  # 将信号告诉连接器
        self.initUI()

    def update_massage(self):
        '获取新消息'
        first = self.sender().bid  # https://www.5axxw.com/questions/content/dpc5m4
        child = self.massageWidget.children()  # 获取原有消息 可能为空
        if child and child[0].massage['mid'] == first:
            # 消息不为空且需要更新的话题是当前话题
            self.connecter.send('/update {}'.format(child[-1].massage['next']))
        else:
            # 重置消息框
            self.massageWidget = QWidget()
            self.massageWidget.resize(615, 0)
            self.connecter.send('/update {}'.format(first))

    def change_massage(self, massages):
        '修改消息框内容'
        mwheight = self.massageWidget.height()
        for msg in massages:
            if msg:
                # 新建单条消息组件
                tm = TMessage(massage=msg, parent=self.massageWidget)
                tm.move(0, mwheight)
                mwheight += tm.height()
        self.massageWidget.setMinimumSize(615, mwheight)
        self.massageScroll.setWidget(self.massageWidget)
        # 自动滚动至最下 https://tieba.baidu.com/p/3174003701?red_tag=0415728187
        self.massageScroll.verticalScrollBar().setValue(self.massageScroll.verticalScrollBar().maximum())

    def initTopic(self):
        '向话题框添加话题'
        self.topicWidget = QWidget()
        self.topicWidget.resize(205, 0)
        twheight = 0
        for topic in self.connecter.topics:
            tb = TPushButton(bid=topic['first'], parent=self.topicWidget)
            tb.setTitle((Qt.white, QFont('msyh', 11), topic['name']))
            tb.setGeometry(0, twheight, 205, 275)
            tb.clicked.connect(self.update_massage)
            twheight += 275
        self.topicWidget.setMinimumSize(205, twheight)
        self.topicScroll.setWidget(self.topicWidget)
        self.topicScroll.verticalScrollBar().setValue(self.topicScroll.verticalScrollBar().minimum())

    def initUI(self):
        # 切换目录
        os.chdir(os.path.dirname(__file__))
        # 设置标题
        self.setWindowTitle('MainWindow')
        # 设置最小化按钮位置和大小 绑定事件
        self.minButton = TPushButton(img=['img/min1.png', 'img/min2.png', 'img/min2.png'], parent=self)
        self.minButton.setGeometry(759, 16, 26, 26)
        self.minButton.clicked.connect(self.showMinimized)
        # 设置关闭按钮位置和大小 绑定事件
        self.closeButton = TPushButton(img=['img/close1.png', 'img/close2.png', 'img/close2.png'], parent=self)
        self.closeButton.setGeometry(790, 16, 26, 26)
        self.closeButton.clicked.connect(self.close)
        # 添加消息滚动框
        self.massageScroll = TScrollArea()
        self.massageScroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.massageScroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.massageScroll.setFrameShape(QFrame.NoFrame)
        # 添加编辑框
        self.lab2 = TLabel((0, 16, 0, 0), color=QColor(0, 255, 0, 155))
        self.sendButton = TPushButton(r=(8, 8, 8, 8), parent=self.lab2)
        self.sendButton.setTitle((QColor(255, 255, 255), QFont('msyh', 11), '发送'))
        self.sendButton.clicked.connect(lambda: self.connecter.send(''))
        self.sendButton.setGeometry(505, 120, 100, 40)
        # 添加布局并设置布局中组件间距
        self.showBox = QVBoxLayout()
        self.topicBox = QVBoxLayout()
        self.hbox = QHBoxLayout()
        self.showBox.setSpacing(0)
        self.topicBox.setSpacing(0)
        self.hbox.setSpacing(0)
        # 将消息框与编辑框垂直布局
        self.showBox.addWidget(self.massageScroll, 23)
        self.showBox.addWidget(self.lab2, 9)
        # 添加话题滚动框
        self.topicScroll = TScrollArea()
        self.topicScroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.topicScroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.topicScroll.setFrameShape(QFrame.NoFrame)
        self.topicWidget.resize(205, 55)
        # 主页按钮
        self.homeButton = TPushButton()
        self.homeButton.setTitle((QColor(255, 255, 255), QFont('msyh', 11), '主页'))
        self.homeButton.clicked.connect(self.initTopic)
        self.homeButton.setMinimumSize(205, 45)
        # 添加"更多"按钮
        self.moreButton = TPushButton(r=(0, 0, 16, 0))
        self.moreButton.setTitle((QColor(255, 255, 255), QFont('msyh', 11), '更多'))
        self.moreButton.setMinimumSize(205, 45)
        # 将话题框与按钮垂直布局
        self.topicBox.addWidget(self.homeButton)
        self.topicBox.addWidget(self.topicScroll)
        self.topicBox.addWidget(self.moreButton)
        # 将两垂直布局水平排布
        self.hbox.addLayout(self.showBox, 3)
        self.hbox.addLayout(self.topicBox, 1)
        # 取消布局与添加布局的组件间距
        self.hbox.setContentsMargins(0, 0, 0, 0)
        # 为窗口背景布局
        self.bglab.setLayout(self.hbox)
