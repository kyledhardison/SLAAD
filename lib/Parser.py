#!/usr/bin/env python3 

import binascii
import struct
from .Instruction import Inst

# FTODO: Support big endian
ENDIANNESS = "little"

# Constants for Version 5.4.4
PROGRAM_HEADER = b"\x1b\x4c\x75\x61"  # \x1bLua
PROGRAM_VERSION = b"\x54"
LUAC_FORMAT= b"\x00"
LUAC_DATA = b"\x19\x93\x0d\x0a\x1a\x0a"
LUAC_INSTRUCTION_SIZE = b"\x04"
# Int and Num sizes can vary by platform - reasonable defaults
LUAC_INT_SIZE = b"\x08"
LUAC_NUM_SIZE = b"\x08"
LUAC_INT = 0x5678
LUAC_NUM = 370.5

class Parser():
    def __init__(self, filename):
        self.f = open(filename, 'rb')
        self.int_size = LUAC_INT_SIZE
        self.num_size = LUAC_NUM_SIZE
        self.sizeup_values = None

    def read_byte(self, n=1):
        return self.f.read(n)

    def read_int(self):
        return self.f.read(self.int_size)

    def read_num(self):
        return self.f.read(self.num_size)

    def verify_data(self, data, expected):
        print("data: " + data.hex())
        if data != expected:
            raise Exception("Unexpected data: " + data.hex() + 
                            " Expected: " + expected.hex())
    def verify_value(self, value, expected):
        print("value: " + str(value))
        if value != expected:
            raise Exception("Unexpected value: " + str(value) + 
                            " Expected: " + str(expected))

    def parse_program_header(self):
        buf = self.read_byte(len(PROGRAM_HEADER))
        self.verify_data(buf, PROGRAM_HEADER)

        buf = self.read_byte(len(PROGRAM_VERSION))
        self.verify_data(buf, PROGRAM_VERSION)

        buf = self.read_byte(len(LUAC_FORMAT))
        self.verify_data(buf, LUAC_FORMAT)

        buf = self.read_byte(len(LUAC_DATA))
        self.verify_data(buf, LUAC_DATA)

        buf = self.read_byte()
        self.verify_data(buf, LUAC_INSTRUCTION_SIZE)

        buf = self.read_byte()
        self.verify_data(buf, LUAC_INT_SIZE)
        self.int_size = int.from_bytes(buf, ENDIANNESS)

        buf = self.read_byte()
        self.verify_data(buf, LUAC_NUM_SIZE)
        self.num_size = int.from_bytes(buf, ENDIANNESS)

        buf = self.read_int()
        self.verify_value(int.from_bytes(buf, ENDIANNESS), LUAC_INT)
        
        buf = self.read_num()
        self.verify_value(struct.unpack('d', buf)[0], LUAC_NUM)


    def parse(self):
        self.parse_program_header()
        i = Inst()
        
