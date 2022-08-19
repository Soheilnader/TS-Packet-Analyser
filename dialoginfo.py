from PyQt5.QtWidgets import QDialog, QApplication, QTableWidget, QTableWidgetItem
from PyQt5 import uic, QtGui, QtCore
import sys
import os

import SDT

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class DialogInfo(QDialog):
    def __init__(self, PID, input_packets):
        super(DialogInfo, self).__init__()

        #uic.loadUi(r"C:\Users\Soheil\Desktop\TS QT\dialogabout.ui", self)
        super().__init__()
        ts_ui = resource_path("dialoginfo.ui")
        uic.loadUi(ts_ui, self)

        self.setFixedSize(609, 407)

        if PID == 0:
            self.table_info.setColumnCount(2)
            self.table_info.setHorizontalHeaderLabels(['PROGRAM_NUMBER', 'PROGRAM_MAP_PID'])
            self.table_info.setRowCount(len(input_packets.PROGRAM_NUMBER))
            row = 0
            for i in range(len(input_packets.PROGRAM_NUMBER)):
                self.table_info.setItem(row, 0, QTableWidgetItem(str(input_packets.PROGRAM_NUMBER[i])))
                self.table_info.setItem(row, 1, QTableWidgetItem(str(input_packets.PROGRAM_MAP_PID[i])))
                row += 1
            for i in range(len(input_packets.PROGRAM_NUMBER)):
                self.table_info.resizeRowToContents(i)

            self.table_info.resizeColumnToContents(0)
            self.table_info.resizeColumnToContents(1)


        if PID == 17:
            self.table_info.setColumnCount(6)
            self.table_info.setHorizontalHeaderLabels(['Service ID', 'Program name', 'EIT schedule flag', 'EIT present/following flag', 'Running status', 'Free CA mode'])
            self.table_info.setRowCount(len(input_packets.SERVICE_ID))
            row = 0
            for i in range(len(input_packets.SERVICE_ID)):
                self.table_info.setItem(row, 0, QTableWidgetItem(str(input_packets.SERVICE_ID[i])))
                self.table_info.setItem(row, 1, QTableWidgetItem(str(input_packets.PROGRAM_NAME[i])))
                self.table_info.setItem(row, 2, QTableWidgetItem(str(input_packets.EIT_SCHEDULE_FLAG[i])))
                self.table_info.setItem(row, 3, QTableWidgetItem(str(input_packets.EIT_PRESENT_FOLLOWING_FLAG[i])))
                self.table_info.setItem(row, 4, QTableWidgetItem(str(input_packets.RUNNING_STATUS[i])))
                self.table_info.setItem(row, 5, QTableWidgetItem(str(input_packets.FREE_CA_MODE[i])))
                row += 1
            for i in range(len(input_packets.SERVICE_ID)):
                self.table_info.resizeRowToContents(i)

            self.table_info.resizeColumnToContents(0)
            self.table_info.resizeColumnToContents(1)
            self.table_info.resizeColumnToContents(2)
            self.table_info.resizeColumnToContents(3)
            self.table_info.resizeColumnToContents(4)
            self.table_info.resizeColumnToContents(5)


        self.show()


#about_dialog = QApplication(sys.argv)

#UIdialog = UId()
#about_dialog.exec()