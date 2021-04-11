import json
import time
import socket
from PyQt5.QtCore import QThread


class connecter(QThread):
    def __init__(self, BUFSIZ, ADDRESS):
        super(connecter, self).__init__()
        self.BUFSIZ = BUFSIZ
        self.ADDRESS = ADDRESS
        self.command = []
        self.results = []
        self.signal = None
        self.tcpClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def setSignal(self, signal):
        self.signal = signal

    def run(self):
        self.tcpClientSocket.connect(self.ADDRESS)
        try:
            while True:
                data = self.tcpClientSocket.recv(self.BUFSIZ).decode('utf-8')
                if data == '/close':
                    break
                else:
                    self.analysis(self.command.pop(0), data)
        except Exception as e:
            print(e)
        finally:
            self.tcpClientSocket.close()
            print("连接已断开！")

    def login(self, account: dict):
        self.send('/login {} {}'.format(account['username'], account['password']))
        time.sleep(0.15)

    def send(self, msg):
        if msg:
            try:
                self.command.append(msg.split(' ')[0])
                self.tcpClientSocket.send(msg.encode('utf-8'))
            except Exception as e:
                print(e)

    def analysis(self, cmd, data):
        if cmd == '/login':
            try:
                data = json.loads(data)
                self.signal.emit()
            except Exception as e:
                print(e)
        if cmd == '/new_topic':
            try:
                data = json.loads(data)
            except Exception as e:
                print(e)
        if cmd == '/update':
            try:
                data = json.loads(data)
                s = ''
                for f in data:
                    s += '\n{}{}({}){}->{}: {}'.format(f['time'], f['from'], f['ip'], f['mid'], f['next'], f['text'])
                    data = s
            except Exception as e:
                print(e)
        self.results.append(data)
        print("<<<{}".format(data))
