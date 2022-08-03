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

        self.show()

# about_dialog = QApplication(sys.argv)

# UIdialog = UId()
# about_dialog.exec()
