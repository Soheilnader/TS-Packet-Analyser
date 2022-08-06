from PyQt5.QtWidgets import QDialog, QFileDialog
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


class DialogRemux(QDialog):
    def __init__(self, pckt):
        super(DialogRemux, self).__init__()

        self.current_packet = pckt
        # uic.loadUi(r"C:\Users\Soheil\Desktop\TS QT\dialogabout.ui", self)
        super().__init__()
        ts_ui = resource_path("dialogremux.ui")
        uic.loadUi(ts_ui, self)
        self.setFixedSize(346, 344)

        self.button_remux.clicked.connect(self.re_mux)
        self.button_browse.clicked.connect(self.browse)

        self.new_pckt = []
        self.selected_PID = []

        pid_type_list = []
        for i in range(len(pckt)):
            if pckt[i].PID in pid_type_list:
                continue
            pid_type_list.append(pckt[i].PID)

        self.pid_type_list_sorted = sorted(pid_type_list)
        print(self.pid_type_list_sorted)

        for i in range(len(self.pid_type_list_sorted)):
            self.list_PID.addItem(str(self.pid_type_list_sorted[i]))

        self.show()


    def re_mux(self):
        #print("Remux")
        #print(self.list_PID.selectedItems())
        self.selected_PID = []
        self.new_pckt = []
        output = ""
        for i in self.list_PID.selectedItems():
            if i.text() in self.selected_PID:
                continue
            self.selected_PID.append(int(i.text()))
        print(self.selected_PID)

        for i in range(len(self.current_packet)):
            if self.current_packet[i].PID in self.selected_PID:
                self.new_pckt += self.current_packet[i].HEADER+self.current_packet[i].PAYLOAD

        #print(self.new_pckt)

        with open(self.path[0], "wb") as f:
            f.write(bytearray(self.new_pckt))


    def browse(self):
        self.path = QFileDialog.getSaveFileName(self, "Open File", "", "TS Files (*.ts)")
        self.text_browse.setText(self.path[0])
        print(self.path)

# about_dialog = QApplication(sys.argv)

# UIdialog = UId()
# about_dialog.exec()
