import os
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QTableWidgetItem, QMessageBox

import dialogdisplay
from TS import TS
import SDT
import PMT

import dialogabout
import dialogpidlist
import dialogpacketlist
import dialogremux
import dialoginfo


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        # uic.loadUi(self.resource_path("TS.ui"), self)
        # uic.loadUi("%s\\TS.ui"%os.getcwd(), self)
        # uic.loadUi(r"C:\Users\Soheil\Desktop\TS QT\output\TS.ui", self)

        # Import .ui forms for the GUI using function resource_path()
        ts_ui = resource_path("main.ui")
        uic.loadUi(ts_ui, self)

        self.setFixedSize(877, 525)
        self.table_text_status = True
        self.button_info.setEnabled(False)

        try:
            with open("config.ini", "r") as f:
                c = f.read()
                self.config = c.split('\n')
        except:
            with open("config.ini", "w") as f:
                SYNC_BYTE_DEC = False
                PID_DEC = True
                CONTINUITY_COUNT_DEC = True
                f.write(str(SYNC_BYTE_DEC))
                f.write('\n')
                f.write(str(PID_DEC))
                f.write('\n')
                f.write(str(CONTINUITY_COUNT_DEC))


        self.menu_open.triggered.connect(self.open)
        self.menu_exit.triggered.connect(self.exit)
        self.menu_about.triggered.connect(self.about)
        self.menu_pidlist.triggered.connect(self.pid_list)
        self.menu_packetlist.triggered.connect(self.packet_list)
        self.menu_remux.triggered.connect(self.remux)
        self.menu_display.triggered.connect(self.display)



        self.button_goto.clicked.connect(self.go)

        self.button_open.clicked.connect(self.open)
        self.button_first.clicked.connect(self.first)
        self.button_prev.clicked.connect(self.prev)
        self.button_next.clicked.connect(self.next)
        self.button_last.clicked.connect(self.last)
        self.button_ascii.clicked.connect(self.ascii)
        self.combo_find.addItem("PAT (0)")
        self.combo_find.addItem("CAT (1)")
        self.combo_find.addItem("NIT (16)")
        self.combo_find.addItem("SDT (17)")
        self.combo_find.addItem("EIT (18)")
        self.combo_find.addItem("TDT (20)")
        self.combo_find.activated.connect(self.combo_select)

        #self.button_open_in_text.clicked.connect(self.open_in_text)
        #self.radiobutton_table.toggled.connect(self.table_radio)
        #self.radiobutton_text.toggled.connect(self.text_radio)
        self.radiobutton_table.toggled.connect(self.table_text_toggle)
        self.radiobutton_text.toggled.connect(self.table_text_toggle)
        self.show()

    def open(self):
        try:
            print("Open")
            #try:
            self.path = QFileDialog.getOpenFileName(self, "Open File", "", "TS Files (*.ts)")
            print(self.path)
            if self.path[0] != '':
                self.entry_path.setText(self.path[0])
            self.file_size = os.path.getsize(self.path[0])
            self.number_of_packets = int(self.file_size / 188)
            self.entry_info.setText("%d bytes,  %d packets" % (self.file_size, self.number_of_packets))

            self.pckt = []
            self.pid_type_list = set()
            self.sdt_pckt = []
            self.sdt = []
            self.packet_count = [0 for i in range(8192)]
            with open(self.path[0], "rb") as f:
                for j in range(self.number_of_packets):
                    lst = []
                    for i in range(188):
                        bytes = ord(f.read(1))
                        # print(hex(ord(txt)))
                        lst.append(bytes)
                    self.progress_load.setRange(0, int(self.file_size / 188 - 1))
                    self.progress_load.setValue(j)
                    if j < self.number_of_packets:
                        self.statusbar.showMessage("Loading...")
                    self.pckt.append(TS(lst))
                    self.packet_count[self.pckt[j].PID] += 1
                    self.pid_type_list.add(self.pckt[j].PID)
                    if self.pckt[j].PID == 17:
                        if self.pckt[j].PAYLOAD not in self.sdt_pckt:
                            self.sdt_pckt.append(self.pckt[j].return_payload())
                            self.sdt += self.pckt[j].return_payload()

            self.statusbar.showMessage("Ready")
            self.ascii_state = False
            self.packet_index = 0



            print(len(self.sdt))
            print(self.sdt)

            self.SDT_P = SDT.SDT(self.sdt)
            print(len(self.SDT_P.PAYLOAD))
            print(self.SDT_P.PROGRAM_NAME)
            print(self.SDT_P.SERVICE_ID)
            self.show_func(self.packet_index)



        except:
            pass


    def first(self):
        try:
            self.packet_index = 0
            self.show_func(self.packet_index)
        except:
            pass

    def prev(self):
        try:
            self.packet_index -= 1
            if self.packet_index >= 0:
                self.show_func(self.packet_index)
            else:
                self.packet_index = 0
                print("ERROR")
        except:
            pass

    def next(self):
        try:
            self.packet_index += 1
            if self.packet_index <= len(self.pckt) - 1:
                self.show_func(self.packet_index)
            else:
                self.packet_index = len(self.pckt) - 1
                print("ERROR")
        except:
            pass

    def last(self):
        try:
            self.packet_index = len(self.pckt) - 1
            self.show_func(self.packet_index)
        except:
            pass

    def go(self):
        try:
            if self.radiobutton_packet.isChecked():
                self.packet_index = int(self.entry_goto.text()) - 1

            if self.radiobutton_pid.isChecked():
                if int(self.entry_goto.text()) not in self.pid_type_list:
                    msg = QMessageBox()
                    msg.setWindowTitle("Error!")
                    msg.setText("PID=%d not found!" %int(self.entry_goto.text()))
                    msg.setIcon(QMessageBox.Critical)
                    x = msg.exec_()

                else:
                    for i in range(self.number_of_packets):
                        if self.pckt[i].PID == int(self.entry_goto.text()):
                            self.packet_index = i
                            break

            self.show_func(self.packet_index)
        except:
            pass

    def ascii(self):
        try:
            self.ascii_state = not (self.ascii_state)
            self.show_func(self.packet_index)
        except:
            pass

    def combo_select(self):
        try:
            self.combo_state = self.combo_find.currentText()
            if self.combo_state == "PAT (0)":
                self.combo_find_pid = 0
            if self.combo_state == "CAT (1)":
                self.combo_find_pid = 1
            if self.combo_state == "NIT (16)":
                self.combo_find_pid = 16
            if self.combo_state == "SDT (17)":
                self.combo_find_pid = 17
            if self.combo_state == "EIT (18)":
                self.combo_find_pid = 18
            if self.combo_state == "TDT (20)":
                self.combo_find_pid = 20
            else:
                pass
            if self.combo_find_pid not in self.pid_type_list:
                msg = QMessageBox()
                msg.setWindowTitle("Error!")
                msg.setText("%s not found!" % self.combo_state)
                msg.setIcon(QMessageBox.Critical)
                x = msg.exec_()

            for i in range(self.number_of_packets):
                if self.pckt[i].PID == self.combo_find_pid:
                    self.packet_index = i
                    break
            self.show_func(self.packet_index)
        except:
            pass

    def show_func(self, packet_index):

        try:
            with open("config.ini", "r") as f:
                c = f.read()
                self.config = c.split('\n')
        except:
            with open("config.ini", "w") as f:
                SYNC_BYTE_DEC = False
                PID_DEC = True
                CONTINUITY_COUNT_DEC = True
                f.write(str(SYNC_BYTE_DEC))
                f.write('\n')
                f.write(str(PID_DEC))
                f.write('\n')
                f.write(str(CONTINUITY_COUNT_DEC))


        if self.config[0] == "True":
            self.entry_sync_byte.setText(str(self.pckt[packet_index].SYNC_BYTE))
        if self.config[0] == "False":
            self.entry_sync_byte.setText(hex(self.pckt[packet_index].SYNC_BYTE))
        self.entry_transport_error_indicator.setText(str(self.pckt[packet_index].TRANSPORT_ERROR_INDICATOR))
        self.entry_payload_unit_start_indicator.setText(str(self.pckt[packet_index].PAYLOAD_UNIT_START_INDICATOR))
        self.entry_transport_priority.setText(str(self.pckt[packet_index].TRANSPORT_PRIORITY))
        if self.config[1] == "True":
            self.entry_pid.setText(str(self.pckt[packet_index].PID))
        if self.config[1] == "False":
            self.entry_pid.setText(hex(self.pckt[packet_index].PID))
        self.entry_transport_scrambling_control.setText(str(self.pckt[packet_index].TRANSPORT_SCRAMBLING_CONTROL))
        self.entry_adaptation_field_control.setText(str(self.pckt[packet_index].ADAPTATION_FIELD_CONTROL))
        if self.config[2] == "True":
            self.entry_continuity_counter.setText(str(self.pckt[packet_index].CONTINUITY_COUNT))
        if self.config[1] == "False":
            self.entry_continuity_counter.setText(hex(self.pckt[packet_index].CONTINUITY_COUNT))

        self.PACKET = []
        for i in range(188):
            if self.ascii_state == False:
                self.PACKET.append(self.str_2_char(hex(self.pckt[packet_index].packet[i])[2:].upper()))
            if self.ascii_state == True:
                self.PACKET.append(chr(self.pckt[packet_index].packet[i]))
        # self.packet_text = ' '.join(self.PACKET)
        # self.text_packet_show.setText(str(self.packet_text))
        # self.yo = self.PACKET.copy()
        # self.packet_text = self.packet_text.split(' ')

        for i in range(4):
            self.PACKET.append(' ')

        #    for i in range(16):
        #        self.table_show.resizeColumnToContents(i)
        if self.table_text_status == True:
            self.text_show.hide()
            self.table_show.show()
            self.table_show.setRowCount(12)
            for i in range(12):
                for j in range(16):
                    self.table_show.setItem(i, j, QTableWidgetItem(self.PACKET[i * 16 + j]))

        if self.table_text_status == False:
            self.table_show.hide()
            text = ""
            for i in range(188):
                if i % 16 == 0 and i > 0:
                    text += "\n"
                text += '{} '.format(str(self.PACKET[i]))
            self.text_show.setText(text)
            self.text_show.show()

        self.frame_ts_packet.setTitle("TS packet %d" % (packet_index + 1))
        self.entry_pid_type.setText(self.pckt[packet_index].PID_TYPE)


        if self.pckt[packet_index].PAYLOAD[0] == 0:
            if self.pckt[packet_index].PID == 0:
                self.button_info.setEnabled(True)
                self.button_info.clicked.connect(self.info_d)

                self.more_info = """Table ID: %s
Section syntax indicator: %d
Section length: %d
Transport stream id: %d
Version number: %d
Current/next indicator: %d
Section number: %d
Last section number: %d""" % (hex(self.pckt[packet_index].TABLE_ID),
                                  self.pckt[packet_index].SECTION_SYNTAX_INDICATOR,
                                  self.pckt[packet_index].SECTION_LENGTH,
                                  self.pckt[packet_index].TRANSPORT_STREAM_ID,
                                  self.pckt[packet_index].VERSION_NUMBER,
                                  self.pckt[packet_index].CURRENT_NEXT_INDICATOR,
                                  self.pckt[packet_index].SECTION_NUMBER,
                                  self.pckt[packet_index].LAST_SECTION_NUMBER)
                # self.text_more_info.setText(self.more_info)
                self.more_info2 = ""
                self.more_info3 = ""
                for i in range(len(self.pckt[packet_index].PROGRAM_NUMBER)):
                    if self.pckt[packet_index].PROGRAM_NUMBER[i] == 0:
                        self.more_info2 += "Program number: %d => Network PID: %d\n" % (self.pckt[packet_index].PROGRAM_NUMBER[i], self.pckt[packet_index].PROGRAM_MAP_PID[i])
                        continue
                    self.more_info2 += "Program number: %d => Program map PID: %d\n" % (self.pckt[packet_index].PROGRAM_NUMBER[i], self.pckt[packet_index].PROGRAM_MAP_PID[i])
                self.more_info3 = "Section CRC: %s %s %s %s" % (
                    self.str_2_char(hex(self.pckt[packet_index].CRC[0])[2:].upper()),
                    self.str_2_char(hex(self.pckt[packet_index].CRC[1])[2:].upper()),
                    self.str_2_char(hex(self.pckt[packet_index].CRC[2])[2:].upper()),
                    self.str_2_char(hex(self.pckt[packet_index].CRC[3])[2:].upper()))
                self.text_more_info.setText(self.more_info + "\n\n\n" + self.more_info2 + "\n\n\n" + self.more_info3)


            elif self.pckt[packet_index].PID == 17:
                self.text_more_info.setText(self.SDT_P.INFO)
                self.button_info.setEnabled(True)
                self.button_info.clicked.connect(self.info_d)
            else:
                if self.pckt[packet_index].TABLE_ID == 2:
                    pmt = PMT.PMT(self.pckt[packet_index].PAYLOAD)
                    self.text_more_info.setText(pmt.INFO)
                    self.button_info.setEnabled(True)
                    self.button_info.clicked.connect(self.info_d)


                else:
                    self.text_more_info.setText("")
                    self.button_info.setEnabled(False)
        else:
            self.text_more_info.setText("")
            self.button_info.setEnabled(False)

        if self.pckt[packet_index].ADAPTATION_FIELD_CONTROL == 0:
            self.entry_adaptation_status.setText("ISO")
            self.entry_adaptation_byte_count.setText("")
            self.entry_adaptation_byte_count.setText(str(0))
        if self.pckt[packet_index].ADAPTATION_FIELD_CONTROL == 1:
            self.entry_adaptation_status.setText("No adaptation field, payload only")
            self.entry_adaptation_byte_count.setText(str(0))
        if self.pckt[packet_index].ADAPTATION_FIELD_CONTROL == 2:
            self.entry_adaptation_status.setText("Adaptation field only, No payload")
            self.entry_adaptation_byte_count.setText(str(self.pckt[packet_index].ADAPTATION_FIELD_LENGTH+1))
            self.text_more_info.setText(self.pckt[packet_index].INFO)
        if self.pckt[packet_index].ADAPTATION_FIELD_CONTROL == 3:
            self.entry_adaptation_status.setText("Adaptation field followed by payload")
            self.entry_adaptation_byte_count.setText(str(self.pckt[packet_index].ADAPTATION_FIELD_LENGTH+1))
            self.text_more_info.setText(self.pckt[packet_index].INFO)


    def about(self):
        self.dialog = dialogabout.DialogAbout()
        self.dialog.show()

    def pid_list(self):
        self.dialog = dialogpidlist.DialogPidList(self.packet_count)
        #self.dialog.packet_count = self.packet_count
        self.dialog.show()

    def packet_list(self):
        self.dialog = dialogpacketlist.DialogPacketList(self.pckt)
        #self.dialog.packet_count = self.packet_count
        self.dialog.show()

    def remux(self):
        self.dialog = dialogremux.DialogRemux(self.pckt)
        #self.dialog.packet_count = self.packet_count
        self.dialog.show()

    def display(self):
        self.dialog = dialogdisplay.DialogDisplay()
        self.dialog.show()
        if self.dialog.exec_() == 0:
            try:
                self.show_func(self.packet_index)
            except:
                pass

    def info_d(self):
        if self.pckt[self.packet_index].PID == 0:
            self.dialog = dialoginfo.DialogInfo(0 ,self.pckt[self.packet_index])
            #self.dialog.packet_count = self.packet_count
            self.dialog.show()
        if self.pckt[self.packet_index].PID == 17:
            self.dialog = dialoginfo.DialogInfo(17 ,self.SDT_P)
            #self.dialog.packet_count = self.packet_count
            self.dialog.show()
        if self.pckt[self.packet_index].TABLE_ID == 2:
            self.dialog = dialoginfo.DialogInfo(-1 ,self.pckt[self.packet_index])
            #self.dialog.packet_count = self.packet_count
            self.dialog.show()


    def text_radio(self):
        self.table_text_status = False
        print("Text")

    def table_text_toggle(self):
        if self.radiobutton_table.isChecked():
            self.table_text_status = True
            print(self.table_text_status)
            try:
                self.show_func(self.packet_index)
            except:
                self.table_show.show()
                self.text_show.hide()
        if self.radiobutton_text.isChecked():
            self.table_text_status = False
            print(self.table_text_status)
            try:
                self.show_func(self.packet_index)
            except:
                self.table_show.hide()
                self.text_show.show()

    def str_2_char(self, string):
        if len(string) == 2:
            return string
        else:
            return "0" + string



    def exit(self):
        sys.exit()


app = QApplication(sys.argv)

UIWindow = UI()
app.exec()
