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

# Used by Lua for data & version verification
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


class Verbosity(enum.Enum):
    '''
    Used to track Parser verbosity level
    '''
    OFF = 0
    INFO = 1
    VERBOSE = 2


class Parser():
    def __init__(self, filename, verbosity=Verbosity.OFF):
        '''
        :param filename: Lua bytecode file to be parsed
        :param verbosity: 0-2 verbosity level
        '''
        self.f = open(filename, "rb")
        self.int_size = LUAC_INT_SIZE
        self.num_size = LUAC_NUM_SIZE
        self.size_upvalues = None
        # Every program has one main function, with the other functions
        # going into the Functions.protos list of the main one
        self.func = None
        self.verbosity = verbosity

    def error(self, message):
        raise Exception(message)

    def error_unexpected(self, data, expected):
        raise Exception("Unexpected data: {} Expected: {}".format(data, expected))

    def is_info_level(self):
        return self.verbosity == Verbosity.INFO or \
                self.verbosity == Verbosity.VERBOSE

    def is_verbose_level(self):
        return self.verbosity == Verbosity.VERBOSE

    def read_byte(self, n=1) -> bytes:
        """ Read in one byte and return it """
        if n == 0:
            return None
        return self.f.read(n)

    def read_integer(self):
        """ Read in Lua Integer (distinct from read_int()) """
        return self.f.read(self.int_size)

    def read_num(self):
        """ Read in lua num (float) """
        return self.f.read(self.num_size)

    def read_unsigned(self, limit) -> int:
        """
        7 bits for each byte are used for data storage, the most significant bit
        Is used as a flag to indicate if it is the last byte in the sequence
        :returns: An integer containing the size value
        """
        x = 0
        b = 0
        limit = limit >> 7
        while True:
            b = int.from_bytes(self.read_byte(), ENDIANNESS)
            if x >= limit:
                self.error("Integer Overflow")
            if self.is_verbose_level():
                print("BYTE: {}".format(hex(b)))
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
        if size == 0:
            return None
        size = size - 1
        out = self.read_byte(size).decode("utf-8")
        if self.is_info_level():
            print("String: {}".format(out))
        return out

    def verify_data(self, data, expected):
        if self.is_info_level():
            print("Verifying Data: " + data.hex())
        if data != expected:
            self.error_unexpected(hex(data), hex(expected))

    def verify_value(self, value, expected):
        if self.is_info_level():
            print("Verifying Value: " + str(value))
        if value != expected:
            self.error_unexpected(str(data), str(expected))

    def read_code(self, func):
        """
        Load code, add data members to func
        :param Function: func 
        """
        n = self.read_int()
        for i in range(0, n):
            word = self.read_byte(4)
            inst = Inst(int.from_bytes(word, ENDIANNESS))

    def read_constants(self, func):
        """
        Load constants, add members to func
        :param Function: func
        """
        n = self.read_int()

        for i in range(0, n):
            t = int.from_bytes(self.read_byte(), ENDIANNESS)
            if t == Variant.VNIL or t == Variant.VFALSE or t == Variant.VTRUE:
                if self.is_info_level():
                    print("Constant {} {}".format(Variant(t).name, False))
                func.add_constant(Variant(t), False)

            elif t == Variant.VNUMFLT:
                n = self.read_num()
                if self.is_info_level():
                    print("Constant {} {}".format(Variant(t).name, n))
                func.add_constant(Variant(t), n)

            elif t == Variant.VNUMINT:
                n = self.read_integer()
                if self.is_info_level():
                    print("Constant {} {}".format(Variant(t).name, n))
                func.add_constant(Variant(t), n)

            elif t == Variant.VSHRSTR or t == Variant.VLNGSTR:
                s = self.read_string()
                if self.is_info_level():
                    print("Constant {} {}".format(Variant(t).name, s))
                func.add_constant(Variant(t), s)

            else:
                self.error("Unexpected const type: {}".format(t))

    def read_upvalues(self, func):
        """
        Read function upvalues
        :param func: The function containing the upvalues
        """
        n = self.read_int()
        for i in range(0, n):
            instack = int.from_bytes(self.read_byte(), ENDIANNESS)
            idx = int.from_bytes(self.read_byte(), ENDIANNESS)
            kind = int.from_bytes(self.read_byte(), ENDIANNESS)
            if self.is_info_level():
                print("Upvalue: {} {} {}".format(instack, idx, kind))
            func.add_upvalue(None, instack, idx, kind)

    def read_protos(self, func):
        """
        Read function prototypes
        Note: prototypes are just more functions, 
        this is just how they're scoped in Lua
        :param func: The function containing the prototypes
        """
        n = self.read_int()
        for i in range(0, n):
            f = self.read_function(func)
            print("Adding proto")
            func.add_proto(f)

    def read_debug(self, func):
        """
        Read function debug information
        :param func: The function containing the debug information
        """
        n = self.read_int()
        # FTODO how to parse this
        func.line_info = self.read_byte(n)

        n = self.read_int()
        for i in range(0, n):
            # TODO verify this works
            pc = self.read_int()
            line = self.read_int()
            if self.is_info_level():
                print("pc {}, line {}".format(pc, line))
            func.add_abs_line_info(pc, line)

        n = self.read_int()
        for i in range(0, n):
            var_name = self.read_string()
            start_pc = self.read_int()
            end_pc = self.read_int()
            if self.is_info_level():
                print("Local var {} {} {}".format(var_name, start_pc, end_pc))
            func.add_local_var(var_name, start_pc, end_pc)

        n = self.read_int()
        if n != len(func.upvalues):
            self.error("Mismatched upvalue names and values!")
        s = self.read_string()
        for i in range(0, n):
            if self.is_info_level():
                print("Upvalue name: {}".format(s))
            func.upvalues[i].name = s

    def parse_program_header(self):
        """
        Verify the funcion header
        """
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

        buf = self.read_integer()
        self.verify_value(int.from_bytes(buf, ENDIANNESS), LUAC_INT)
        
        buf = self.read_num()
        self.verify_value(struct.unpack("d", buf)[0], LUAC_NUM)

    def read_function(self, parent=None):
        f = Function()
        f.source = self.read_string()
        if self.is_info_level():
            print("Function name: {}".format(f.source))
        if f.source is None and parent is not None:
            f.source = parent.source

        f.line_defined = self.read_int()
        f.last_line_defined = self.read_int()
        f.num_params = int.from_bytes(self.read_byte(), ENDIANNESS)
        f.is_vararg = int.from_bytes(self.read_byte(), ENDIANNESS)
        f.max_stack_size = int.from_bytes(self.read_byte(), ENDIANNESS)
        if self.is_info_level():
            print("Params: {}, is_vararg: {}, max_stack_size: {}"
                    .format(f.num_params, f.is_vararg, f.max_stack_size))
        self.read_code(f)
        # Constants
        self.read_constants(f)
        # Upvalues
        self.read_upvalues(f)
        # Protos
        # TODO verify read_protos works
        self.read_protos(f)
        # Debug
        self.read_debug(f)

        return f


    def parse(self):
        self.parse_program_header()
        #i = Inst()
        self.size_upvalues = self.read_byte()
        self.func = self.read_function()




