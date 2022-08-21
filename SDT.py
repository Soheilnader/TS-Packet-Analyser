class SDT:
    def __init__(self, s):
        self.PAYLOAD = s
        try:
            self.PID_TYPE = "SDT"
            self.TABLE_ID = self.PAYLOAD[1]
            self.SECTION_SYNTAX_INDICATOR = (self.PAYLOAD[2] & 0x80) >> 7
            self.SECTION_LENGTH = (((self.PAYLOAD[2] & 0xF) << 8) | self.PAYLOAD[3])
            self.TRANSPORT_STREAM_ID = (self.PAYLOAD[4] << 8) | (self.PAYLOAD[5])
            self.VERSION_NUMBER = (self.PAYLOAD[6] & 0b111110) >> 1
            self.CURRENT_NEXT_INDICATOR = self.PAYLOAD[6] & 1
            self.SECTION_NUMBER = self.PAYLOAD[7]
            self.LAST_SECTION_NUMBER = self.PAYLOAD[8]
            self.ORIGINAL_NETWORK_ID = (self.PAYLOAD[9] << 8) | (self.PAYLOAD[10])

            self.i = 12
            self.service_index = 0
            self.SERVICE_ID = []
            self.EIT_SCHEDULE_FLAG = []
            self.EIT_PRESENT_FOLLOWING_FLAG = []
            self.RUNNING_STATUS = []
            self.FREE_CA_MODE = []
            #############DESCRIPTOR###################
            self.DESCRIPTORS_LOOP_LENGTH = []
            self.DESCRIPTOR_TAG = []
            self.DESCRIPTOR_LENGTH = []
            self.SERVICE_TYPE = []
            self.SERVICE_PROVIDER_NAME_LENGTH = []
            self.SERVICE_PROVIDER_NAME = []
            self.SERVICE_NAME_LENGTH = []
            self.SERVICE_NAME = []

            self.PROGRAM_NAME = []
            self.NAME = ""

            while self.i < self.SECTION_LENGTH - 8:
                self.NAME = ""
                self.j = 0
                self.SERVICE_ID.append((self.PAYLOAD[self.i] << 8) | self.PAYLOAD[self.i + 1])
                self.i += 2  # i=14 38
                self.EIT_SCHEDULE_FLAG.append((self.PAYLOAD[self.i] & 0x2) >> 1)
                self.EIT_PRESENT_FOLLOWING_FLAG.append(self.PAYLOAD[self.i] & 0x1)
                self.i += 1  # i = 15 39
                self.RUNNING_STATUS.append((self.PAYLOAD[self.i] & 0xE0) >> 5)
                self.FREE_CA_MODE.append((self.PAYLOAD[self.i] & 0x10) >> 4)
                self.DESCRIPTORS_LOOP_LENGTH.append(((self.PAYLOAD[self.i] & 0xF) << 8) | self.PAYLOAD[self.i + 1])
                self.i += 2
                self.DESCRIPTOR_TAG.append(self.PAYLOAD[self.i])
                self.i += 1
                self.DESCRIPTOR_LENGTH.append(self.PAYLOAD[self.i])
                self.i += 1
                self.SERVICE_TYPE.append(self.PAYLOAD[self.i])
                self.i += 1
                self.SERVICE_PROVIDER_NAME_LENGTH.append(self.PAYLOAD[self.i])
                self.i += 1
                self.STRING = ""
                for k in range(self.SERVICE_PROVIDER_NAME_LENGTH[self.service_index]):
                    self.STRING += chr(self.PAYLOAD[self.i])
                    self.i += 1
                self.SERVICE_PROVIDER_NAME.append(self.STRING)
                self.SERVICE_NAME_LENGTH.append(self.PAYLOAD[self.i])
                self.i += 1
                self.STRING = ""
                for k in range(self.SERVICE_NAME_LENGTH[self.service_index]):
                    self.STRING += chr(self.PAYLOAD[self.i])
                    self.i += 1
                self.SERVICE_NAME.append(self.STRING)

                self.service_index += 1


            self.CRC = self.PAYLOAD[self.SECTION_LENGTH:self.SECTION_LENGTH + 4]

            self.INFO = """table_id: %s
section_length: %d
transport_stream_id: %d
version_number: %d
current_next: %d
section_number: %d
last_section_number: %d \n\n
""" % (self.TABLE_ID, self.SECTION_LENGTH, self.TRANSPORT_STREAM_ID, self.VERSION_NUMBER, self.CURRENT_NEXT_INDICATOR,
       self.SECTION_NUMBER, self.LAST_SECTION_NUMBER)
            for i in range(len(self.SERVICE_NAME)):
                self.INFO += "Service ID: %d => %s %s\n" % (self.SERVICE_ID[i], self.SERVICE_PROVIDER_NAME[i], self.SERVICE_NAME[i])
            self.INFO += "\n\n\nSection CRC: %s %s %s %s" % (self.str_2_char(hex(self.CRC[0])[2:].upper()),
                                                             self.str_2_char(hex(self.CRC[1])[2:].upper()),
                                                             self.str_2_char(hex(self.CRC[2])[2:].upper()),
                                                             self.str_2_char(hex(self.CRC[3])[2:].upper()))
        except:
            pass

    def isEnglish(self, s):
        try:
            s.encode(encoding='utf-8').decode('ascii')
        except UnicodeDecodeError:
            return False
        else:
            return True

    def str_2_char(self, string):
        if len(string) == 2:
            return string
        else:
            return "0" + string

