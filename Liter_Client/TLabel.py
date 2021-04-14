from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import (QImage, QBrush, QPainter)
from .TPath import RoundPath
import requests
from PIL import Image, ImageFilter, ImageQt
from io import BytesIO


class TLabel(QLabel):
    '''
    带圆角的展示框\n
    r 圆角半径，类型为列表，从左上开始逆时针顺序\n
    img 要展示的图片
    color 纯色
    text 颜色、字体、文本
    '''
    def __init__(self, r=(0, 0, 0, 0), img=None, color=Qt.white, text=None, parent=None):
        super(TLabel, self).__init__(parent)
        self.r = r
        self.img = img
        self.color = color
        self.text = text
        if img:
            response = requests.get(img)
            image = Image.open(BytesIO(response.content))  # 读取网络图片 https://blog.csdn.net/zwyact/article/details/100133350
            image = image.filter(ImageFilter.GaussianBlur(radius=5))  # 高斯模糊 https://blog.csdn.net/yanshuai_tek/article/details/80653064
            # 透明图片需要加白色底 https://www.cnblogs.com/RChen/archive/2007/03/31/pil_thumb.html
            image = image.convert('RGBA')
            alpha = image.split()[3]
            bgmask = alpha.point(lambda x: 255-x)
            image.paste((255, 255, 255), None, bgmask)
            self.img = ImageQt.ImageQt(image)

    def paintEvent(self, event):
        # 画笔设置不描边
        pat = QPainter(self)
        pat.setPen(Qt.NoPen)
        brush = QBrush()
        pat.setRenderHint(pat.Antialiasing)  # 抗锯齿
        # 画刷为图片 若不存在为纯色
        if self.img:
            self.img = QImage(self.img).scaled(self.width(), self.height())
            brush.setTextureImage(self.img)
        else:
            brush = QBrush(self.color)
        # 喷漆
        pat.setBrush(brush)
        path = RoundPath(self.rect(), self.r)
        pat.drawPath(path)
        # 文字
        if self.text:
            color, font, text = self.text
            pat.setPen(color)
            pat.setFont(font)
            pat.drawText(self.rect(), Qt.AlignCenter, text)
        super(TLabel, self).paintEvent(event)
