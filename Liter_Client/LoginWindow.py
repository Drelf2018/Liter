import json
import requests
from .TLabel import TLabel
from .TLineEdit import TLineEdit
from .TPushButton import TPushButton
from .RoundShadow import RoundShadow
from PyQt5.QtCore import (QRegExp, pyqtSignal)
from PyQt5.QtGui import (QColor, QFont, QRegExpValidator)


class LoginWindow(RoundShadow):
    close_signal = pyqtSignal(bool)  # 关闭窗口信号

    def check_login(self, x):
        if x:
            self.close()
        else:
            self.passwordEdit.clear()
            self.passwordEdit.setPlaceholderText('账号或密码错误')

    def __init__(self, connecter, pic='http://bing.getlove.cn/latelyBingImageStory'):  # img\\bg.jpg
        r = requests.get(pic)
        pic = 'https:'+json.loads(r.text)[0]['CDNUrl']
        super(LoginWindow, self).__init__(540, 420, img=pic)
        self.connecter = connecter  # 与服务端的连接器
        self.close_signal.connect(self.check_login)  # 连接槽函数
        self.connecter.setSignal('/login', self.close_signal)  # 将信号告诉连接器
        self.initUI()

    def initUI(self):
        # 设置标题
        self.setWindowTitle('LoginWindow')
        w, h = self.bglab.width(), self.bglab.height()  # 背景长款 540 380
        # 新建展示框用于放置文本框与按钮
        self.lab = TLabel((15, 15, 15, 15), color=QColor(255, 255, 255, 155), parent=self.bglab)
        self.lab.setGeometry(0.2*w, 0.275*h, 0.6*w, 0.45*h)
        # 新建账号文本框并设置大小位置
        self.account = TLineEdit(5, 0.025*h, 0.6*w-10, 0.118*h, TLineEdit.ACCOUNT, self.lab)
        self.account.Edit.setPlaceholderText('账号/用户名/邮箱')  # 默认文字
        self.account.Edit.setFont(QFont('微软雅黑', 14*h/380))
        # self.account.Edit.setText('drelf')
        # 新建密码文本框并设置大小位置
        self.password = TLineEdit(5, 0.17*h, 0.6*w-10, 0.118*h, TLineEdit.PASSWORD, self.lab)  # [QIcon('img/1.png'), QIcon('img/2.png')],
        self.password.Edit.setPlaceholderText('密码')  # 默认文字
        self.password.Edit.setEchoMode(self.password.Edit.Password)  # 密码模式 输入字符用圆点代替
        self.password.Edit.setFont(QFont('微软雅黑', 14*h/380))
        self.password.Edit.textChanged.connect(lambda: self.password.Edit.setPlaceholderText('密码'))
        # self.password.Edit.setText('drelf...')
        # 限制输入字符
        reg = QRegExp('[a-zA-Z0-9!@#%^&*()_.]+$')  # 创建一个正则表达式对象
        validator = QRegExpValidator(reg, self)  # 创建一个过滤器对象
        self.account.Edit.setValidator(validator)  # 限制用户名范围
        self.password.Edit.setValidator(validator)  # 限制密码范围
        # 新建登录按钮并设置大小位置
        loginButton = TPushButton(r=(8, 8, 8, 8), color=[QColor(7, 188, 252), QColor(31, 200, 253), QColor(31, 200, 253)], parent=self.lab)
        loginButton.setTitle((QColor(255, 255, 255), QFont('微软雅黑', 12*h/380), '登录'))
        loginButton.clicked.connect(
            lambda: self.connecter.login({
                'username': self.account.Edit.text(),
                'password': self.password.Edit.text()
            })
        )
        loginButton.setGeometry(10, 0.31*h, 0.6*w-20, 0.118*h)

    def mousePressEvent(self, QMouseEvent):
        super(LoginWindow, self).mousePressEvent(QMouseEvent)
        x, y = QMouseEvent.x(), QMouseEvent.y()
        child = self.childAt(x, y)
        if not child or not isinstance(child, TLineEdit):
            self.setFocus()
        QMouseEvent.accept()

    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() in [16777220, 16777221]:  # 回车
            if self.account.Edit.hasFocus() or self.password.Edit.hasFocus():
                self.connecter.login({
                    'username': self.account.Edit.text(),
                    'password': self.password.Edit.text()
                })
        QKeyEvent.accept()
