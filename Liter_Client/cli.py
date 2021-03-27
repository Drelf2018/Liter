# coding:utf-8
import json
import time
import socket
import concurrent.futures as futures


class TCPClient:
    def __init__(self, host='127.0.0.1', port=7233):
        self.HOST = host
        self.PORT = port
        self.BUFSIZ = 1024
        self.ADDRESS = (self.HOST, self.PORT)
        self.tcpClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcpClientSocket.connect(self.ADDRESS)

    def login(self, account: dict):
        self.tcpClientSocket.send(('/login {} {}'.format(account['username'], account['password'])).encode('utf-8'))
        time.sleep(0.15)

    def send(self, msg):
        if msg:
            self.tcpClientSocket.send(msg.encode('utf-8'))

    def receive(self):
        try:
            while True:
                data = self.tcpClientSocket.recv(self.BUFSIZ).decode('utf-8')
                if data == '/close':
                    break
                try:
                    data = json.loads(data)
                    s = ''
                    for f in data:
                        s += '\n{}{}({}){}->{}: {}'.format(f['time'], f['from'], f['ip'], f['mid'], f['next'], f['text'])
                    data = s
                except Exception as e:
                    print(e)
                    pass
                print("<<<{}".format(data))
        finally:
            self.tcpClientSocket.close()
            print("连接已断开！")


ex = futures.ThreadPoolExecutor(max_workers=1)
tc = TCPClient()
ex.submit(tc.receive)
tc.login({'username': 'drelf', 'password': 'drelf...'})
while not tc.tcpClientSocket._closed:
    tc.send(input('>>>'))
    time.sleep(0.15)
