#!/usr/bin/env python3 

import binascii
import enum
import struct
from .Instruction import Inst
from .Function import Function
from .Opcode import Opcode
from .Types import *

# FTODO: Support big endian
ENDIANNESS = "little"

# Constants for Version 5.4.4
PROGRAM_HEADER = b"\x1b\x4c\x75\x61"  # \x1bLua
PROGRAM_VERSION = b"\x54"
LUAC_FORMAT= b"\x00"
LUAC_DATA = b"\x19\x93\x0d\x0a\x1a\x0a"
LUAC_INSTRUCTION_SIZE = b"\x04"
# Int and Num sizes can vary by platform - FTODO support others
LUAC_INT_SIZE = b"\x08"
LUAC_NUM_SIZE = b"\x08"
LUAC_INT = 0x5678
LUAC_NUM = 370.5


class Parser():
    def __init__(self, filename, verbose=False):
        self.f = open(filename, 'rb')
        self.int_size = LUAC_INT_SIZE
        self.num_size = LUAC_NUM_SIZE
        self.sizeup_values = None
        self.verbose = verbose

    def error(self, message):
        raise Exception(message)

    def error_unexpected(self, data, expected):
        raise Exception("Unexpected data: {} Expected: {}".format(data, expected))

    def read_byte(self, n=1) -> bytes:
        ''' Read in one byte and return it '''
        return self.f.read(n)

    def read_luac_int(self):
        ''' Used to read in Lua int constant '''
        return self.f.read(self.int_size)

    def read_luac_num(self):
        ''' Used to read in Lua number constant ''' 
        return self.f.read(self.num_size)

    def read_unsigned(self, limit) -> int:
        '''
        7 bits for each byte are used for data storage, the most significant bit
        Is used as a flag to indicate if it is the last byte in the sequence
        :returns: An integer containing the size value
        '''
        x = 0
        b = 0
        limit = limit >> 7
        while True:
            b = int.from_bytes(self.read_byte(), ENDIANNESS)
            if x >= limit:
                self.error("Integer Overflow")
            if self.verbose:
                print("BYTE: {}".format(b))
            x = (x << 0x07) | (b & 0x7f)
            if ((b & 0x80) != 0):
                break
        return x

    def read_size(self) -> int:
        return self.read_unsigned(0xffffffffffffffff)  # ~(size_t)0

    def read_int(self) -> int:
        return self.read_unsigned(2147483647)  # MAX_INT

    def read_string(self) -> str:
        size = self.read_size()
        if self.verbose:
            print('size: {}'.format(size))
        size = size - 1
        out = self.read_byte(size)
        if self.verbose:
            print(out)
        return out

    def verify_data(self, data, expected):
        if self.verbose:
            print("data: " + data.hex())
        if data != expected:
            self.error_unexpected(hex(data), hex(expected))

    def verify_value(self, value, expected):
        if self.verbose:
            print("value: " + str(value))
        if value != expected:
            self.error_unexpected(str(data), str(expected))

    def read_code(self, func):
        '''
        Load code, add data members to func
        :param Function: func 
        '''
        func.size_code = self.read_int()
        for i in range(0, func.size_code):
            word = self.read_byte(4)
            inst = Inst(int.from_bytes(word, ENDIANNESS))
            # inst.print_inst()

    def read_constants(self, func):
        '''
        Load constants, add members to func
        :param Function: func
        '''
        func.size_constants = self.read_int()

        for i in range(0, func.size_constants):
            t = int.from_bytes(self.read_byte(), ENDIANNESS)
            if t == Variant.VNIL or t == Variant.VFALSE or t == Variant.VTRUE:
                if self.verbose:
                    print("Const {} {}".format(Variant(t), s))
                func.add_constant(Variant(t), False)
            elif t == Variant.VNUMFLT:
                # TODO read_number
                #num = self.read_number()
                if self.verbose:
                    print("Const {} {}".format(Variant(t), s))
                pass
            elif t == Variant.VNUMINT:
                n = self.read_int()
                if self.verbose:
                    print("Const {} {}".format(Variant(t), s))
                func.add_constant(Variant(t), num)
            elif t == Variant.VSHRSTR or t == Variant.VLNGSTR:
                s = str(self.read_string())
                if self.verbose:
                    print("Const {} {}".format(Variant(t), s))
                func.add_constant(Variant(t), s)
            else:
                self.error('Unexpected const type: {}'.format(t))

    def read_upvalues(self, func):
        n = self.read_int()
        print(n)

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

        buf = self.read_luac_int()
        self.verify_value(int.from_bytes(buf, ENDIANNESS), LUAC_INT)
        
        buf = self.read_luac_num()
        self.verify_value(struct.unpack('d', buf)[0], LUAC_NUM)

    def read_function(self):
        f = Function()
        f.source = str(self.read_string())
        f.line_defined = self.read_int()
        f.last_line_defined = self.read_int()
        f.num_params = int.from_bytes(self.read_byte(), ENDIANNESS)
        f.is_vararg = int.from_bytes(self.read_byte(), ENDIANNESS)
        f.max_stack_size = int.from_bytes(self.read_byte(), ENDIANNESS)
        if self.verbose:
            print(f.num_params, f.is_vararg, f.max_stack_size)
        self.read_code(f)
        # Constants
        self.read_constants(f)
        # Upvalues
        self.read_upvalues(f)
        # Protos
        # Debug


    def parse(self):
        self.parse_program_header()
        #i = Inst()
        self.sizeupvalues = self.read_byte()
        self.read_function()




