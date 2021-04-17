import re
import time
import json
import requests
from .TLabel import TLabel
from .TPushButton import TPushButton
from .RoundShadow import RoundShadow
from .TMessage import TMessage
from .TScrollArea import TScrollArea
from .CmdWindow import CmdWindow
from PyQt5.QtCore import (Qt, pyqtSignal, QThread, QEvent)
from PyQt5.QtGui import (QColor, QFont, QKeyEvent)
from PyQt5.QtWidgets import (QFrame, QVBoxLayout, QHBoxLayout, QWidget, QTextEdit)


def splitImg(text):
    '分割图片'
    patten = re.compile(r'<img src="[a-zA-z]+://[^\s]*"/>')
    split_point = [0]
    for m in re.finditer(patten, text):
        if not split_point[-1] == m.start():
            split_point.append(m.start())
        split_point.append(m.end())
    count = 0  # 统计加了几个转行
    for i in split_point[1:]:
        text = text[0:i+count] + '\n' + text[i+count:]
        count += 1
    return text


class autoUpdate(QThread):
    '自动刷新消息 间隔一秒'
    def __init__(self, mainwindow):
        super(autoUpdate, self).__init__()
        self.mw = mainwindow

    def update_msg(self):
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

    def run(self):
        while True:
            self.update_msg()
            time.sleep(5)  # 太快服务器反应不过来


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
        self.rwidth = 820*1.5
        self.rheight = 640*1.5
        super(MainWindow, self).__init__(self.rwidth, self.rheight, title='主页')
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
                text = splitImg(text)
                text = text.replace(' ', '<sp/>')
                text = text.replace('\n', '<br/>')
                self.connecter.send('/sendto {} {}'.format(self.selectButton.tid, text))
                self.sendEdit.clear()
                self.auto.update_msg()

    def button_clicked(self):
        '按钮按下'
        self.selectButton = self.sender()  # https://www.5axxw.com/questions/content/dpc5m4
        if self.selectButton == self.homeButton:
            self.homeLabel.show()  # 显示主页
        else:
            self.homeLabel.hide()  # 隐藏主页
            self.auto.update_msg()

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
            self.massageWidget.resize(0.75*self.rwidth, 0)
            mwheight = 0
            for msg in massages:
                # 新建单条消息组件
                tm = TMessage(msg, 0.75*self.rwidth, parent=self.massageWidget)
                tm.move(0, mwheight)
                mwheight += tm.height()
            self.massageWidget.setMinimumSize(0.75*self.rwidth, mwheight)
            self.massageScroll.setWidget(self.massageWidget)
            # 自动滚动至最下 https://tieba.baidu.com/p/3174003701?red_tag=0415728187
            self.massageScroll.verticalScrollBar().setValue(self.massageScroll.verticalScrollBar().maximum())

    def initTopic(self):
        '向话题框添加话题'
        self.topicWidget = QWidget()
        self.topicWidget.resize(0.25*self.rwidth, 0)
        # self.topicWidget.setStyleSheet(("background:rgba();"))
        theight = 75
        twheight = 0
        for topic in self.connecter.topics:
            tb = TPushButton(bid=topic['first'], tid=topic['tid'], parent=self.topicWidget)
            tb.setTitle((Qt.black, QFont('微软雅黑', 11, QFont.Bold), topic['name']))
            tb.setGeometry(0, twheight, 0.25*self.rwidth, theight)
            tb.clicked.connect(self.button_clicked)
            twheight += theight
        self.topicWidget.setMinimumSize(0.25*self.rwidth, twheight)
        self.topicScroll.setWidget(self.topicWidget)
        self.topicScroll.verticalScrollBar().setValue(self.topicScroll.verticalScrollBar().minimum())

    def cmd(self):
        CmdWindow(self.connecter.ADDRESS).show()

    def initUI(self):
        # 设置标题
        self.setWindowTitle('MainWindow')
        # 添加聊天框背景
        r = requests.get('http://bing.getlove.cn/latelyBingImageStory')
        bg = TLabel(img='https:'+json.loads(r.text)[1]['CDNUrl'], parent=self.bglab)
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
        font = QFont('微软雅黑')
        font.setPixelSize(19)
        self.sendLabel = TLabel((0, 16, 0, 0))
        self.sendEdit = TTextEdit(self, self.sendLabel)
        self.sendEdit.setFont(font)
        self.sendEdit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.sendEdit.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.sendEdit.setStyleSheet(("border:0px;background:rgba(0,0,0,0);"))  # 取消背景
        self.sendEdit.setGeometry(10, 10, 0.75*self.rwidth-20, 0.208*(self.rheight-40)-20)  # 初始位置以及大小
        self.sendEdit.setContextMenuPolicy(Qt.NoContextMenu)  # 禁用右键菜单 https://bbs.csdn.net/topics/391545518
        # 发送按钮
        self.sendButton = TPushButton(r=(8, 8, 8, 8), color=[QColor(217, 135, 89), QColor(225, 163, 126), QColor(217, 135, 89)], parent=self.sendLabel)
        self.sendButton.setTitle((Qt.white, QFont('微软雅黑', 11, QFont.Bold), '发送'))
        self.sendButton.clicked.connect(self.sendTo)
        self.sendButton.setGeometry(0.6375*self.rwidth, 0.208*(self.rheight-40), 0.0975*self.rwidth, 0.0583*(self.rheight-40))
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
        self.topicScroll.setStyleSheet(("border:0px;background:rgba(187,222,255,255);"))
        # 主页
        self.homeLabel = TLabel(text=(Qt.black, QFont('微软雅黑', 50, QFont.Bold), '主页'), parent=self)
        self.homeLabel.setGeometry(self.s, self.s+40, self.bglab.width()*3/(3+1)-2, self.bglab.height()*23/(23+9)-1)
        # 主页按钮
        self.homeButton = TPushButton()
        self.homeButton.setTitle((Qt.black, QFont('微软雅黑', 11, QFont.Bold), '主页'))
        self.homeButton.clicked.connect(self.button_clicked)
        self.homeButton.setMinimumSize(0.25*self.rwidth, 45)
        # 记录被选中的按钮
        self.selectButton = self.homeButton
        # 添加"更多"按钮
        self.moreButton = TPushButton(r=(0, 0, 16, 0))
        self.moreButton.setTitle((Qt.black, QFont('微软雅黑', 11, QFont.Bold), '命令行'))
        self.moreButton.clicked.connect(self.cmd)
        self.moreButton.setMinimumSize(0.25*self.rwidth, 45)
        # 将消息框与编辑框垂直布局
        self.showBox.addWidget(self.massageScroll, 23)
        # 分割条
        splitLab = TLabel(color=QColor(242, 242, 242))
        splitLab.setMaximumHeight(2)
        self.showBox.addWidget(splitLab)
        self.showBox.addWidget(self.sendLabel, 9)
        # 将话题框与按钮垂直布局
        self.topicBox.addWidget(self.homeButton)
        self.topicBox.addWidget(self.topicScroll)
        self.topicBox.addWidget(self.moreButton)
        # 将两垂直布局水平排布
        self.hbox.addLayout(self.showBox, 3)
        # 分割条
        splitLab = TLabel(color=QColor(242, 242, 242))
        splitLab.setMaximumWidth(2)
        self.hbox.addWidget(splitLab)
        self.hbox.addLayout(self.topicBox, 1)
        # 取消布局与添加布局的组件间距
        self.hbox.setContentsMargins(0, 0, 0, 0)
        # 为窗口背景布局
        self.bglab.setLayout(self.hbox)

    def close(self):
        self.auto.quit()
        super().close()
