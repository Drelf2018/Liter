from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QPainterPath


def RoundPath(rect: QRectF, r00, r10, r11, r01):
    path = QPainterPath()
    # 左上
    path.moveTo(rect.x()+r00, rect.y())
    path.arcTo(rect.x(), rect.y(), 2*r00, 2*r00, 90, 90)
    # 左下
    path.lineTo(rect.x(), rect.y()+rect.height()-r10)
    path.arcTo(rect.x(), rect.y()+rect.height()-2*r10, 2*r10, 2*r10, 180, 90)
    # 右下
    path.lineTo(rect.x()+rect.width()-r11, rect.y()+rect.height())
    path.arcTo(rect.x()+rect.width()-2*r11, rect.y()+rect.height()-2*r11, 2*r11, 2*r11, -90, 90)
    # 右上
    path.lineTo(rect.x()+rect.width(), rect.y()-r01)
    path.arcTo(rect.x()+rect.width()-2*r01, rect.y(), 2*r01, 2*r01, 0, 90)
    # 闭合
    path.closeSubpath()
    return path
