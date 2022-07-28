from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QFileDialog, QLineEdit, QTextBrowser, QGroupBox, QRadioButton
from PyQt5 import uic
import sys
import os

class TS:
    def __init__(self, p):
        self.packet = p

        self.HEADER = self.packet[:4]
        self.PAYLOAD = self.packet[4:]

        self.SYNC_BYTE = self.HEADER[0]
        self.TRANSPORT_ERROR_INDICATOR = (self.HEADER[1]&(1<<7))>>7
        self.PAYLOAD_UNIT_START_INDICATOR = (self.HEADER[1]&(1<<6))>>6
        self.TRANSPORT_PRIORITY = (self.HEADER[1]&(1<<5))>>5
        self.PID = ((self.HEADER[1]&(0b11111))<<8)|self.HEADER[2]
        self.TRANSPORT_SCRAMBLING_CONTROL = (self.HEADER[3]&(0b11<<6))>>6
        self.ADAPTATION_FIELD_CONTROL = (self.HEADER[3]&(0b11<<4))>>4
        self.CONTINUITY_COUNT = self.HEADER[3]&(0b1111)

        self.PID_TYPE=""

        if self.PID == 0:
            self.PID_TYPE = "PAT"
            self.TABLE_ID = self.PAYLOAD[0]
            self.SECTION_SYNTAX_INDICATOR = (self.PAYLOAD[1]&(1<<3))>>3
            self.SECTION_LENGTH = (((self.PAYLOAD[2]&0xF)<<8)|self.PAYLOAD[3])
            self.TRANSPORT_STREAM_ID = (self.PAYLOAD[4]<<8)|(self.PAYLOAD[5])
            self.VERSION_NUMBER = (self.PAYLOAD[6]&0b111110)>>1
            self.CURRENT_NEXT_INDICATOR = self.PAYLOAD[6]&1
            self.SECTION_NUMBER = self.PAYLOAD[7]
            self.LAST_SECTION_NUMBER = self.PAYLOAD[8]
            self.CRC = self.PAYLOAD[180:]
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
        if self.PID == 18:
            self.PID_TYPE = "NIT"
        if self.PID == 20:
            self.PID_TYPE = "TDT"




class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        uic.loadUi(r"C:\Users\Soheil\Desktop\TS QT\TS.ui", self)
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

        self.text_packet_show = self.findChild(QTextBrowser, "text_packet_show")
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

        self.show()

    def open(self):
        print("Open")
        try:
            self.path = QFileDialog.getOpenFileName(self, "Open File", "", "TS Files (*.ts)")
            self.entry_path.setText(self.path[0])
            self.file_size = os.path.getsize(self.path[0])
            self.number_of_packets = int(self.file_size/188)
            self.entry_info.setText("%d bytes,  %d packets" %(self.file_size, self.number_of_packets))



            self.pckt = []
            with open(self.path[0], "rb") as f:
                for j in range(int(self.file_size/188)):
                    lst = []
                    for i in range(188):
                        bytes = ord(f.read(1))
                        #print(hex(ord(txt)))
                        lst.append(bytes)
                    self.label_status.setText("Loading data...")
                    self.pckt.append(TS(lst))

            
            self.label_status.setText("Ready")

            self.packet_index = 0
            self.show_func(self.packet_index)    


        except:
            pass

    def first(self):
            self.packet_index = 0
            self.show_func(self.packet_index)    
   

    def prev(self):
        self.packet_index -= 1
        if self.packet_index >=0:
            self.show_func(self.packet_index)    
        else:
            self.packet_index = 0
            print("ERROR") 

    def next(self):
        self.packet_index += 1
        if self.packet_index <= len(self.pckt)-1:
            self.show_func(self.packet_index)    
        else:
            self.packet_index = len(self.pckt)-1
            print("ERROR")

    def last(self):
        self.packet_index = len(self.pckt)-1
        self.show_func(self.packet_index)    

    def go(self):
        if self.radiobutton_packet.isChecked():
            self.packet_index = int(self.entry_goto.text())

        if self.radiobutton_pid.isChecked():
            for i in range(self.number_of_packets):
                if self.pckt[i].PID ==  int(self.entry_goto.text()):
                    self.packet_index = i
                    break
        self.show_func(self.packet_index)    


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
            self.PACKET.append(hex(self.pckt[packet_index].packet[i])[2:])
        self.packet_text = ' '.join(self.PACKET)
        self.text_packet_show.setText(str(self.packet_text))
        self.frame_ts_packet.setTitle("TS packet %d" %packet_index) 
        self.entry_pid_type.setText(self.pckt[packet_index].PID_TYPE)
        if self.pckt[packet_index].PID == 0:
            self.more_info = """Table ID: %d
Section syntax indicator: %d
Section length: %d
Transport stream id: %d
Version number: %d
Current next: %d
Section number: %d
Last section number: %d""" %(self.pckt[packet_index].TABLE_ID,
            self.pckt[packet_index].SECTION_SYNTAX_INDICATOR,
            self.pckt[packet_index].SECTION_LENGTH, 
            self.pckt[packet_index].TRANSPORT_STREAM_ID, 
            self.pckt[packet_index].VERSION_NUMBER, 
            self.pckt[packet_index].CURRENT_NEXT_INDICATOR, 
            self.pckt[packet_index].SECTION_NUMBER, 
            self.pckt[packet_index].LAST_SECTION_NUMBER)
            #self.text_more_info.setText(self.more_info)
            self.more_info2 = ""
            self.more_info3 = ""

            for i in range(len(self.pckt[packet_index].PROGRAM_NUMBER)):
                if self.pckt[packet_index].PROGRAM_NUMBER[i] > 10000:
                    continue
                self.more_info2 += "Program number: %d => Program map PID: %d\n" %(self.pckt[packet_index].PROGRAM_NUMBER[i], self.pckt[packet_index].PROGRAM_MAP_PID[i])
            self.more_info3 = "Section CRC: " + hex(self.pckt[packet_index].CRC[0])
            self.text_more_info.setText(self.more_info+"\n\n\n"+self.more_info2+"\n\n\n"+self.more_info3) 
        else:
            self.text_more_info.setText("")
app = QApplication(sys.argv)

UIWindow = UI()
app.exec()


