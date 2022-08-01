from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QFileDialog, QLineEdit, QTextBrowser, \
    QGroupBox, QRadioButton, QComboBox, QStatusBar, QProgressBar, QTableWidget, QTableWidgetItem, QAction
import dialogabout
import dialogpidlist
from PyQt5 import uic
import sys
import os


class TS:
    def __init__(self, p):
        self.packet = p

        self.HEADER = self.packet[:4]
        self.PAYLOAD = self.packet[4:]

        self.SYNC_BYTE = self.HEADER[0]
        self.TRANSPORT_ERROR_INDICATOR = (self.HEADER[1] & (1 << 7)) >> 7
        self.PAYLOAD_UNIT_START_INDICATOR = (self.HEADER[1] & (1 << 6)) >> 6
        self.TRANSPORT_PRIORITY = (self.HEADER[1] & (1 << 5)) >> 5
        self.PID = ((self.HEADER[1] & 0b11111) << 8) | self.HEADER[2]
        self.TRANSPORT_SCRAMBLING_CONTROL = (self.HEADER[3] & (0b11 << 6)) >> 6
        self.ADAPTATION_FIELD_CONTROL = (self.HEADER[3] & (0b11 << 4)) >> 4
        self.CONTINUITY_COUNT = self.HEADER[3] & 0b1111

        self.PID_TYPE = ""

        if self.PID == 0:
            self.PID_TYPE = "PAT"
            self.TABLE_ID = self.PAYLOAD[1]
            self.SECTION_SYNTAX_INDICATOR = (self.PAYLOAD[1]&(1<<3))>>3
            self.SECTION_LENGTH = (((self.PAYLOAD[2]&0xF)<<8)|self.PAYLOAD[3])
            self.TRANSPORT_STREAM_ID = (self.PAYLOAD[4]<<8)|(self.PAYLOAD[5])
            self.VERSION_NUMBER = (self.PAYLOAD[6]&0b111110)>>1
            self.CURRENT_NEXT_INDICATOR = self.PAYLOAD[6]&1
            self.SECTION_NUMBER = self.PAYLOAD[7]
            self.LAST_SECTION_NUMBER = self.PAYLOAD[8]
            self.CRC = self.PAYLOAD[self.SECTION_LENGTH:self.SECTION_LENGTH + 4]
            self.PROGRAM_NUMBER = []
            self.PROGRAM_MAP_PID = []
            for i in range(9,173,4):
                self.PROGRAM_NUMBER.append(self.PAYLOAD[i]<<8|self.PAYLOAD[i+1])
                self.PROGRAM_MAP_PID.append((self.PAYLOAD[i+2]&0b11111)<<8|self.PAYLOAD[i+3])

        if self.PID == 1:
            self.PID_TYPE = "CAT"
        if self.PID == 16:
            self.PID_TYPE = "NIT"
        if self.PID == 17:
            self.PID_TYPE = "SDT"
            self.TABLE_ID = self.PAYLOAD[1]
            self.SECTION_SYNTAX_INDICATOR = (self.PAYLOAD[2]& 0x80) >> 7
            self.SECTION_LENGTH = (((self.PAYLOAD[2]&0xF)<<8)|self.PAYLOAD[3])
            self.TRANSPORT_STREAM_ID = (self.PAYLOAD[4]<<8)|(self.PAYLOAD[5])
            self.VERSION_NUMBER = (self.PAYLOAD[6]&0b111110)>>1
            self.CURRENT_NEXT_INDICATOR = self.PAYLOAD[6]&1
            self.SECTION_NUMBER = self.PAYLOAD[7]
            self.LAST_SECTION_NUMBER = self.PAYLOAD[8]
            self.ORIGINAL_NETWORK_ID = (self.PAYLOAD[9] << 8 )|(self.PAYLOAD[10])
        elif self.PID == 18:
            self.PID_TYPE = "NIT"
        elif self.PID == 20:
            self.PID_TYPE = "TDT"
        elif self.PID == 8191:
            self.PID_TYPE = "NULL Packet"


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()


        #uic.loadUi(self.resource_path("TS.ui"), self)
        #uic.loadUi("%s\\TS.ui"%os.getcwd(), self)
        #uic.loadUi(r"C:\Users\Soheil\Desktop\TS QT\output\TS.ui", self)

# Import .ui forms for the GUI using function resource_path()
        ts_ui = self.resource_path("TS.ui")
        uic.loadUi(ts_ui, self)

        self.setFixedSize(876, 431)

        self.statusbar = self.findChild(QStatusBar, "statusbar")


        self.menu_open = self.findChild(QAction, "menu_open")
        self.menu_exit = self.findChild(QAction, "menu_exit")
        self.menu_about = self.findChild(QAction, "menu_about")
        self.menu_pidlist = self.findChild(QAction, "menu_pidlist")


        self.menu_open.triggered.connect(self.open)
        self.menu_exit.triggered.connect(self.exit)
        self.menu_about.triggered.connect(self.about)
        self.menu_pidlist.triggered.connect(self.pid_list)

        self.label_path = self.findChild(QLabel, "label_path")
        self.entry_path = self.findChild(QLineEdit, "entry_path")
        self.label_info = self.findChild(QLabel, "label_info")
        self.entry_info = self.findChild(QLineEdit, "entry_info")

        self.entry_sync_byte = self.findChild(QLineEdit, "entry_sync_byte")
        self.entry_transport_error_indicator = self.findChild(QLineEdit, "entry_transport_error_indicator")
        self.entry_payload_unit_start_indicator = self.findChild(QLineEdit, "entry_payload_unit_start_indicator")
        self.entry_transport_priority = self.findChild(QLineEdit, "entry_transport_priority")
        self.entry_pid = self.findChild(QLineEdit, "entry_pid")
        self.entry_transport_scrambling_control = self.findChild(QLineEdit, "entry_transport_scrambling_control")
        self.entry_adaptation_field_control = self.findChild(QLineEdit, "entry_adaptation_field_control")
        self.entry_continuity_counter = self.findChild(QLineEdit, "entry_continuity_counter")

        self.label_status = self.findChild(QLabel, "label_status")
        self.entry_pid_type = self.findChild(QLineEdit, "entry_pid_type")

        self.radiobutton_packet.findChild(QRadioButton, "radiobutton_packet")
        self.radiobutton_pid.findChild(QRadioButton, "radiobutton_pid")

        self.entry_goto = self.findChild(QLineEdit, "entry_goto")
        self.button_goto = self.findChild(QPushButton, "button_goto")
        self.button_goto.clicked.connect(self.go)

        #self.text_packet_show = self.findChild(QTextBrowser, "text_packet_show")
        self.table_show = self.findChild(QTableWidget, "table_show")
        self.text_more_info = self.findChild(QTextBrowser, "text_more_info")

        self.frame_ts_packet = self.findChild(QGroupBox, "frame_ts_packet")

        self.button_open = self.findChild(QPushButton, "button_open")
        self.button_open.clicked.connect(self.open)
        self.button_first = self.findChild(QPushButton, "button_first")
        self.button_first.clicked.connect(self.first)
        self.button_prev = self.findChild(QPushButton, "button_prev")
        self.button_prev.clicked.connect(self.prev)
        self.button_next = self.findChild(QPushButton, "button_next")
        self.button_next.clicked.connect(self.next)
        self.button_last = self.findChild(QPushButton, "button_last")
        self.button_last.clicked.connect(self.last)
        self.button_ascii = self.findChild(QPushButton, "button_ascii")
        self.button_ascii.clicked.connect(self.ascii)
        self.combo_find = self.findChild(QComboBox, "combo_find")
        self.combo_find.addItem("PAT (0)")
        self.combo_find.addItem("CAT (1)")
        self.combo_find.addItem("NIT (16)")
        self.combo_find.addItem("SDT (17)")
        self.combo_find.addItem("EIT (18)")
        self.combo_find.addItem("TDT (20)")
        self.combo_find.activated.connect(self.combo_select)

        self.progress_load = self.findChild(QProgressBar, "progress_load")

        self.show()

    def open(self):
        print("Open")
        try:
            self.path = QFileDialog.getOpenFileName(self, "Open File", "", "TS Files (*.ts)")
            self.entry_path.setText(self.path[0])
            self.file_size = os.path.getsize(self.path[0])
            self.number_of_packets = int(self.file_size / 188)
            self.entry_info.setText("%d bytes,  %d packets" % (self.file_size, self.number_of_packets))

            self.pckt = []
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

            self.statusbar.showMessage("Ready")
            self.ascii_state = False
            self.packet_index = 0
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
            for i in range(self.number_of_packets):
                if self.pckt[i].PID == self.combo_find_pid:
                    self.packet_index = i
                    break
            self.show_func(self.packet_index)
        except:
            pass
        
    def show_func(self, packet_index):
        self.entry_sync_byte.setText(hex(self.pckt[packet_index].SYNC_BYTE))
        self.entry_transport_error_indicator.setText(str(self.pckt[packet_index].TRANSPORT_ERROR_INDICATOR))
        self.entry_payload_unit_start_indicator.setText(str(self.pckt[packet_index].PAYLOAD_UNIT_START_INDICATOR))
        self.entry_transport_priority.setText(str(self.pckt[packet_index].TRANSPORT_PRIORITY))
        self.entry_pid.setText(str(self.pckt[packet_index].PID))
        self.entry_transport_scrambling_control.setText(str(self.pckt[packet_index].TRANSPORT_SCRAMBLING_CONTROL))
        self.entry_adaptation_field_control.setText(str(self.pckt[packet_index].ADAPTATION_FIELD_CONTROL))
        self.entry_continuity_counter.setText(str(self.pckt[packet_index].CONTINUITY_COUNT))
        self.PACKET = []
        for i in range(188):
            if self.ascii_state == False:
                self.PACKET.append(self.str_2_char(hex(self.pckt[packet_index].packet[i])[2:].upper()))
            if self.ascii_state == True:
                self.PACKET.append(chr(self.pckt[packet_index].packet[i]))
        #self.packet_text = ' '.join(self.PACKET)
        #self.text_packet_show.setText(str(self.packet_text))
        self.yo = self.PACKET.copy()
        #self.packet_text = self.packet_text.split(' ')

        for i in range(4):
            self.yo.append(' ')

    #    for i in range(16):
    #        self.table_show.resizeColumnToContents(i)


        self.table_show.setRowCount(12)
        for i in range(12):
            for j in range(16):
                self.table_show.setItem(i, j, QTableWidgetItem(self.yo[i*16+j]))

        self.frame_ts_packet.setTitle("TS packet %d" % (packet_index + 1))
        self.entry_pid_type.setText(self.pckt[packet_index].PID_TYPE)

        if self.pckt[packet_index].PID == 0:
            self.more_info = """Table ID: %s
Section syntax indicator: %d
Section length: %d
Transport stream id: %d
Version number: %d
Current next: %d
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
                if self.pckt[packet_index].PROGRAM_NUMBER[i] > 10000:
                    continue
                self.more_info2 += "Program number: %d => Program map PID: %d\n" % (
                self.pckt[packet_index].PROGRAM_NUMBER[i], self.pckt[packet_index].PROGRAM_MAP_PID[i])
            self.more_info3 = "Section CRC: %s %s %s %s"  %(self.str_2_char(hex(self.pckt[packet_index].CRC[0])[2:].upper()), self.str_2_char(hex(self.pckt[packet_index].CRC[1])[2:].upper()),
            self.str_2_char(hex(self.pckt[packet_index].CRC[2])[2:].upper()), self.str_2_char(hex(self.pckt[packet_index].CRC[3])[2:].upper()))
            self.text_more_info.setText(self.more_info + "\n\n\n" + self.more_info2 + "\n\n\n" + self.more_info3)


        elif self.pckt[packet_index].PID == 17:
            self.more_info = """Table ID: %s
Section syntax indicator: %d
Section length: %d
Transport stream id: %d
Version number: %d
Current next: %d
Section number: %d
Last section number: %d""" % (hex(self.pckt[packet_index].TABLE_ID),
                              self.pckt[packet_index].SECTION_SYNTAX_INDICATOR,
                              self.pckt[packet_index].SECTION_LENGTH,
                              self.pckt[packet_index].TRANSPORT_STREAM_ID,
                              self.pckt[packet_index].VERSION_NUMBER,
                              self.pckt[packet_index].CURRENT_NEXT_INDICATOR,
                              self.pckt[packet_index].SECTION_NUMBER,
                              self.pckt[packet_index].LAST_SECTION_NUMBER)

            self.text_more_info.setText(self.more_info)

        else:
            self.text_more_info.setText("")

    def about(self):
        self.ui = dialogabout.UId()
        self.ui.show()

    def pid_list(self):
        self.ui = dialogpidlist.UId()
        self.ui.packet_count = self.packet_count
        self.ui.show()

    def str_2_char(self, string):
        if len(string) == 2:
            return string
        else:
            return "0"+string

    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

            
    def exit(self):
        sys.exit()


app = QApplication(sys.argv)

UIWindow = UI()
app.exec()
