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


class DialogDisplay(QDialog):
    def __init__(self):
        super(DialogDisplay, self).__init__()

        # uic.loadUi(r"C:\Users\Soheil\Desktop\TS QT\dialogabout.ui", self)
        super().__init__()
        ts_ui = resource_path("dialogdisplay.ui")
        uic.loadUi(ts_ui, self)

        self.setFixedSize(176, 216)


        try:
            with open("config.ini", "r") as f:
                c = f.read()
                self.config = c.split('\n')
        except:
            print("Error")


        self.SYNC_BYTE_DEC = self.str_to_bool(self.config[0])
        self.PID_DEC = self.str_to_bool(self.config[1])
        self.CONTINUITY_COUNT_DEC = self.str_to_bool(self.config[2])

        print(self.SYNC_BYTE_DEC, self.PID_DEC, self.CONTINUITY_COUNT_DEC)

        self.button_cancel.clicked.connect(self.exit)
        self.button_apply.clicked.connect(self.apply)


        self.radio_sync_byte_dec.setChecked(self.SYNC_BYTE_DEC)
        self.radio_sync_byte_hex.setChecked(not(self.SYNC_BYTE_DEC))
        self.radio_pid_dec.setChecked(self.PID_DEC)
        self.radio_pid_hex.setChecked(not(self.PID_DEC))
        self.radio_continuity_counter_dec.setChecked(self.CONTINUITY_COUNT_DEC)
        self.radio_continuity_counter_hex.setChecked(not(self.CONTINUITY_COUNT_DEC))


    def apply(self):
        print("Apply")
        try:
            with open("config.ini", "w") as f:
                f.write(str(self.radio_sync_byte_dec.isChecked()))
                f.write('\n')
                f.write(str(self.radio_pid_dec.isChecked()))
                f.write('\n')
                f.write(str(self.radio_continuity_counter_dec.isChecked()))
                print("Apply")
            print(self.radio_sync_byte_dec.isChecked(), self.radio_pid_dec.isChecked(), self.radio_continuity_counter_dec.isChecked())

        except:
            pass
        self.close()

    def str_to_bool(self, s):
        if s == 'True':
            return True
        elif s == 'False':
            return False

        self.show()

    def exit(self):
        self.close()
# about_dialog = QApplication(sys.argv)

# UIdialog = UId()
# about_dialog.exec()
