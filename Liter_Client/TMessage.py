from PyQt5.QtWidgets import (QLabel)
from PyQt5.QtCore import (Qt, QRect)
from PyQt5.QtGui import (QPainter, QFont, QFontMetricsF, QBrush)
from .TMessageLabel import TMessageLabel
from PIL import Image, ImageQt
from io import BytesIO
from .PicBase64 import icon
import base64


class TMessage(QLabel):
    '单条消息'
    def __init__(self, massage, rwidth, parent=None):
        super(TMessage, self).__init__(parent)
        self.text = massage['text'].replace('<sp/>', ' ')  # 空格替换
        self.text = self.text.split('<br/>')  # 裁剪出消息
        self.identity = massage['from']  # 发消息人的身份
        self.time_ip = [False, '{} {}'.format(massage['time'], massage['ip'])]
        self.massage = massage  # 保存整条消息备用
        self.rwidth = rwidth
        self.im = None
        self.initUI()

    def initUI(self):
        self.TMlab = TMessageLabel(self.text, maxWidth=self.rwidth-95, parent=self)  # 消息气泡框
        if self.massage['from_me']:
            self.TMlab.move(self.rwidth-70-self.TMlab.width(), 25)
        else:
            self.TMlab.move(70, 25)
        self.resize(self.rwidth, self.TMlab.height()+40)  # 放入文字后调整组件大小
        image = BytesIO(base64.b64decode(icon))
        image = Image.open(image)
        image = image.convert('RGBA')
        alpha = image.split()[3]
        bgmask = alpha.point(lambda x: 255-x)
        image.paste((255, 255, 255), None, bgmask)
        image = image.resize((50, 50), Image.ANTIALIAS)
        self.im = ImageQt.ImageQt(image)

    def mousePressEvent(self, QMouseEvent):
        '显示/隐藏隐私'
        self.time_ip[0] = not self.time_ip[0]
        self.update()

    def paintEvent(self, event):
        '绘制消息'
        super(TMessage, self).paintEvent(event)
        # 个人信息
        identity_pat = QPainter(self)
        identity_pat.setPen(Qt.NoPen)
        identity_pat.setRenderHint(identity_pat.Antialiasing)
        brush = QBrush()
        brush.setTextureImage(self.im)
        identity_pat.setBrush(brush)
        identity_pat.save()
        if not self.massage['from_me']:
            identity_pat.translate(10, 25)
            identity_pat.drawRoundedRect(QRect(0, 0, 50, 50), 25, 25)  # 他人头像
        else:
            identity_pat.translate(self.rwidth-60, 25)
            identity_pat.drawRoundedRect(QRect(0, 0, 50, 50), 25, 25)  # 自己头像
        identity_pat.restore()
        identity_pat.setPen(Qt.gray)
        font = QFont('微软雅黑', weight=QFont.Bold)
        font.setPixelSize(14)
        identity_pat.setFont(font)
        if self.massage['from_me']:
            identity_pat.drawText(self.rwidth-10-QFontMetricsF(font).width(self.identity), 17, self.identity)  # 昵称
        else:
            identity_pat.drawText(5, 17, self.identity)  # 昵称
        if self.time_ip[0]:
            identity_pat.drawText(QRect(0, 7, self.rwidth, 14), Qt.AlignCenter, self.time_ip[1])  # 时间和 ip
