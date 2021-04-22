from PyQt5.QtCore import Qt, QRect, QPointF
from PyQt5.QtGui import QPainter, QColor, QBrush, QWheelEvent
from PyQt5.QtWidgets import QWidget, QDesktopWidget
from math import sqrt
from PIL import ImageQt
import time


class PicWindow(QWidget):
    '''
    圆角边框类\n
    width, height 去掉边框后界面的长宽\n
    r 界面圆角半径\n
    s 阴影扩散范围\n
    alpha 阴影可见度变化函数\n
    color 颜色\n
    space 自变量(距离界面距离，取值[0-s])每次增加距离\n
    img 背景图片
    '''
    def __init__(self, img, parent=None):
        super(PicWindow, self).__init__(parent)
        im = img.convert('RGBA')
        alpha = im.split()[3]
        bgmask = alpha.point(lambda x: 255-x)
        im.paste((255, 255, 255), None, bgmask)
        self.ori_img = ImageQt.ImageQt(im)
        self.img = ImageQt.ImageQt(im)
        self.k = img.width/img.height
        self.alpha = alpha
        self.color = QColor(0, 0, 0, 255)
        # m_drag 用于判断是否可以移动窗口
        self.m_drag = False
        self.m_DragPosition = None
        # 圆角
        self.r = 5
        # 中心位置
        self.cpos = None
        # 时间戳
        self.tpos = []
        # 按住Ctrl 用滚轮缩放窗口
        self.m_scale = False
        # 设置窗口大小为界面大小加上两倍阴影扩散距离
        self.resize(img.width, img.height)
        # 设置窗口无边框和背景透明
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.center()

    def center(self):
        dw, dh = QDesktopWidget().geometry().width(), QDesktopWidget().geometry().height()
        iw, ih = self.ori_img.width(), self.ori_img.height()
        k1 = sqrt(0.75*dw*dh/iw/ih)
        k2 = 0.86*dw/iw
        k3 = 0.86*dh/ih
        k = min(k1, k2, k3)
        self.img = self.ori_img.scaled(iw*k, ih*k, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.resize(int(self.img.width()), int(self.img.height()))
        # 记录窗口中心
        # 获得窗口
        qr = self.frameGeometry()
        # 获得屏幕中心点
        cp = QDesktopWidget().availableGeometry().center()
        # 显示到屏幕中心
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        self.cpos = self.pos()+QPointF(self.width()/2, self.height()/2)

    def paintEvent(self, event):
        self.resize(self.img.width(), self.img.height())
        self.move(self.cpos.x()-self.width()/2, self.cpos.y()-self.height()/2)
        # 画图片
        pic_pat = QPainter(self)
        pic_pat.setRenderHint(pic_pat.Antialiasing)
        brush = QBrush()
        brush.setTextureImage(self.img)
        pic_pat.setPen(Qt.gray)
        pic_pat.setBrush(brush)
        pic_pat.drawRoundedRect(QRect(0, 0, self.width(), self.height()), self.r, self.r)
        pic_pat.end()

    def mousePressEvent(self, QMouseEvent):
        '鼠标点击 检测点击位置判断是否可移动'
        if QMouseEvent.button() == Qt.LeftButton:
            # 鼠标点击点的相对位置
            self.m_DragPosition = QMouseEvent.globalPos()-self.pos()
            if 0 < self.m_DragPosition.y() < self.height():
                self.m_drag = True

    def mouseMoveEvent(self, QMouseEvent):
        '按住左键可移动窗口'
        if QMouseEvent.buttons() == Qt.LeftButton:
            if self.m_drag:
                self.move(QMouseEvent.globalPos()-self.m_DragPosition)
                self.cpos = self.pos()+QPointF(self.width()/2, self.height()/2)
                QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_drag = False
        QMouseEvent.accept()

    def keyPressEvent(self, keyEvent):
        if keyEvent.key() == Qt.Key_Escape:
            self.close()

    def mouseDoubleClickEvent(self, QMouseEvent):
        if QMouseEvent.buttons() == Qt.LeftButton:
            self.close()

    def wheelEvent(self, e: QWheelEvent):
        if not self.tpos:
            self.tpos.append(time.time())
        else:
            t = time.time()
            if t-self.tpos[-1] > 0.5:
                self.tpos.append(t)
            else:
                return
        para = e.angleDelta().y()/1200+1
        w = self.width()*para
        h = w/self.k
        if w < 100 or h < 100:
            self.tpos.pop(0)
            return
        self.img = self.ori_img.scaled(w, h, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.repaint()
        self.tpos.pop(0)
