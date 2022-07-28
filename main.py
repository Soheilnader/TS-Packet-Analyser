from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QFileDialog, QLineEdit, QTextBrowser, QGroupBox, QRadioButton
from PyQt5 import uic
import sys
import os

class TS:
    def __init__(self, packet):
        self.packet = packet

        self.HEADER = self.packet[:4]
        self.PAYLOAD = self.packet[5:]

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
            self.entry_sync_byte.setText(hex(self.pckt[self.packet_index].SYNC_BYTE))
            self.entry_transport_error_indicator.setText(str(self.pckt[self.packet_index].TRANSPORT_ERROR_INDICATOR))
            self.entry_payload_unit_start_indicator.setText(str(self.pckt[self.packet_index].PAYLOAD_UNIT_START_INDICATOR))
            self.entry_transport_priority.setText(str(self.pckt[self.packet_index].TRANSPORT_PRIORITY))
            self.entry_pid.setText(str(self.pckt[self.packet_index].PID))
            self.entry_transport_scrambling_control.setText(str(self.pckt[self.packet_index].TRANSPORT_SCRAMBLING_CONTROL))
            self.entry_adaptation_field_control.setText(str(self.pckt[self.packet_index].ADAPTATION_FIELD_CONTROL))
            self.entry_continuity_counter.setText(str(self.pckt[self.packet_index].CONTINUITY_COUNT))
            self.PACKET = []
            for i in range(188):
                self.PACKET.append(hex(self.pckt[self.packet_index].packet[i])[2:])
            self.packet_text = ' '.join(self.PACKET)
            self.text_packet_show.setText(str(self.packet_text))
            self.frame_ts_packet.setTitle("TS packet %d" % self.packet_index) 
            self.entry_pid_type.setText(self.pckt[self.packet_index].PID_TYPE)       


        except:
            pass
    def first(self):
            self.packet_index = 0
            self.entry_sync_byte.setText(hex(self.pckt[self.packet_index].SYNC_BYTE))
            self.entry_transport_error_indicator.setText(str(self.pckt[self.packet_index].TRANSPORT_ERROR_INDICATOR))
            self.entry_payload_unit_start_indicator.setText(str(self.pckt[self.packet_index].PAYLOAD_UNIT_START_INDICATOR))
            self.entry_transport_priority.setText(str(self.pckt[self.packet_index].TRANSPORT_PRIORITY))
            self.entry_pid.setText(str(self.pckt[self.packet_index].PID))
            self.entry_transport_scrambling_control.setText(str(self.pckt[self.packet_index].TRANSPORT_SCRAMBLING_CONTROL))
            self.entry_adaptation_field_control.setText(str(self.pckt[self.packet_index].ADAPTATION_FIELD_CONTROL))
            self.entry_continuity_counter.setText(str(self.pckt[self.packet_index].CONTINUITY_COUNT))
            self.PACKET = []
            for i in range(188):
                self.PACKET.append(hex(self.pckt[self.packet_index].packet[i])[2:])
            self.packet_text = ' '.join(self.PACKET)
            self.text_packet_show.setText(str(self.packet_text))
            self.frame_ts_packet.setTitle("TS Packet %d" % self.packet_index) 
            self.entry_pid_type.setText(self.pckt[self.packet_index].PID_TYPE)       
       

    def prev(self):
        self.packet_index -= 1
        if self.packet_index >=0:
            self.entry_sync_byte.setText(hex(self.pckt[self.packet_index].SYNC_BYTE))
            self.entry_transport_error_indicator.setText(str(self.pckt[self.packet_index].TRANSPORT_ERROR_INDICATOR))
            self.entry_payload_unit_start_indicator.setText(str(self.pckt[self.packet_index].PAYLOAD_UNIT_START_INDICATOR))
            self.entry_transport_priority.setText(str(self.pckt[self.packet_index].TRANSPORT_PRIORITY))
            self.entry_pid.setText(str(self.pckt[self.packet_index].PID))
            self.entry_transport_scrambling_control.setText(str(self.pckt[self.packet_index].TRANSPORT_SCRAMBLING_CONTROL))
            self.entry_adaptation_field_control.setText(str(self.pckt[self.packet_index].ADAPTATION_FIELD_CONTROL))
            self.entry_continuity_counter.setText(str(self.pckt[self.packet_index].CONTINUITY_COUNT))
            self.PACKET = []
            for i in range(188):
                self.PACKET.append(hex(self.pckt[self.packet_index].packet[i])[2:])
            self.packet_text = ' '.join(self.PACKET)
            self.text_packet_show.setText(str(self.packet_text))
            self.frame_ts_packet.setTitle("TS Packet %d" % self.packet_index)  
            self.entry_pid_type.setText(self.pckt[self.packet_index].PID_TYPE)       
 
        else:
            self.packet_index = 0
            print("ERROR") 

    def next(self):
        self.packet_index += 1
        if self.packet_index <= len(self.pckt)-1:
            self.entry_sync_byte.setText(hex(self.pckt[self.packet_index].SYNC_BYTE))
            self.entry_transport_error_indicator.setText(str(self.pckt[self.packet_index].TRANSPORT_ERROR_INDICATOR))
            self.entry_payload_unit_start_indicator.setText(str(self.pckt[self.packet_index].PAYLOAD_UNIT_START_INDICATOR))
            self.entry_transport_priority.setText(str(self.pckt[self.packet_index].TRANSPORT_PRIORITY))
            self.entry_pid.setText(str(self.pckt[self.packet_index].PID))
            self.entry_transport_scrambling_control.setText(str(self.pckt[self.packet_index].TRANSPORT_SCRAMBLING_CONTROL))
            self.entry_adaptation_field_control.setText(str(self.pckt[self.packet_index].ADAPTATION_FIELD_CONTROL))
            self.entry_continuity_counter.setText(str(self.pckt[self.packet_index].CONTINUITY_COUNT))
            self.PACKET = []
            for i in range(188):
                self.PACKET.append(hex(self.pckt[self.packet_index].packet[i])[2:])
            self.packet_text = ' '.join(self.PACKET)
            self.text_packet_show.setText(str(self.packet_text))
            self.frame_ts_packet.setTitle("TS Packet %d" % self.packet_index)   
            self.entry_pid_type.setText(self.pckt[self.packet_index].PID_TYPE)       
  

        else:
            self.packet_index = len(self.pckt)-1
            print("ERROR")

    def last(self):
        self.packet_index = len(self.pckt)-1
        self.entry_sync_byte.setText(hex(self.pckt[self.packet_index].SYNC_BYTE))
        self.entry_transport_error_indicator.setText(str(self.pckt[self.packet_index].TRANSPORT_ERROR_INDICATOR))
        self.entry_payload_unit_start_indicator.setText(str(self.pckt[self.packet_index].PAYLOAD_UNIT_START_INDICATOR))
        self.entry_transport_priority.setText(str(self.pckt[self.packet_index].TRANSPORT_PRIORITY))
        self.entry_pid.setText(str(self.pckt[self.packet_index].PID))
        self.entry_transport_scrambling_control.setText(str(self.pckt[self.packet_index].TRANSPORT_SCRAMBLING_CONTROL))
        self.entry_adaptation_field_control.setText(str(self.pckt[self.packet_index].ADAPTATION_FIELD_CONTROL))
        self.entry_continuity_counter.setText(str(self.pckt[self.packet_index].CONTINUITY_COUNT))
        self.PACKET = []
        for i in range(188):
            self.PACKET.append(hex(self.pckt[self.packet_index].packet[i])[2:])
        self.packet_text = ' '.join(self.PACKET)
        self.text_packet_show.setText(str(self.packet_text))
        self.frame_ts_packet.setTitle("TS Packet %d" % self.packet_index) 
        self.entry_pid_type.setText(self.pckt[self.packet_index].PID_TYPE)       
         

    def go(self):
        if self.radiobutton_packet.isChecked():
            self.packet_index = int(self.entry_goto.text())

        if self.radiobutton_pid.isChecked():
            for i in range(self.number_of_packets):
                if self.pckt[i].PID ==  int(self.entry_goto.text()):
                    self.packet_index = i
                    break

        self.entry_sync_byte.setText(hex(self.pckt[self.packet_index].SYNC_BYTE))
        self.entry_transport_error_indicator.setText(str(self.pckt[self.packet_index].TRANSPORT_ERROR_INDICATOR))
        self.entry_payload_unit_start_indicator.setText(str(self.pckt[self.packet_index].PAYLOAD_UNIT_START_INDICATOR))
        self.entry_transport_priority.setText(str(self.pckt[self.packet_index].TRANSPORT_PRIORITY))
        self.entry_pid.setText(str(self.pckt[self.packet_index].PID))
        self.entry_transport_scrambling_control.setText(str(self.pckt[self.packet_index].TRANSPORT_SCRAMBLING_CONTROL))
        self.entry_adaptation_field_control.setText(str(self.pckt[self.packet_index].ADAPTATION_FIELD_CONTROL))
        self.entry_continuity_counter.setText(str(self.pckt[self.packet_index].CONTINUITY_COUNT))
        self.PACKET = []
        for i in range(188):
            self.PACKET.append(hex(self.pckt[self.packet_index].packet[i])[2:])
        self.packet_text = ' '.join(self.PACKET)
        self.text_packet_show.setText(str(self.packet_text))
        self.frame_ts_packet.setTitle("TS Packet %d" % self.packet_index)
        self.entry_pid_type.setText(self.pckt[self.packet_index].PID_TYPE)



app = QApplication(sys.argv)

UIWindow = UI()
app.exec()


