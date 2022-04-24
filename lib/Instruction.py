
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
    POS_Ax  =   POS_A
    POS_sJ  =   POS_A
    
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
        self.InstFormat = self.opmode.mode

        if self.InstFormat == InstFormat.iABC:
            self.arg_A = (instruction & Inst.MASK_A) >> Inst.POS_A
            self.arg_B = (instruction & Inst.MASK_B) >> Inst.POS_B
            self.arg_C = (instruction & Inst.MASK_C) >> Inst.POS_C
            self.arg_k = (instruction & Inst.MASK_k) >> Inst.POS_k
        elif self.InstFormat == InstFormat.iABx:
            self.arg_A = (instruction & Inst.MASK_A) >> Inst.POS_A
            self.arg_Bx = (instruction & Inst.MASK_Bx) >> Inst.POS_Bx
        elif self.InstFormat == InstFormat.iAsBx:
            self.arg_A = (instruction & Inst.MASK_A) >> Inst.POS_A
            self.arg_sBx = (instruction & Inst.MASK_sBx) >> Inst.POS_sBx
        elif self.InstFormat == InstFormat.iAx:
            self.arg_Ax = (instruction & Inst.MASK_Ax) >> Inst.POS_Ax
        elif self.InstFormat == InstFormat.isJ:
            self.arg_sJ = (instruction & Inst.MASK_sJ) >> Inst.POS_sJ

    def get_inst_str(self, show_k=False):
        # TODO full instruction formatting (inst #, upvalue?)
        if self.opcode == Opcode.RETURN0:
            # Edge case, the only opcode with no arguments
            # Don't feel like rewriting Opmodes and Opmode for this
            line = str(self.opcode).split('.')[1].ljust(20)

        elif self.InstFormat == InstFormat.iABC:
            line = str(self.opcode).split('.')[1].ljust(20)
            line += '{}'.format(self.arg_A)

            if self.opmode.has_B == Arg.U:
                line += " {}".format(self.arg_B)
            elif self.opmode.has_B == Arg.S:
                # TODO signed B
                line += " {}".format(self.arg_B)

            if self.opmode.has_C == Arg.U:
                line += " {}".format(self.arg_C)
            elif self.opmode.has_C == Arg.S:
                # TODO signed C
                line += " {}".format(self.arg_C)
            # TODO: Print k?

        elif self.InstFormat == InstFormat.iABx:
            line = str(self.opcode).split('.')[1].ljust(20)
            line += '{}'.format(self.arg_A)
            line += ' {}'.format(self.arg_Bx)

        elif self.InstFormat == InstFormat.iAsBx:
            line = str(self.opcode).split('.')[1].ljust(20)
            line += '{}'.format(self.arg_A)
            line += ' {}'.format(self.arg_sBx)

        elif self.InstFormat == InstFormat.iAx:
            line = str(self.opcode).split('.')[1].ljust(20)
            line += '{}'.format(self.arg_A)
            line += ' {}'.format(self.arg_Ax)

        elif self.InstFormat == InstFormat.isJ:
            line = str(self.opcode).split('.')[1].ljust(20)
            line += '{}'.format(self.arg_A)
            line += ' {}'.format(self.arg_sJ)

        print(line)

