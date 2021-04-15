import json
import socket
from PyQt5.QtCore import QThread


class connecter(QThread):
    '连接器'
    def __init__(self, BUFSIZ, ADDRESS):
        super(connecter, self).__init__()
        self.BUFSIZ = BUFSIZ  # 数据传输时大小
        self.ADDRESS = ADDRESS  # 连接地址
        self.command = []  # 用户发出的命令
        self.signal = {}  # 各种信号 由窗口给与
        self.topics = []  # 用户关注话题
        self.tcpClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 真正的 Socket 连接器

    def setSignal(self, name, signal):
        '设置信号'
        self.signal[name] = signal

    def send(self, msg):
        '发送消息'
        if msg:
            try:
                self.command.append(msg.split(' ')[0])  # 将发送的指令分离出来添加到指令集
                self.tcpClientSocket.send(msg.encode('utf-8'))
            except Exception as e:
                print(e)

    def login(self, account: dict):
        '登录'
        self.send('/login {} {}'.format(account['username'], account['password']))

    def run(self):
        '接收服务端数据'
        self.tcpClientSocket.connect(self.ADDRESS)  # 连接
        try:
            while True:
                # 死循环不断接收
                data = self.tcpClientSocket.recv(self.BUFSIZ).decode('utf-8')
                if data == '/close':
                    break
                else:
                    # 分析数据 并弹出对应的指令
                    self.analysis(self.command.pop(0), data)
        except Exception as e:
            # 非主动断开时报错才打印
            if '你的主机中的软件中止了一个已建立的连接' not in str(e):
                print(e)
            self.tcpClientSocket.close()

    def analysis(self, cmd, data):
        '分析数据'
        if cmd == '/login':
            try:
                data = json.loads(data)
                self.topics = data  # 保存获取的话题
                self.signal['/login'].emit(True)
            except Exception:
                # 如果 json 解析失败发送False信号给登录窗口
                self.signal['/login'].emit(False)
        else:
            try:
                data = json.loads(data)
                # 将解析好的 json 数据发送给窗体
                if cmd in self.signal:
                    self.signal[cmd].emit(data)
            except Exception as e:
                print(e, data)

    def quit(self):
        '断开连接'
        self.send('/close')
        self.tcpClientSocket.close()
        super().quit()
