import sys
from .send_receive import connecter
from .LoginWindow import LoginWindow
from .MainWindow import MainWindow
from PyQt5.QtWidgets import QApplication


class Client(object):
    def __init__(self, host='127.0.0.1', port=7233):
        self.app = QApplication(sys.argv)  # 新建窗口前必运行app
        self.ct = connecter(10240000, (host, port))  # 设定连接器 BUFSIZ, ADDRESS

    def start(self):
        self.ct.start()  # 启动连接器
        LoginWindow(self.ct).show()  # 显示登录窗口
        self.app.exec_()  # 等待直到登录窗口关闭
        if self.ct.topics:  # 检测是人为关闭还是登录成功 若登录成功 连接器会获取用户关注的话题
            MainWindow(self.ct).show()  # 显示主窗口
            self.app.exec_()  # 等待主窗口关闭
        self.ct.quit()  # 断开连接器
