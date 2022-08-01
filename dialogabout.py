from PyQt5.QtWidgets import QDialog
from PyQt5 import uic
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

        self.setFixedSize(378, 322)

        self.show()


#about_dialog = QApplication(sys.argv)

#UIdialog = UId()
#about_dialog.exec()
