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
            self.SECTION_SYNTAX_INDICATOR = (self.PAYLOAD[2] & 0x80) >> 7
            self.SECTION_LENGTH = (((self.PAYLOAD[2] & 0xF) << 8) | self.PAYLOAD[3])
            self.TRANSPORT_STREAM_ID = (self.PAYLOAD[4] << 8) | (self.PAYLOAD[5])
            self.VERSION_NUMBER = (self.PAYLOAD[6] & 0b111110) >> 1
            self.CURRENT_NEXT_INDICATOR = self.PAYLOAD[6] & 1
            self.SECTION_NUMBER = self.PAYLOAD[7]
            self.LAST_SECTION_NUMBER = self.PAYLOAD[8]
            self.CRC = self.PAYLOAD[self.SECTION_LENGTH:self.SECTION_LENGTH + 4]
            self.PROGRAM_NUMBER = []
            self.PROGRAM_MAP_PID = []
            for i in range(9, 173, 4):
                self.PROGRAM_NUMBER.append(self.PAYLOAD[i] << 8 | self.PAYLOAD[i + 1])
                self.PROGRAM_MAP_PID.append((self.PAYLOAD[i + 2] & 0b11111) << 8 | self.PAYLOAD[i + 3])

        if self.PID == 1:
            self.PID_TYPE = "CAT"
            self.TABLE_ID = self.PAYLOAD[1]
            self.SECTION_SYNTAX_INDICATOR = (self.PAYLOAD[2] & 0x80) >> 7
            self.SECTION_LENGTH = (((self.PAYLOAD[2] & 0xF) << 8) | self.PAYLOAD[3])
            self.VERSION_NUMBER = (self.PAYLOAD[6] & 0b111110) >> 1
            self.CURRENT_NEXT_INDICATOR = self.PAYLOAD[6] & 1
            self.SECTION_NUMBER = self.PAYLOAD[7]
            self.LAST_SECTION_NUMBER = self.PAYLOAD[8]
            self.CRC = self.PAYLOAD[self.SECTION_LENGTH:self.SECTION_LENGTH + 4]

        if self.PID == 16:
            self.PID_TYPE = "NIT"
            self.TABLE_ID = self.PAYLOAD[1]
            self.SECTION_SYNTAX_INDICATOR = (self.PAYLOAD[2] & 0x80) >> 7
            self.SECTION_LENGTH = (((self.PAYLOAD[2] & 0xF) << 8) | self.PAYLOAD[3])
            self.NETWORK_ID = (self.PAYLOAD[4] << 8) | (self.PAYLOAD[5])
            self.VERSION_NUMBER = (self.PAYLOAD[6] & 0b111110) >> 1
            self.CURRENT_NEXT_INDICATOR = self.PAYLOAD[6] & 1
            self.SECTION_NUMBER = self.PAYLOAD[7]
            self.LAST_SECTION_NUMBER = self.PAYLOAD[8]
            self.NETWORK_DESCRIPTORS_LENGTH = ((self.PAYLOAD[9] & 0xF) << 8) | self.PAYLOAD[10]
            self.CRC = self.PAYLOAD[self.SECTION_LENGTH:self.SECTION_LENGTH + 4]

        if self.PID == 17:
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
        elif self.PID == 18:
            self.PID_TYPE = "NIT"
        elif self.PID == 20:
            self.PID_TYPE = "TDT"
        elif self.PID == 8191:
            self.PID_TYPE = "NULL Packet"
