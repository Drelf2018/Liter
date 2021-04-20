import socket
import command
import concurrent.futures as futures


class LiterServer(object):
    def __init__(self, host='', port=7233):
        self.HOST = host
        self.PORT = port
        self.BUFSIZ = 10240000
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
                    uid, topics = command.analysis(login, need='/login')
                    if uid:
                        client_socket.send(topics.encode('utf-8'))
                        user = [uid, client_address[0]]
                        break
                    else:
                        if topics:
                            client_socket.send('请先登录'.encode('utf-8'))
                        else:
                            client_socket.send('账户或密码错误'.encode('utf-8'))
                except Exception as e:
                    print(e)
            while True:
                data = client_socket.recv(self.BUFSIZ).decode('utf-8')
                print('接收到来自{2}的消息({1} bytes)：{0}'.format(data, len(data.encode('utf-8')), client_address))
                try:
                    if data == '/close':
                        break
                    else:
                        resp = command.analysis(data, user[0], user[1])
                        client_socket.send(resp.encode('utf-8'))
                except Exception as e:
                    client_socket.send(str(e).encode('utf-8'))
        finally:
            client_socket.close()
            print("已断开客户端{}！".format(client_address))


if __name__ == '__main__':
    ls = LiterServer()
    ls.launch()
