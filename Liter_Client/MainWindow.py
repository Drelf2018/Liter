import os
import time
from .TLabel import TLabel
from .TPushButton import TPushButton
from .RoundShadow import RoundShadow
from .TMessage import TMessage
from .TScrollArea import TScrollArea
from PyQt5.QtCore import (Qt, pyqtSignal, QThread, QEvent)
from PyQt5.QtGui import (QColor, QFont, QKeyEvent)
from PyQt5.QtWidgets import (QFrame, QVBoxLayout, QHBoxLayout, QWidget, QTextEdit)


class autoUpdate(QThread):
    '自动刷新消息 间隔一秒'
    def __init__(self, mainwindow):
        super(autoUpdate, self).__init__()
        self.mw = mainwindow

    def run(self):
        while True:
            button = self.mw.selectButton
            if not button == self.mw.homeButton:
                first = button.bid
                child = self.mw.massageWidget.children()  # 获取原有消息 可能为空
                self.mw.setTitle(button.text[2])  # 改标题
                if child and child[0].massage['mid'] == first:
                    # 消息不为空且需要更新的话题是当前话题
                    self.mw.remake = True
                    self.mw.connecter.send('/update {}'.format(child[-1].massage['mid']))
                else:
                    self.mw.remake = False
                    self.mw.connecter.send('/update {}'.format(first))
            time.sleep(0.45)  # 太快服务器反应不过来


class TTextEdit(QTextEdit):
    def __init__(self, mainwindow, parent=None):
        super(TTextEdit, self).__init__(parent)
        self.mw = mainwindow

    def keyPressEvent(self, keyEvent):
        '回车发送 CTRL+Enter换行'
        # 按钮 https://blog.csdn.net/u012308586/article/details/104982137/
        # 事件 https://www.yuque.com/apachecn/aahuk0/docs_qkeyevent
        if keyEvent.key() in [16777220, 16777221]:  # 主键盘和小键盘的回车
            if keyEvent.modifiers() == Qt.ControlModifier:  # 修饰键是否是 CTRL
                # 构造新的不含修饰键的事件发给 QTextEdit 让他换行
                super().keyPressEvent(QKeyEvent(QEvent.KeyPress, Qt.Key_Enter, Qt.NoModifier))
            else:
                # 发送消息
                self.mw.sendTo()
        else:
            # 直接给 QTextEdit 让他操作文本
            super().keyPressEvent(keyEvent)


class MainWindow(RoundShadow):
    update_signal = pyqtSignal(list)  # 更新消息的信号

    def __init__(self, connecter):
        super(MainWindow, self).__init__(820, 640, 16, 8, lambda x: 20*(1-x**0.5*0.3535), QColor(0, 0, 0, 255), 0.2, None, '主页')
        self.connecter = connecter  # 与服务端的连接器
        self.massageWidget = QWidget()  # 消息框
        self.topicWidget = QWidget()  # 话题框
        self.update_signal.connect(self.change_massage)  # 连接槽函数
        self.connecter.setSignal('/update', self.update_signal)  # 将信号告诉连接器
        self.remake = False  # 判断是否保留消息框
        self.auto = autoUpdate(self)  # 自动刷新
        self.initUI()
        self.initTopic()
        self.auto.start()  # 启动线程

    def sendTo(self):
        if not self.selectButton == self.homeButton:
            text = self.sendEdit.toPlainText()
            if text:
                text = text.replace('\n', '<br/>')
                self.connecter.send('/sendto {} {}'.format(self.selectButton.tid, text))
                self.sendEdit.clear()

    def button_clicked(self):
        '按钮按下'
        self.selectButton = self.sender()  # https://www.5axxw.com/questions/content/dpc5m4
        if self.selectButton == self.homeButton:
            self.homeLabel.show()  # 显示主页
        else:
            self.homeLabel.hide()  # 隐藏主页

    def change_massage(self, massages):
        '修改消息框内容'
        old_massages = []
        if massages:
            if self.remake:
                if len(massages) == 1:
                    return
                else:
                    massages = massages[1:]
                old_massages = [tm.massage for tm in self.massageWidget.children()]
            massages = old_massages + massages
            self.massageWidget = QWidget()
            self.massageWidget.resize(615, 0)
            mwheight = 0
            for msg in massages:
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
        theight = 75
        twheight = 0
        for topic in self.connecter.topics:
            tb = TPushButton(bid=topic['first'], tid=topic['tid'], parent=self.topicWidget)
            tb.setTitle((Qt.black, QFont('msyh', 11, QFont.Bold), topic['name']))
            tb.setGeometry(0, twheight, 205, theight)
            tb.clicked.connect(self.button_clicked)
            twheight += theight
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
        # 添加聊天框背景
        bg = TLabel(img='img/bg.jpg', parent=self.bglab)
        bg.resize(self.bglab.width()*3/(3+1), self.bglab.height()*23/(23+9))
        bg = TLabel(color=(QColor(255, 255, 255, 190)), parent=self.bglab)
        bg.resize(self.bglab.width()*3/(3+1), self.bglab.height()*23/(23+9))
        # 添加消息滚动框
        self.massageScroll = TScrollArea()
        self.massageScroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.massageScroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.massageScroll.setFrameShape(QFrame.NoFrame)
        self.massageScroll.setStyleSheet(("border:0px;background:rgba(0,0,0,0);"))
        # 添加编辑框
        self.sendLabel = TLabel((0, 16, 0, 0), color=QColor(0, 255, 0, 155))
        self.sendEdit = TTextEdit(self, self.sendLabel)
        self.sendEdit.setFont(QFont('msyh', 11))
        self.sendEdit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.sendEdit.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.sendEdit.setGeometry(10, 10, 595, 105)  # 初始位置以及大小
        # 发送按钮
        self.sendButton = TPushButton(r=(8, 8, 8, 8), parent=self.sendLabel)
        self.sendButton.setTitle((Qt.black, QFont('msyh', 11, QFont.Bold), '发送'))
        self.sendButton.clicked.connect(self.sendTo)
        self.sendButton.setGeometry(525, 125, 80, 35)
        # 添加布局并设置布局中组件间距
        self.showBox = QVBoxLayout()
        self.topicBox = QVBoxLayout()
        self.hbox = QHBoxLayout()
        self.showBox.setSpacing(0)
        self.topicBox.setSpacing(0)
        self.hbox.setSpacing(0)
        # 添加话题滚动框
        self.topicScroll = TScrollArea()
        self.topicScroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.topicScroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.topicScroll.setFrameShape(QFrame.NoFrame)
        self.topicWidget.resize(205, 55)
        # 主页
        self.homeLabel = TLabel(text=(Qt.black, QFont('msyh', 50, QFont.Bold), '主页'), parent=self)
        self.homeLabel.setGeometry(self.s, self.s+40, self.bglab.width()*3/(3+1), self.bglab.height()*23/(23+9))
        # 主页按钮
        self.homeButton = TPushButton()
        self.homeButton.setTitle((Qt.black, QFont('msyh', 11, QFont.Bold), '主页'))
        self.homeButton.clicked.connect(self.button_clicked)
        self.homeButton.setMinimumSize(205, 45)
        # 记录被选中的按钮
        self.selectButton = self.homeButton
        # 添加"更多"按钮
        self.moreButton = TPushButton(r=(0, 0, 16, 0))
        self.moreButton.setTitle((Qt.black, QFont('msyh', 11, QFont.Bold), '更多'))
        self.moreButton.setMinimumSize(205, 45)
        # 将消息框与编辑框垂直布局
        self.showBox.addWidget(self.massageScroll, 23)
        self.showBox.addWidget(self.sendLabel, 9)
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

    def close(self):
        self.connecter.send('/close')
        self.auto.quit()
        super().close()
