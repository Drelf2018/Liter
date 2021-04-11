import sys
import time
from .send_receive import connecter
from .LoginWindow import LoginWindow
from .MainWindow import MainWindow
from PyQt5.QtWidgets import QApplication


class Client(object):
    def __init__(self, host='127.0.0.1', port=7233):
        self.app = QApplication(sys.argv)
        self.ct = connecter(1024, (host, port))

    def start(self):
        self.ct.start()
        LoginWindow(self.ct).show()
        self.app.exec_()
        if self.ct.results:
            time.sleep(0.15)
            MainWindow(self.ct).show()
            self.app.exec_()
        self.ct.quit()
