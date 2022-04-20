
from .Opcode import Opcode

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
    MASK_K  = 0b00000000000000001000000000000000
    MASK_B  = 0b00000000111111110000000000000000
    MASK_C  = 0b11111111000000000000000000000000
    MASK_sBx= 0b11111111111111111000000000000000
    MASK_Ax = 0b11111111111111111111111110000000
    MASK_sJ = 0b11111111111111111111111110000000

    def __init__(self):
        print(Inst.MASK_OP)


