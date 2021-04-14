from PyQt5.QtWidgets import (QLabel, QTextEdit)
from PyQt5.QtCore import (Qt, QRect)
from PyQt5.QtGui import (QPainter, QFont, QColor, QPen)
import requests
from PIL import Image
from io import BytesIO
import math
import re


def is_chinese(uchar):
    '判断一个unicode是否是汉字'
    # https://blog.csdn.net/qq_31112205/article/details/103972831
    return uchar >= u'\u4e00' and uchar <= u'\u9fa5'


class TMessage(QLabel):
    '单条消息'
    def __init__(self, massage, from_me=True, parent=None):
        super(TMessage, self).__init__(parent)
        self.textedit = QTextEdit(self)  # 放置消息的文本框
        self.textedit.setContextMenuPolicy(Qt.NoContextMenu)  # 禁用右键菜单 https://bbs.csdn.net/topics/391545518
        self.text = massage['text'].replace('<sp/>', ' ')  # 空格替换
        self.text = self.text.split('<br/>')  # 裁剪出消息
        self.identity = massage['from']  # 发消息人的身份
        self.count = 0
        for chn in self.identity:
            if is_chinese(chn):
                self.count += 1
        self.count = (len(self.identity) - self.count)/2 + self.count  # 统计多少个汉字
        self.time_ip = [False, '{} {}'.format(massage['time'], massage['ip'])]
        self.massage = massage  # 保存整条消息备用
        self.initUI()

    def __str__(self):
        return self.textedit.toPlainText()

    def mousePressEvent(self, QMouseEvent):
        self.time_ip[0] = not self.time_ip[0]

    def initUI(self):
        self.textedit.setMaximumWidth(530)  # 限制宽度最大值
        # 不显示滚动条
        self.textedit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textedit.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textedit.setGeometry(70, 35, 8, 25)  # 初始位置以及大小
        self.textedit.setReadOnly(True)  # 只读
        self.textedit.setStyleSheet(("border:0px;background:rgba(0,0,0,0);"))  # 取消背景
        self.font = QFont('msyh')  # 字体
        self.font.setPixelSize(20)
        self.textedit.setFont(self.font)
        self.setText()  # 放入文字
        self.resize(615, self.textedit.height()+50)  # 放入文字后调整组件大小

    def setText(self):
        fontsize = self.font.pixelSize()  # 字体像素值
        maxWidth = 0  # 最大宽度
        maxHeight = 0  # 最大高度
        picHeight = 0  # 图片高度
        patten = re.compile(r'<img src="[a-zA-z]+://[^\s]*"/>')
        while '' in self.text:
            self.text.remove('')  # 删除空字符 https://blog.csdn.net/crack6677/article/details/107728841
        for t in self.text:
            img = re.search(patten, t)
            if not img:
                count = 0
                for chn in t:
                    if is_chinese(chn):
                        count += 1
                count = (len(t) - count) + count * 2  # 字节 汉字占两字节
                if fontsize*count/2 <= self.textedit.maximumWidth():
                    maxWidth = max(maxWidth, fontsize*count/2)
                else:
                    maxWidth = self.textedit.maximumWidth()
                self.textedit.append(t)
                maxHeight += math.ceil(count/52)
            else:
                url = t[10:-3]
                try:
                    response = requests.get(url)
                    image = Image.open(BytesIO(response.content))  # 读取网络图片 https://blog.csdn.net/zwyact/article/details/100133350
                    w, h = image.width, image.height
                    new_w = self.textedit.maximumWidth()/2
                    t = t[0:-2] + 'width="{}"/>'.format(new_w)  # 改html图片大小 https://www.w3school.com.cn/tiy/t.asp?f=eg_html_image_size
                    self.textedit.append(t)
                    maxWidth = max(maxWidth, self.textedit.maximumWidth()/2)
                    picHeight += h/w*new_w
                except Exception:
                    t = '<图片错误>'
                    count = 10  # 字节 汉字占两字节
                    if fontsize*count/2 <= self.textedit.maximumWidth():
                        maxWidth = max(maxWidth, fontsize*count/2)
                    else:
                        maxWidth = self.textedit.maximumWidth()
                    self.textedit.append(t)
                    maxHeight += math.ceil(count/52)
        maxWidth += 10
        maxHeight = picHeight+23*maxHeight+10
        self.textedit.resize(maxWidth, maxHeight)
        if self.massage['from_me']:
            self.textedit.move(545-self.textedit.width(), 35)

    def paintEvent(self, event):
        '绘制消息框'
        super(TMessage, self).paintEvent(event)
        # 气泡
        bubble_pat = QPainter(self)
        bubble_pat.setPen(QPen(QColor(205, 156, 177), 2))
        bubble_pat.setBrush(QColor(238, 252, 255))
        bubble_pat.setRenderHint(bubble_pat.Antialiasing)
        tr = self.textedit.rect()
        tr.moveTo(self.textedit.pos())
        tr.setTop(tr.top()-5)
        bubble_pat.drawRoundedRect(tr, 10, 10)
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
            identity_pat.drawText(595-self.count*font.pixelSize(), 17, self.identity)  # 昵称
        else:
            identity_pat.drawText(5, 17, self.identity)  # 昵称
        if self.time_ip[0]:
            identity_pat.drawText(QRect(0, 7, 615, 10), Qt.AlignCenter, self.time_ip[1])  # 时间和ip
