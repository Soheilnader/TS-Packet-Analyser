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
            self.label1.setText("Table ID:")
            self.entry1.setText(hex(input_packets.TABLE_ID))
            self.label2.setText("Section syntax indicator:")
            self.entry2.setText(str(input_packets.SECTION_SYNTAX_INDICATOR))
            self.label3.setText("Section length:")
            self.entry3.setText(str(input_packets.SECTION_LENGTH))
            self.label4.setText("Transport stream ID:")
            self.entry4.setText(str(input_packets.TRANSPORT_STREAM_ID))
            self.label5.setText("Version number:")
            self.entry5.setText(str(input_packets.VERSION_NUMBER))
            self.label6.setText("Current next indicator:")
            self.entry6.setText(str(input_packets.CURRENT_NEXT_INDICATOR))
            self.label7.setText("Section number:")
            self.entry7.setText(str(input_packets.SECTION_NUMBER))
            self.label8.setText("Last section number:")
            self.entry8.setText(str(input_packets.LAST_SECTION_NUMBER))
            self.label9.setText("CRC:")
            self.entry9.setText("%s %s %s %s" %(self.str_2_char(hex(input_packets.CRC[0])[2:].upper()),
                self.str_2_char(hex(input_packets.CRC[1])[2:].upper()),
                self.str_2_char(hex(input_packets.CRC[2])[2:].upper()),
                self.str_2_char(hex(input_packets.CRC[3])[2:].upper())))
            self.label10.hide()
            self.entry10.hide()

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
            self.label1.setText("Table ID:")
            self.entry1.setText(hex(input_packets.TABLE_ID))
            self.label2.setText("Section syntax indicator:")
            self.entry2.setText(str(input_packets.SECTION_SYNTAX_INDICATOR))
            self.label3.setText("Section length:")
            self.entry3.setText(str(input_packets.SECTION_LENGTH))
            self.label4.setText("Transport stream ID:")
            self.entry4.setText(str(input_packets.TRANSPORT_STREAM_ID))
            self.label5.setText("Version number:")
            self.entry5.setText(str(input_packets.VERSION_NUMBER))
            self.label6.setText("Current next indicator:")
            self.entry6.setText(str(input_packets.CURRENT_NEXT_INDICATOR))
            self.label7.setText("Section number:")
            self.entry7.setText(str(input_packets.SECTION_NUMBER))
            self.label8.setText("Last section number:")
            self.entry8.setText(str(input_packets.LAST_SECTION_NUMBER))
            self.label9.setText("CRC:")
            self.entry9.setText("%s %s %s %s" %(self.str_2_char(hex(input_packets.CRC[0])[2:].upper()),
                self.str_2_char(hex(input_packets.CRC[1])[2:].upper()),
                self.str_2_char(hex(input_packets.CRC[2])[2:].upper()),
                self.str_2_char(hex(input_packets.CRC[3])[2:].upper())))
            self.label10.setText("Original network ID:")
            self.entry10.setText(str(input_packets.ORIGINAL_NETWORK_ID))

            self.table_info.setColumnCount(12)
            self.table_info.setHorizontalHeaderLabels(['Service ID', 'Service provider name', 'Service name', 'EIT schedule flag', 'EIT present/following flag', 'Running status', 'Free CA mode', 'Descriptor Tag', 'Descriptor length', 'Service type', 'Service provider name length', 'Service name length'])
            self.table_info.setRowCount(len(input_packets.SERVICE_ID))
            row = 0
            for i in range(len(input_packets.SERVICE_ID)):
                self.table_info.setItem(row, 0, QTableWidgetItem(str(input_packets.SERVICE_ID[i])))
                self.table_info.setItem(row, 1, QTableWidgetItem(str(input_packets.SERVICE_PROVIDER_NAME[i])))
                self.table_info.setItem(row, 2, QTableWidgetItem(str(input_packets.SERVICE_NAME[i])))
                self.table_info.setItem(row, 3, QTableWidgetItem(str(input_packets.EIT_SCHEDULE_FLAG[i])))
                self.table_info.setItem(row, 4, QTableWidgetItem(str(input_packets.EIT_PRESENT_FOLLOWING_FLAG[i])))
                self.table_info.setItem(row, 5, QTableWidgetItem(str(input_packets.RUNNING_STATUS[i])))
                self.table_info.setItem(row, 6, QTableWidgetItem(str(input_packets.FREE_CA_MODE[i])))
                self.table_info.setItem(row, 7, QTableWidgetItem(str(input_packets.DESCRIPTOR_TAG[i])))
                self.table_info.setItem(row, 8, QTableWidgetItem(str(input_packets.DESCRIPTOR_LENGTH[i])))
                self.table_info.setItem(row, 9, QTableWidgetItem(str(input_packets.SERVICE_TYPE[i])))
                self.table_info.setItem(row, 10, QTableWidgetItem(str(input_packets.SERVICE_PROVIDER_NAME_LENGTH[i])))
                self.table_info.setItem(row, 11, QTableWidgetItem(str(input_packets.SERVICE_NAME_LENGTH[i])))


                row += 1
            for i in range(len(input_packets.SERVICE_ID)):
                self.table_info.resizeRowToContents(i)

            for i in range(12):
                self.table_info.resizeColumnToContents(i)


    def str_2_char(self, string):
        if len(string) == 2:
            return string
        else:
            return "0" + string

        self.show()


#about_dialog = QApplication(sys.argv)

#UIdialog = UId()
#about_dialog.exec()