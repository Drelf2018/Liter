import json
import time
import socket
from .LoginWindow import LoginWindow
import concurrent.futures as futures


class Client(object):
    def __init__(self, host='127.0.0.1', port=7233):
        self.BUFSIZ = 1024
        self.ADDRESS = (host, port)
        self.command = []
        self.Lw = None
        self.ex = None
        self.tcpClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcpClientSocket.connect(self.ADDRESS)

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

    def receive(self):
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

    def analysis(self, cmd, data):
        if cmd == '/login' or cmd == '/new_topic':
            try:
                data = json.loads(data)
                s = ''
                for f in data:
                    s += '\n[{}]({},{},{}): {}->{}'.format(f['name'], f['tid'], f['belong'], f['regtime'], f['first'], f['last'])
                    data = s
                if self.Lw.alive:
                    self.Lw.close()
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
        print("<<<{}".format(data))

    def start(self):
        self.ex = futures.ThreadPoolExecutor(max_workers=2)
        self.ex.submit(self.receive)
        self.Lw = LoginWindow(func=lambda x: self.login(x))
        self.Lw.show()
        input()
