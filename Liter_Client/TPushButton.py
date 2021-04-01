from PyQt5.QtWidgets import QPushButton


class TPushButton(QPushButton):
    def __init__(self, img_normal, img_hover, img_press, parent=None):
        super(TPushButton, self).__init__(parent)
        if not img_hover:
            img_hover = img_normal
        if not img_press:
            img_press = img_normal
        self.setStyleSheet("QPushButton{border-image: url(" + img_normal + ")}"
                           "QPushButton:hover{border-image: url(" + img_hover + ")}"
                           "QPushButton:pressed{border-image: url(" + img_press + ")}")
