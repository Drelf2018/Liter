from PyQt5.QtWidgets import (QLabel)
from PyQt5.QtCore import (Qt, QRect, QThread)
from PyQt5.QtGui import (QPen, QColor, QFont, QBrush, QPainter, QFontMetricsF)
from .PicWindow import PicWindow
from PIL import Image, ImageQt
from io import BytesIO
import requests
import re
import time


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
        self.finish = 0
        self.picHeight = {}
        if font:
            self.font = font
        else:
            self.font = QFont('微软雅黑')
            self.font.setPixelSize(20)
        self.td = TDownload(self)
        self.td.start()
        self.fm = QFontMetricsF(self.font)  # 测字符长度
        self.text = self.split()  # 分割字符
        self.td.finish = self.finish
        self.resize(self.rwidth+14, self.rheight+11+16)

    def split(self):
        temp = []  # 返回分割后字符串
        while '' in self.text:
            self.text.remove('')  # 删除空字符 https://blog.csdn.net/crack6677/article/details/107728841
        patten = re.compile(r'<img src="[a-zA-z]+://[^\s]*"/>')  # 正则提取图片
        for t in self.text:
            img = re.search(patten, t)
            if img:
                try:
                    url = t[10:-3]
                    size = re.search(r'@\d+x\d+', t)
                    if size:
                        size = size.group()[1:]
                        w, h = size.split('x')
                        new_height = int(int(h)/int(w)*self.maxWidth*2/3)  # 图片宽度为限宽 2/3
                        self.rwidth = max(self.rwidth, self.maxWidth*2/3)
                        self.rheight += new_height + 3
                        self.finish += 1
                        self.td.append(url.replace('@{}x{}'.format(w, h), ''), len(temp))
                        temp.append(len(temp))
                    else:
                        response = requests.get(url)  # 请求图片
                        image = Image.open(BytesIO(response.content))  # 读取网络图片
                        new_height = int(image.height/image.width*self.maxWidth*2/3)  # 图片宽度为限宽一半
                        self.rwidth = max(self.rwidth, int(self.maxWidth*2/3))
                        self.rheight += new_height + 3
                        image = image.convert('RGBA')
                        alpha = image.split()[3]
                        bgmask = alpha.point(lambda x: 255-x)
                        image.paste((255, 255, 255), None, bgmask)
                        new_image = image.resize((int(self.maxWidth*2/3), new_height), Image.ANTIALIAS)  # 缩放 https://blog.csdn.net/u010417185/article/details/74357382
                        temp.append((new_image, image))
                    continue
                except Exception as e:
                    t = '<图片错误>'
                    print(e)
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

    def mouseDoubleClickEvent(self, QMouseEvent):
        if QMouseEvent.buttons() == Qt.LeftButton:
            x = QMouseEvent.pos().x()
            y = QMouseEvent.pos().y()
            lastKey = -1
            if 0 <= x <= self.maxWidth//2:
                if self.picHeight:
                    for key in self.picHeight:
                        if y < key:
                            break
                        else:
                            lastKey = key
                    if lastKey == -1:
                        lastKey = key
                    if 0 <= y-lastKey <= self.picHeight[lastKey][0]:
                        PicWindow(self.picHeight[lastKey][1], self).show()

    def mousePressEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.RightButton:
            QMouseEvent.ignore()

    def paintEvent(self, event):
        super(TMessageLabel, self).paintEvent(event)
        # 气泡
        bb = QRect(2, 2, self.width()-4, self.height()-4)
        bubble_pat = QPainter(self)
        bubble_pat.setPen(QPen(QColor(205, 156, 177), 2))
        bubble_pat.setBrush(QColor(238, 252, 255))
        bubble_pat.setRenderHint(bubble_pat.Antialiasing)
        if len(self.text) == 1 and isinstance(self.text[0], (tuple, int)):
            pass
        else:
            bubble_pat.drawRoundedRect(bb, 10, 10)
        # 画正文与图片
        y = 7+8  # 指示画笔垂直绘画位置
        text_pat = QPainter(self)
        text_pat.setFont(self.font)
        text_pat.setPen(Qt.black)
        text_pat.setRenderHint(text_pat.Antialiasing)  # 抗锯齿
        brush = QBrush()
        for t in self.text:
            if isinstance(t, str):  # 文本
                w = self.fm.width(t)
                h = self.fm.height()
                text_pat.drawText(QRect(7, y, w, h+3), Qt.AlignTop, t)
                y += h + 3
            elif isinstance(t, tuple) and isinstance(t[0], Image.Image):  # 图片
                pic = ImageQt.ImageQt(t[0])
                brush.setTextureImage(pic)
                text_pat.save()
                text_pat.translate(7, y)  # 移动画笔 https://tieba.baidu.com/p/3769108658
                text_pat.setPen(Qt.NoPen)
                text_pat.setBrush(brush)
                text_pat.drawRoundedRect(QRect(0, 0, pic.width(), pic.height()), 10, 10)
                text_pat.restore()
                if not self.picHeight.get(y):
                    self.picHeight[y] = (pic.height(), t[1])
                y += pic.height() + 3
            elif isinstance(t, int):
                images = self.td.pic.get(t, None)
                if images:
                    new_image, image = images
                    pic = ImageQt.ImageQt(new_image)
                    brush.setTextureImage(pic)
                    text_pat.save()
                    text_pat.translate(7, y)  # 移动画笔 https://tieba.baidu.com/p/3769108658
                    text_pat.setPen(Qt.NoPen)
                    text_pat.setBrush(brush)
                    text_pat.drawRoundedRect(QRect(0, 0, pic.width(), pic.height()), 10, 10)
                    text_pat.restore()
                    if not self.picHeight.get(y):
                        self.picHeight[y] = (pic.height(), image)
            else:
                pass


class TDownload(QThread):
    def __init__(self, tml: TMessageLabel):
        super(TDownload, self).__init__()
        self.tml = tml
        self.pic = {}
        self.url = []
        self.count = 0
        self.finish = -1

    def append(self, url, pos):
        self.url.append((url, pos))

    def run(self):
        while True:
            if not self.finish == -1:
                if self.finish == self.count:
                    break
            while len(self.url):
                try:
                    url, pos = self.url.pop(0)
                    response = requests.get(url)  # 请求图片
                    image = Image.open(BytesIO(response.content))  # 读取网络图片
                    image = image.convert('RGBA')
                    alpha = image.split()[3]
                    bgmask = alpha.point(lambda x: 255-x)
                    image.paste((255, 255, 255), None, bgmask)
                    new_height = int(image.height/image.width*self.tml.maxWidth*2/3)  # 图片宽度为限宽 2/3
                    new_image = image.resize((int(self.tml.maxWidth*2/3), new_height), Image.ANTIALIAS)  # 缩放 https://blog.csdn.net/u010417185/article/details/74357382
                    self.pic[pos] = (new_image, image)
                    self.count += 1
                    self.tml.u()
                except Exception:
                    pass
            time.sleep(0.5)
