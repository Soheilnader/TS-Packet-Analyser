from PyQt5.QtWidgets import QDialog
from PyQt5 import uic
from PyQt5.QtGui import QPixmap

import sys
import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class DialogAbout(QDialog):
    def __init__(self):
        super(DialogAbout, self).__init__()

        #uic.loadUi(r"C:\Users\Soheil\Desktop\TS QT\dialogabout.ui", self)
        super().__init__()
        ts_ui = resource_path("dialogabout.ui")
        uic.loadUi(ts_ui, self)

        self.setFixedSize(420, 350)

        pic1 = QPixmap(resource_path("logo1.png"))
        pic2 = QPixmap(resource_path("logo2.png"))
        pic3 = QPixmap(resource_path("logo3.png"))
        pic4 = QPixmap(resource_path("packet.ico"))

        self.label_2.setPixmap(pic1)
        self.label.setPixmap(pic2)
        self.label_7.setPixmap(pic3)
        self.label_5.setPixmap(pic4)

        self.show()


#about_dialog = QApplication(sys.argv)

#UIdialog = UId()
#about_dialog.exec()