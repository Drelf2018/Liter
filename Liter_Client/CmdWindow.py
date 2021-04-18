from .RoundShadow import RoundShadow
from PyQt5.QtGui import QFont
from PyQt5.QtCore import (Qt, pyqtSignal)
from PyQt5.QtWidgets import QTextEdit
from .TLineEdit import TLineEdit
from .send_receive import connecter


class CmdWindow(RoundShadow):
    signal = pyqtSignal(str)

    def __init__(self, address: tuple, parent=None):
        super(CmdWindow, self).__init__(560, 420, title='{}:{}'.format(address[0], address[1]), parent=parent)
        self.initUI()
        self.setWindowTitle('CmdWindow')
        # 窗口置顶 https://blog.csdn.net/qq_38161040/article/details/87365818
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window | Qt.WindowStaysOnTopHint)
        self.signal.connect(lambda s: self.recvEdit.append('<<<'+s))
        self.ct = connecter(10240000, address)
        self.ct.setSignal('default', self.signal)
        self.ct.start()

    def initUI(self):
        self.font = QFont('微软雅黑', 10)
        self.sendEdit = TLineEdit(5, 320, 550, 45, None, self.bglab)
        self.sendEdit.Edit.setFont(self.font)
        self.recvEdit = QTextEdit(self.bglab)
        self.recvEdit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.recvEdit.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.recvEdit.setGeometry(5, 10, 550, 300)  # 初始位置以及大小
        self.recvEdit.setReadOnly(True)  # 只读
        self.recvEdit.setStyleSheet(("border:2px solid rgb(229,229,229);background:rgba(0,0,0,0);"))  # 取消背景
        self.recvEdit.setFont(self.font)

    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() in [16777220, 16777221]:  # 回车
            if self.sendEdit.Edit.hasFocus():
                text = self.sendEdit.Edit.text()
                if text:
                    self.ct.send(text)
                    self.recvEdit.append('>>>'+text)
                    self.sendEdit.Edit.clear()
                    if text == '/close':
                        self.close()
        QKeyEvent.accept()

    def close(self):
        self.ct.quit()
        super().close()
