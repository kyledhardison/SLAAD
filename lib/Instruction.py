
from .Opcode import *


class Inst():
    """
    Used to identify instructions and parse their data
    """
    # Instruction definitions, taken from lopcodes.h
    SIZE_C  =   8
    SIZE_B  =   8
    SIZE_Bx =   SIZE_C + SIZE_B - 1
    SIZE_A  =   8
    SIZE_Ax =   SIZE_Bx + SIZE_A
    SIZE_sJ =   SIZE_Bx + SIZE_A

    SIZE_OP =   7
    POS_OP  =   0

    POS_A   =   (POS_OP + SIZE_OP)
    POS_k   =   (POS_A + SIZE_A)
    POS_B   =   (POS_k + 1)
    POS_C   =   (POS_B + SIZE_B)

    POS_Bx  =   POS_k
    POS_sBx =   POS_k
    POS_Ax  =   POS_A
    POS_sJ  =   POS_A
    
    # Signed arguments are represented in excess-K (offset binary) notation.
    # The represented value is the written unassigned value minus K, where
    # K is half of the maximum for a given field (2 ^ (n-1)) - 1
    K_8_BIT  =  127  # 2^7 - 1
    K_17_BIT =  65535  # 2^16 - 1
    K_25_BIT =  16777215  # 2^24 - 1

    MASK_OP = 0b00000000000000000000000001111111
    MASK_A  = 0b00000000000000000111111110000000
    MASK_k  = 0b00000000000000001000000000000000
    MASK_B  = 0b00000000111111110000000000000000
    MASK_C  = 0b11111111000000000000000000000000
    MASK_Bx = 0b11111111111111111000000000000000
    MASK_sBx= 0b11111111111111111000000000000000
    MASK_Ax = 0b11111111111111111111111110000000
    MASK_sJ = 0b11111111111111111111111110000000

    def __init__(self, instruction):
        '''
        Parse an instruction from raw bytes
        :param raw_instruction: the raw 32-bit instruction
        :param endianness: "little" or "big"
        '''
        self.arg_A = None
        self.arg_B = None
        self.arg_C = None
        self.arg_k = None
        self.arg_Bx = None
        self.arg_sBx = None
        self.arg_Ax = None
        self.arg_sJ = None
        self.opcode = Opcode(instruction & Inst.MASK_OP)
        self.opmode = Opmodes.opmodes[self.opcode.value] 
        self.desc = Opmodes.opdesc[self.opcode.value]
        self.InstFormat = self.opmode.mode
        self.inst_print_len = 12  # Longest opcode string is 10, plus some padding

        if self.InstFormat == InstFormat.iABC:
            self.arg_A = (instruction & Inst.MASK_A) >> Inst.POS_A
            self.arg_B = (instruction & Inst.MASK_B) >> Inst.POS_B
            self.arg_C = (instruction & Inst.MASK_C) >> Inst.POS_C
            self.arg_k = (instruction & Inst.MASK_k) >> Inst.POS_k

            # Adjust for signing
            if self.opmode.has_B == Arg.S:
                self.arg_B -= Inst.K_8_BIT
            elif self.opmode.has_C == Arg.S:
                self.arg_C -= Inst.K_8_BIT

        elif self.InstFormat == InstFormat.iABx:
            self.arg_A = (instruction & Inst.MASK_A) >> Inst.POS_A
            self.arg_Bx = (instruction & Inst.MASK_Bx) >> Inst.POS_Bx

        elif self.InstFormat == InstFormat.iAsBx:
            self.arg_A = (instruction & Inst.MASK_A) >> Inst.POS_A
            self.arg_sBx = (instruction & Inst.MASK_sBx) >> Inst.POS_sBx
            # Adjust for signing
            self.arg_sBx -= Inst.K_17_BIT

        elif self.InstFormat == InstFormat.iAx:
            self.arg_Ax = (instruction & Inst.MASK_Ax) >> Inst.POS_Ax

        elif self.InstFormat == InstFormat.isJ:
            self.arg_sJ = (instruction & Inst.MASK_sJ) >> Inst.POS_sJ
            # Adjust for signing
            self.arg_sJ -= Inst.K_25_BIT

    def get_inst_str(self) -> str:
        """
        Create and return the string representation of this instance's 
        opcode and arguments
        """
        if self.InstFormat == InstFormat.iABC:
            line = str(self.opcode).split('.')[1].ljust(self.inst_print_len)

            if self.opmode.has_A == Arg.U or self.opmode.has_A == Arg.S:
                line += "{}".format(self.arg_A)

            if self.opmode.has_B == Arg.U or self.opmode.has_B == Arg.S:
                line += " {}".format(self.arg_B)

            if self.opmode.has_C == Arg.U or self.opmode.has_C == Arg.S:
                line += " {}".format(self.arg_C)

            if self.opmode.has_k == Arg.U:
                line += " {}".format(self.arg_k)

        elif self.InstFormat == InstFormat.iABx:
            line = str(self.opcode).split('.')[1].ljust(self.inst_print_len)
            line += '{}'.format(self.arg_A)
            line += ' {}'.format(self.arg_Bx)

        elif self.InstFormat == InstFormat.iAsBx:
            line = str(self.opcode).split('.')[1].ljust(self.inst_print_len)
            line += '{}'.format(self.arg_A)
            line += ' {}'.format(self.arg_sBx)

        elif self.InstFormat == InstFormat.iAx:
            line = str(self.opcode).split('.')[1].ljust(self.inst_print_len)
            line += '{}'.format(self.arg_A)
            line += ' {}'.format(self.arg_Ax)

        elif self.InstFormat == InstFormat.isJ:
            line = str(self.opcode).split('.')[1].ljust(self.inst_print_len)
            line += '{}'.format(self.arg_sJ)

        return line

