import socket
from command_copy import analysis_command as ac
import concurrent.futures as futures


class TCPServer:
    def __init__(self, host='127.0.0.1', port=7233):
        self.HOST = host
        self.PORT = port
        self.BUFSIZ = 1024
        self.ADDRESS = (self.HOST, self.PORT)
        self.ex = futures.ThreadPoolExecutor(max_workers=100)
        self.tcpServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcpServerSocket.bind(self.ADDRESS)
        self.tcpServerSocket.listen(10)

    def launch(self):
        print('服务器正在运行，等待客户端连接...')
        while True:
            client_socket, client_address = self.tcpServerSocket.accept()
            self.ex.submit(self.response, client_socket, client_address)
            print('已连接客户端{}！'.format(client_address))

    def response(self, client_socket, client_address):
        try:
            while True:
                login = client_socket.recv(self.BUFSIZ).decode('utf-8')
                try:
                    uid, info = ac(login, '/login')
                    if uid:
                        client_socket.send(info.encode('utf-8'))
                        user = [uid, client_address[0]]
                        break
                    else:
                        client_socket.send('账户或密码错误'.encode('utf-8'))
                except Exception as e:
                    print(e)
            while True:
                data = client_socket.recv(self.BUFSIZ).decode('utf-8')
                print('接收到来自{2}的消息({1} bytes)：{0}'.format(data, len(data.encode('utf-8')), client_address))
                try:
                    resp = ac(data, user=user)
                    if not resp:
                        client_socket.send('/close'.encode('utf-8'))
                        break
                    else:
                        client_socket.send(resp.encode('utf-8'))
                except Exception as e:
                    client_socket.send(str(e).encode('utf-8'))
        finally:
            client_socket.close()
            print("已主动断开客户端{}！".format(client_address))


ts = TCPServer()
ts.launch()
