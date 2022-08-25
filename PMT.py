class PMT:
    def __init__(self, p):
        self.PAYLOAD = p
        try:
            self.PID_TYPE = "PMT"
            self.TABLE_ID = self.PAYLOAD[1]
            self.SECTION_SYNTAX_INDICATOR = (self.PAYLOAD[2] & 0x80) >> 7
            self.SECTION_LENGTH = (((self.PAYLOAD[2] & 0xF) << 8) | self.PAYLOAD[3])
            self.PROGRAM_NUMBER = (self.PAYLOAD[4] << 8) | (self.PAYLOAD[5])
            self.VERSION_NUMBER = (self.PAYLOAD[6] & 0b111110) >> 1
            self.CURRENT_NEXT_INDICATOR = self.PAYLOAD[6] & 1
            self.SECTION_NUMBER = self.PAYLOAD[7]
            self.LAST_SECTION_NUMBER = self.PAYLOAD[8]
            self.PCR_PID = ((self.PAYLOAD[9] & 0b11111) << 8) | (self.PAYLOAD[10])
            self.PROGRAM_INFO_LENGTH = ((self.PAYLOAD[11] & 0xF) << 8) | (self.PAYLOAD[12])

            self.i = 13 + self.PROGRAM_INFO_LENGTH
            self.stream_index = 0
            self.STREAM_TYPE = []
            self.ELEMENTRY_PID = []
            self.ES_INFO_LENGTH = []
            self.RUNNING_STATUS = []
            self.FREE_CA_MODE = []

            while self.i < self.SECTION_LENGTH - 4 - self.PROGRAM_INFO_LENGTH:
                self.STREAM_TYPE.append(self.PAYLOAD[self.i])
                self.i += 1
                self.ELEMENTRY_PID.append(((self.PAYLOAD[self.i] & 0b11111) << 8) | (self.PAYLOAD[self.i + 1]))
                self.i += 2
                self.ES_INFO_LENGTH.append(((self.PAYLOAD[self.i] & 0xF) << 8) | (self.PAYLOAD[self.i + 1]))
                self.i += 2  # i = 15 39
                self.i += self.ES_INFO_LENGTH[self.stream_index]
                self.stream_index += 1

            self.CRC = self.PAYLOAD[self.SECTION_LENGTH:self.SECTION_LENGTH + 4]

            self.INFO = """table_id: %s
section_syntax_indicator: %s
section_length: %d
program_number: %d
version_number: %d
current_next: %d
section_number: %d
last_section_number: %d
pcr_pid: %d
program_info_length: %d \n\n
""" % (self.TABLE_ID, self.SECTION_SYNTAX_INDICATOR, self.SECTION_LENGTH, self.PROGRAM_NUMBER, self.VERSION_NUMBER,
       self.CURRENT_NEXT_INDICATOR,
       self.SECTION_NUMBER, self.LAST_SECTION_NUMBER, self.PCR_PID, self.PROGRAM_INFO_LENGTH)
            for i in range(len(self.STREAM_TYPE)):
                self.INFO += "Stream Type: %s => Elementary PID: %d\n" % (hex(self.STREAM_TYPE[i]), self.ELEMENTRY_PID[i])
            self.INFO += "\n\n\nSection CRC: %s %s %s %s" % (self.str_2_char(hex(self.CRC[0])[2:].upper()),
                                                             self.str_2_char(hex(self.CRC[1])[2:].upper()),
                                                             self.str_2_char(hex(self.CRC[2])[2:].upper()),
                                                             self.str_2_char(hex(self.CRC[3])[2:].upper()))
        except:
            pass


    def str_2_char(self, string):
        if len(string) == 2:
            return string
        else:
            return "0" + string
