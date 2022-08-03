from PyQt5.QtWidgets import QDialog, QApplication, QTableWidget, QTableWidgetItem
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


class DialogPidList(QDialog):
    def __init__(self, packet_count):
        super(DialogPidList, self).__init__()
        # uic.loadUi(r"C:\Users\Soheil\Desktop\TS QT\dialogpidlist.ui", self)
        ts_ui = resource_path("dialogpidlist.ui")
        uic.loadUi(ts_ui, self)
        self.setFixedSize(378, 322)

        #self.table_pid = self.findChild(QTableWidget, "table_pid")
        #self.label_pid = self.findChild(QLabel, "label_pid")

        self.table_pid.setColumnWidth(0, 40)
        self.table_pid.setColumnWidth(1, 40)
        self.table_pid.setColumnWidth(2, 40)
        self.table_pid.setColumnWidth(3, 200)

        self.non_zero_count = 0
        for i in range(len(packet_count)):
            if packet_count[i] != 0:
                self.non_zero_count += 1

        self.table_pid.setRowCount(self.non_zero_count)
        row = 0
        total = sum(packet_count)
        for i in range(len(packet_count)):
            if packet_count[i] == 0:
                continue
            self.table_pid.setItem(row, 0, QTableWidgetItem(str(i)))
            self.table_pid.setItem(row, 1, QTableWidgetItem(str(packet_count[i])))
            self.table_pid.setItem(row, 2, QTableWidgetItem(str(round(packet_count[i]*100/total, 2))))
            if i == 0:
                self.table_pid.setItem(row, 3, QTableWidgetItem("PAT"))
            if i == 1:
                self.table_pid.setItem(row, 3, QTableWidgetItem("CAT"))
            if i == 16:
                self.table_pid.setItem(row, 3, QTableWidgetItem("NIT"))
            if i == 17:
                self.table_pid.setItem(row, 3, QTableWidgetItem("SDT"))
            if i == 18:
                self.table_pid.setItem(row, 3, QTableWidgetItem("EIT"))
            if i == 20:
                self.table_pid.setItem(row, 3, QTableWidgetItem("TDT"))
            if i == 8191:
                self.table_pid.setItem(row, 3, QTableWidgetItem("NULL Packet"))
            #if
            row+=1

        for i in range(self.non_zero_count):
            self.table_pid.resizeRowToContents(i)

        #self.tttttt = main.UI()
        self.label_packet_count.setText("%s packets analysed" %str(total))
        self.label_pid_used.setText("%s PIDs in use" %str(self.non_zero_count))

        self.show()


app = QApplication(sys.argv)
'''
UIWindow = UId()
app.exec()
'''
