from PyQt5.QtWidgets import (QLabel)
from PyQt5.QtCore import (Qt, QRect)
from PyQt5.QtGui import (QPen, QColor, QFont,  QPainter, QFontMetricsF)
from PIL import Image, ImageQt
from io import BytesIO
import requests
import re


class TMessageLabel(QLabel):
    '''
    内部类 消息展示框\n
    text 文本\n
    maxWidth 限宽\n
    font 字体
    '''
    def __init__(self, text, maxWidth=520, font=None, parent=None):
        super(TMessageLabel, self).__init__(parent)
        self.text = text
        self.maxWidth = maxWidth
        self.rwidth = 0
        self.rheight = 0
        if font:
            self.font = font
        else:
            self.font = QFont('msyh')
            self.font.setPixelSize(20)
        self.fm = QFontMetricsF(self.font)  # 测字符长度
        self.text = self.split()  # 分割字符
        self.resize(self.rwidth+14, self.rheight+11+16)

    def split(self):
        temp = []  # 返回分割后字符串
        while '' in self.text:
            self.text.remove('')  # 删除空字符 https://blog.csdn.net/crack6677/article/details/107728841
        patten = re.compile(r'<img src="[a-zA-z]+://[^\s]*"/>')  # 正则提取图片
        for t in self.text:
            img = re.search(patten, t)
            if img:
                url = t[10:-3]  # 图片网址
                try:
                    response = requests.get(url)  # 请求图片
                    image = Image.open(BytesIO(response.content))  # 读取网络图片
                    new_height = int(image.height/image.width*self.maxWidth/2)  # 图片宽度为限宽一半
                    self.rwidth = max(self.rwidth, self.maxWidth/2)
                    self.rheight += new_height + 3
                    image = image.resize((self.maxWidth//2, new_height), Image.ANTIALIAS)  # 缩放 https://blog.csdn.net/u010417185/article/details/74357382
                    temp.append(image)
                    continue
                except Exception:
                    t = '<图片错误>'
            count = 0  # 记录字符串长度
            last = 0  # 上一次分割的点位
            point = -1  # 指针
            for chn in t:
                point += 1
                count += self.fm.width(chn)
                if count > self.maxWidth:  # 超过限宽就分割
                    temp.append(t[last:point])
                    count = self.fm.width(chn)
                    last = point
                    self.rwidth = self.maxWidth
                    self.fm.width(t[last:point])  # 用于后面加上整行高度
                    self.rheight += self.fm.height() + 3  # 行间隔 3 像素
            if count <= self.maxWidth:  # 没达到限宽 不分割
                temp.append(t[last:])
                self.rwidth = max(self.rwidth, self.fm.width(t[last:]))
                self.fm.width(t[last:])  # 用于后面加上整行高度
                self.rheight += self.fm.height() + 3
        return temp

    def paintEvent(self, event):
        super(TMessageLabel, self).paintEvent(event)
        # 气泡
        bb = QRect(2, 2, self.width()-4, self.height()-4)
        bubble_pat = QPainter(self)
        bubble_pat.setPen(QPen(QColor(205, 156, 177), 2))
        bubble_pat.setBrush(QColor(238, 252, 255))
        bubble_pat.setRenderHint(bubble_pat.Antialiasing)
        if not(len(self.text) == 1 and isinstance(self.text[0], Image.Image)):
            bubble_pat.drawRoundedRect(bb, 10, 10)
        # 画正文与图片
        y = 7+8  # 指示画笔垂直绘画位置
        text_pat = QPainter(self)
        text_pat.setPen(Qt.black)
        text_pat.setFont(self.font)
        text_pat.setRenderHint(text_pat.Antialiasing)  # 抗锯齿
        for t in self.text:
            if isinstance(t, str):  # 文本
                w = self.fm.width(t)
                h = self.fm.height()
                text_pat.drawText(QRect(7, y, w, h), Qt.AlignCenter, t)
                y += h + 3
            elif isinstance(t, Image.Image):  # 图片
                pic = ImageQt.toqpixmap(t)
                text_pat.drawPixmap(7, y, pic)
                y += t.height + 3
            else:
                pass
        bubble_pat.end()
        text_pat.end()