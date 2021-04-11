import os
from .TLabel import TLabel
from .TLineEdit import TLineEdit
from .TPushButton import TPushButton
from .RoundShadow import RoundShadow
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import (QColor, QIcon, QFont, QRegExpValidator)


class LoginWindow(RoundShadow):
    def __init__(self, connecter, pic='C:\\Users\\drelf\\Pictures\\Saved Pictures\\bg.jpg'):
        super(LoginWindow, self).__init__(540, 420, 16, 8, lambda x: 20*(1-x**0.5*0.3535), QColor(0, 0, 0, 255), 0.2, pic, 'Liter')
        self.connecter = connecter
        self.connecter.setSignal(self.signal)
        self.auto = True
        self.initUI()

    def initUI(self):
        # 切换目录
        os.chdir(os.path.dirname(__file__))
        # 设置标题
        self.setWindowTitle('LoginWindow')
        # 设置最小化按钮位置和大小 绑定事件
        minButton = TPushButton(img=['img/min1.png', 'img/min2.png', 'img/min2.png'], parent=self)
        minButton.setGeometry(479, 16, 26, 26)
        minButton.clicked.connect(self.showMinimized)
        # 设置关闭按钮位置和大小 绑定事件
        closeButton = TPushButton(img=['img/close1.png', 'img/close2.png', 'img/close2.png'], parent=self)
        closeButton.setGeometry(510, 16, 26, 26)
        closeButton.clicked.connect(self.close)
        # 新建展示框用于放置文本框与按钮
        lab = TLabel((20, 20, 20, 20), color=QColor(255, 255, 255, 155), parent=self)
        lab.setGeometry(8+(540-245)/2, 150, 245, 175)
        # 新建账号文本框并设置大小位置
        accountEdit = TLineEdit([QIcon('img/1.png'), QIcon('img/2.png')], lab)
        accountEdit.setPlaceholderText('账号/用户名/邮箱')  # 默认文字
        accountEdit.setFont(QFont('msyh', 14))
        accountEdit.setGeometry(0, 10, 240, 45)
        accountEdit.setText('drelf')
        # 新建密码文本框并设置大小位置
        passwordEdit = TLineEdit([QIcon('img/1.png'), QIcon('img/2.png')], lab)
        passwordEdit.setPlaceholderText('密码')  # 默认文字
        passwordEdit.setEchoMode(TLineEdit.Password)  # 密码模式 输入字符用圆点代替
        passwordEdit.setFont(QFont('msyh', 8))
        passwordEdit.setGeometry(0, 65, 240, 45)
        passwordEdit.setText('drelf...')
        # 限制输入字符
        reg = QRegExp('[a-zA-Z0-9!@#%^&*()_.]+$')  # 创建一个正则表达式对象
        validator = QRegExpValidator(reg, self)  # 创建一个过滤器对象
        accountEdit.setValidator(validator)  # 限制用户名范围
        passwordEdit.setValidator(validator)  # 限制密码范围
        # 新建登录按钮并设置大小位置
        loginButton = TPushButton(r=(10, 10, 10, 10), color=[QColor(7, 188, 252), QColor(31, 200, 253), QColor(31, 200, 253)], parent=lab)
        loginButton.setTitle((QColor(255, 255, 255), QFont('msyh', 11), '登录'))
        loginButton.clicked.connect(
            lambda: self.connecter.login({
                'username': accountEdit.text(),
                'password': passwordEdit.text()
            })
        )
        loginButton.setGeometry(10, 125, 225, 34.6)
