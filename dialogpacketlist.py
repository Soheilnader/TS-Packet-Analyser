from PyQt5.QtWidgets import QDialog, QApplication, QTableWidget, QTableWidgetItem
from PyQt5 import uic, QtGui, QtCore
import sys
import os

from TS import TS


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class DialogPacketList(QDialog):
    def __init__(self, pckt):
        super(DialogPacketList, self).__init__()
        ts_ui = resource_path("dialogpacketlist.ui")
        uic.loadUi(ts_ui, self)

        self.table_packet.setRowCount(len(pckt))
        self.table_packet.setColumnCount(8)
        # self.table_packet.setColumnWidth(0, 40)
        # self.table_packet.setColumnWidth(1, 40)
        # self.table_packet.setColumnWidth(2, 40)
        # self.table_packet.setColumnWidth(3, 200)
        row = 0
        for i in range(len(pckt)):
            try:
                self.table_packet.setItem(row, 0, QTableWidgetItem(str(pckt[i].PID_TYPE)))
                self.table_packet.setItem(row, 1, QTableWidgetItem(hex(pckt[i].SYNC_BYTE)))
                self.table_packet.setItem(row, 2, QTableWidgetItem(str(pckt[i].TRANSPORT_ERROR_INDICATOR)))
                self.table_packet.setItem(row, 3, QTableWidgetItem(str(pckt[i].PAYLOAD_UNIT_START_INDICATOR)))
                self.table_packet.setItem(row, 4, QTableWidgetItem(str(pckt[i].TRANSPORT_PRIORITY)))
                self.table_packet.setItem(row, 5, QTableWidgetItem(str(pckt[i].PID)))
                self.table_packet.setItem(row, 6, QTableWidgetItem(str(pckt[i].SECTION_NUMBER)))
                self.table_packet.setItem(row, 7, QTableWidgetItem(str(pckt[i].LAST_SECTION_NUMBER)))

                if pckt[i].PID_TYPE == "PAT":
                    for j in range(8):
                        self.table_packet.item(row, j).setBackground(QtGui.QColor(255, 204, 223))
                if pckt[i].PID_TYPE == "SDT":
                    for j in range(8):
                        self.table_packet.item(row, j).setBackground(QtGui.QColor(173, 216, 230))
                if pckt[i].PID_TYPE == "PMT":
                    for j in range(8):
                        self.table_packet.item(row, j).setBackground(QtGui.QColor(252, 232, 131))
            except:
                pass
            row += 1


        #self.table_packet.setItem(3, 2, QtGui.QTableWidgetItem())
        #self.table_packet.item(3, 2).setBackground(QtGui.QColor(100, 100, 100))

        #brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        #brush.setStyle(QtCore.Qt.SolidPattern)
        #self.table_packet.item(3, 2).setBackground(brush)

        for i in range(len(pckt)):
            self.table_packet.resizeRowToContents(i)

        self.table_packet.resizeColumnToContents(0)
        self.table_packet.resizeColumnToContents(1)
        self.table_packet.resizeColumnToContents(2)
        self.table_packet.resizeColumnToContents(3)
        self.table_packet.resizeColumnToContents(4)
        self.table_packet.resizeColumnToContents(5)
        self.table_packet.resizeColumnToContents(6)
        self.table_packet.resizeColumnToContents(7)

        self.setFixedSize(823, 486)

        self.button_apply.clicked.connect(self.apply)


        self.show()

    def apply(self):
        self.table_packet.setColumnHidden(0,not(self.checkBox_1.isChecked()))
        self.table_packet.setColumnHidden(1,not(self.checkBox_2.isChecked()))
        self.table_packet.setColumnHidden(2,not(self.checkBox_3.isChecked()))
        self.table_packet.setColumnHidden(3,not(self.checkBox_4.isChecked()))
        self.table_packet.setColumnHidden(4,not(self.checkBox_5.isChecked()))
        self.table_packet.setColumnHidden(5,not(self.checkBox_6.isChecked()))
        self.table_packet.setColumnHidden(6,not(self.checkBox_7.isChecked()))
        self.table_packet.setColumnHidden(7,not(self.checkBox_8.isChecked()))


# about_dialog = QApplication(sys.argv)

# UIdialog = UId()
# about_dialog.exec()
