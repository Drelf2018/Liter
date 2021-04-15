from PyQt5.QtWidgets import (QLabel)
from PyQt5.QtCore import (Qt, QRect)
from PyQt5.QtGui import (QPainter, QFont, QColor, QFontMetricsF)
from .TMessageLabel import TMessageLabel


class TMessage(QLabel):
    '单条消息'
    def __init__(self, massage, from_me=True, parent=None):
        super(TMessage, self).__init__(parent)
        self.text = massage['text'].replace('<sp/>', ' ')  # 空格替换
        self.text = self.text.split('<br/>')  # 裁剪出消息
        self.identity = massage['from']  # 发消息人的身份
        self.time_ip = [False, '{} {}'.format(massage['time'], massage['ip'])]
        self.massage = massage  # 保存整条消息备用
        self.initUI()

    def initUI(self):
        self.font = QFont('msyh')  # 字体
        self.font.setPixelSize(20)  # 字体像素大小
        self.TMlab = TMessageLabel(self.text, 520, self.font, self)  # 消息气泡框
        if self.massage['from_me']:
            self.TMlab.move(545-self.TMlab.width(), 25)
        else:
            self.TMlab.move(70, 25)
        self.resize(615, self.TMlab.height()+40)  # 放入文字后调整组件大小

    def mousePressEvent(self, QMouseEvent):
        '显示/隐藏隐私'
        self.time_ip[0] = not self.time_ip[0]
        self.update()

    def paintEvent(self, event):
        '绘制消息'
        super(TMessage, self).paintEvent(event)
        # 个人信息
        identity_pat = QPainter(self)
        identity_pat.setPen(Qt.red)
        identity_pat.setBrush(QColor(229, 229, 229))
        identity_pat.setRenderHint(identity_pat.Antialiasing)
        if not self.massage['from_me']:
            identity_pat.drawRoundedRect(QRect(10, 25, 50, 50), 25, 25)  # 他人头像
        else:
            identity_pat.drawRoundedRect(QRect(555, 25, 50, 50), 25, 25)  # 自己头像
        identity_pat.setPen(Qt.gray)
        font = QFont('msyh', 10, QFont.Bold)
        font.setPixelSize(14)
        identity_pat.setFont(font)
        if self.massage['from_me']:
            identity_pat.drawText(595-QFontMetricsF(font).width(self.identity), 17, self.identity)  # 昵称
        else:
            identity_pat.drawText(5, 17, self.identity)  # 昵称
        if self.time_ip[0]:
            identity_pat.drawText(QRect(0, 7, 615, 10), Qt.AlignCenter, self.time_ip[1])  # 时间和 ip
