
import enum


class Opcode(enum.IntEnum):
    '''
    All Lua 5.4.4 opcodes
    '''
    MOVE         = 0
    LOADI        = 1
    LOADF        = 2
    LOADK        = 3
    LOADKX       = 4
    LOADFALSE    = 5
    LFALSESKIP   = 6
    LOADTRUE     = 7
    LOADNIL      = 8
    GETUPVAL     = 9
    SETUPVAL     = 10
    GETTABUP     = 11
    GETTABLE     = 12
    GETI         = 13
    GETFIELD     = 14
    SETTABUP     = 15
    SETTABLE     = 16
    SETI         = 17
    SETFIELD     = 18
    NEWTABLE     = 19
    SELF         = 20
    ADDI         = 21
    ADDK         = 22
    SUBK         = 23
    MULK         = 24
    MODK         = 25
    POWK         = 26
    DIVK         = 27
    IDIVK        = 28
    BANDK        = 29
    BORK         = 30
    BXORK        = 31
    SHRI         = 32
    SHLI         = 33
    ADD          = 34
    SUB          = 35
    MUL          = 36
    MOD          = 37
    POW          = 38
    DIV          = 39
    IDIV         = 40
    BAND         = 41
    BOR          = 42
    BXOR         = 43
    SHL          = 44
    SHR          = 45
    MMBIN        = 46
    MMBINI       = 47
    MMBINK       = 48
    UNM          = 49
    BNOT         = 50
    NOT          = 51
    LEN          = 52
    CONCAT       = 53
    CLOSE        = 54
    TBC          = 55
    JMP          = 56
    EQ           = 57
    LT           = 58
    LE           = 59
    EQK          = 60
    EQI          = 61
    LTI          = 62
    LEI          = 63
    GTI          = 64
    GEI          = 65
    TEST         = 66
    TESTSET      = 67
    CALL         = 68
    TAILCALL     = 69
    RETURN       = 70
    RETURN0      = 71
    RETURN1      = 72
    FORLOOP      = 73
    FORPREP      = 74
    TFORPREP     = 75
    TFORCALL     = 76
    TFORLOOP     = 77
    SETLIST      = 78
    CLOSURE      = 79
    VARARG       = 80
    VARARGPREP   = 81
    EXTRAARG     = 82


class InstFormat(enum.IntEnum):
    '''
    The 5 instruction formats available in Lua 5.4.4
    '''
    iABC  = 0
    iABx  = 1
    iAsBx = 2
    iAx   = 3
    isJ   = 4


class Opmode():
    '''
    Opmodes for each instruction
    '''
    # Array of Opmodes for each instruction
    def __init__(self, mm, ot, it, t, a, m):
        # Whether an instruction calls a metainstruction
        self.mm = mm
        # Instruction sets 'L->top' for next instruction (when C == 0)
        self.ot = ot
        # Instruction uses 'L->top' set by previous instruction (when B == 0)
        self.it = it
        # Operator is a test (next instruction must be a jump)
        self.t = t
        # Instruction set register A
        self.a = a
        # Op mode (InstFormat)
        self.mode = InstFormat(m)

    def get_format(self):
        return self.mode


class Opmodes():
    ''' 
    Storage class for the opmodes array which contains instruction
    details like instruction format
    '''
    opmodes = [
        #      MM OT IT T  A  Mode                 opcode
        Opmode(0, 0, 0, 0, 1, InstFormat.iABC),  # MOVE
        Opmode(0, 0, 0, 0, 1, InstFormat.iAsBx), # LOADI
        Opmode(0, 0, 0, 0, 1, InstFormat.iAsBx), # LOADF
        Opmode(0, 0, 0, 0, 1, InstFormat.iABx),  # LOADK
        Opmode(0, 0, 0, 0, 1, InstFormat.iABx),  # LOADKX
        Opmode(0, 0, 0, 0, 1, InstFormat.iABC),  # LOADFALSE
        Opmode(0, 0, 0, 0, 1, InstFormat.iABC),  # LFALSESKIP
        Opmode(0, 0, 0, 0, 1, InstFormat.iABC),  # LOADTRUE
        Opmode(0, 0, 0, 0, 1, InstFormat.iABC),  # LOADNIL
        Opmode(0, 0, 0, 0, 1, InstFormat.iABC),  # GETUPVAL
        Opmode(0, 0, 0, 0, 0, InstFormat.iABC),  # SETUPVAL
        Opmode(0, 0, 0, 0, 1, InstFormat.iABC),  # GETTABUP
        Opmode(0, 0, 0, 0, 1, InstFormat.iABC),  # GETTABLE
        Opmode(0, 0, 0, 0, 1, InstFormat.iABC),  # GETI
        Opmode(0, 0, 0, 0, 1, InstFormat.iABC),  # GETFIELD
        Opmode(0, 0, 0, 0, 0, InstFormat.iABC),  # SETTABUP
        Opmode(0, 0, 0, 0, 0, InstFormat.iABC),  # SETTABLE
        Opmode(0, 0, 0, 0, 0, InstFormat.iABC),  # SETI
        Opmode(0, 0, 0, 0, 0, InstFormat.iABC),  # SETFIELD
        Opmode(0, 0, 0, 0, 1, InstFormat.iABC),  # NEWTABLE
        Opmode(0, 0, 0, 0, 1, InstFormat.iABC),  # SELF
        Opmode(0, 0, 0, 0, 1, InstFormat.iABC),  # ADDI
        Opmode(0, 0, 0, 0, 1, InstFormat.iABC),  # ADDK
        Opmode(0, 0, 0, 0, 1, InstFormat.iABC),  # SUBK
        Opmode(0, 0, 0, 0, 1, InstFormat.iABC),  # MULK
        Opmode(0, 0, 0, 0, 1, InstFormat.iABC),  # MODK
        Opmode(0, 0, 0, 0, 1, InstFormat.iABC),  # POWK
        Opmode(0, 0, 0, 0, 1, InstFormat.iABC),  # DIVK
        Opmode(0, 0, 0, 0, 1, InstFormat.iABC),  # IDIVK
        Opmode(0, 0, 0, 0, 1, InstFormat.iABC),  # BANDK
        Opmode(0, 0, 0, 0, 1, InstFormat.iABC),  # BORK
        Opmode(0, 0, 0, 0, 1, InstFormat.iABC),  # BXORK
        Opmode(0, 0, 0, 0, 1, InstFormat.iABC),  # SHRI
        Opmode(0, 0, 0, 0, 1, InstFormat.iABC),  # SHLI
        Opmode(0, 0, 0, 0, 1, InstFormat.iABC),  # ADD
        Opmode(0, 0, 0, 0, 1, InstFormat.iABC),  # SUB
        Opmode(0, 0, 0, 0, 1, InstFormat.iABC),  # MUL
        Opmode(0, 0, 0, 0, 1, InstFormat.iABC),  # MOD
        Opmode(0, 0, 0, 0, 1, InstFormat.iABC),  # POW
        Opmode(0, 0, 0, 0, 1, InstFormat.iABC),  # DIV
        Opmode(0, 0, 0, 0, 1, InstFormat.iABC),  # IDIV
        Opmode(0, 0, 0, 0, 1, InstFormat.iABC),  # BAND
        Opmode(0, 0, 0, 0, 1, InstFormat.iABC),  # BOR
        Opmode(0, 0, 0, 0, 1, InstFormat.iABC),  # BXOR
        Opmode(0, 0, 0, 0, 1, InstFormat.iABC),  # SHL
        Opmode(0, 0, 0, 0, 1, InstFormat.iABC),  # SHR
        Opmode(1, 0, 0, 0, 0, InstFormat.iABC),  # MMBIN
        Opmode(1, 0, 0, 0, 0, InstFormat.iABC),  # MMBINI
        Opmode(1, 0, 0, 0, 0, InstFormat.iABC),  # MMBINK
        Opmode(0, 0, 0, 0, 1, InstFormat.iABC),  # UNM
        Opmode(0, 0, 0, 0, 1, InstFormat.iABC),  # BNOT
        Opmode(0, 0, 0, 0, 1, InstFormat.iABC),  # NOT
        Opmode(0, 0, 0, 0, 1, InstFormat.iABC),  # LEN
        Opmode(0, 0, 0, 0, 1, InstFormat.iABC),  # CONCAT
        Opmode(0, 0, 0, 0, 0, InstFormat.iABC),  # CLOSE
        Opmode(0, 0, 0, 0, 0, InstFormat.iABC),  # TBC
        Opmode(0, 0, 0, 0, 0, InstFormat.isJ),   # JMP
        Opmode(0, 0, 0, 1, 0, InstFormat.iABC),  # EQ
        Opmode(0, 0, 0, 1, 0, InstFormat.iABC),  # LT
        Opmode(0, 0, 0, 1, 0, InstFormat.iABC),  # LE
        Opmode(0, 0, 0, 1, 0, InstFormat.iABC),  # EQK
        Opmode(0, 0, 0, 1, 0, InstFormat.iABC),  # EQI
        Opmode(0, 0, 0, 1, 0, InstFormat.iABC),  # LTI
        Opmode(0, 0, 0, 1, 0, InstFormat.iABC),  # LEI
        Opmode(0, 0, 0, 1, 0, InstFormat.iABC),  # GTI
        Opmode(0, 0, 0, 1, 0, InstFormat.iABC),  # GEI
        Opmode(0, 0, 0, 1, 0, InstFormat.iABC),  # TEST
        Opmode(0, 0, 0, 1, 1, InstFormat.iABC),  # TESTSET
        Opmode(0, 1, 1, 0, 1, InstFormat.iABC),  # CALL
        Opmode(0, 1, 1, 0, 1, InstFormat.iABC),  # TAILCALL
        Opmode(0, 0, 1, 0, 0, InstFormat.iABC),  # RETURN
        Opmode(0, 0, 0, 0, 0, InstFormat.iABC),  # RETURN0
        Opmode(0, 0, 0, 0, 0, InstFormat.iABC),  # RETURN1
        Opmode(0, 0, 0, 0, 1, InstFormat.iABx),  # FORLOOP
        Opmode(0, 0, 0, 0, 1, InstFormat.iABx),  # FORPREP
        Opmode(0, 0, 0, 0, 0, InstFormat.iABx),  # TFORPREP
        Opmode(0, 0, 0, 0, 0, InstFormat.iABC),  # TFORCALL
        Opmode(0, 0, 0, 0, 1, InstFormat.iABx),  # TFORLOOP
        Opmode(0, 0, 1, 0, 0, InstFormat.iABC),  # SETLIST
        Opmode(0, 0, 0, 0, 1, InstFormat.iABx),  # CLOSURE
        Opmode(0, 1, 0, 0, 1, InstFormat.iABC),  # VARARG
        Opmode(0, 0, 1, 0, 1, InstFormat.iABC),  # VARARGPREP
        Opmode(0, 0, 0, 0, 0, InstFormat.iAx),   # EXTRAARG
    ]

