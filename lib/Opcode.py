
import enum


class InstFormat(enum.Enum):
    '''
    The 5 instruction formats available in Lua 5.4.4
    '''
    iABC  = 1
    iABx  = 2
    iAsBx = 3
    iAx   = 4
    isJ   = 5


class Opmode():
    '''
    Opmodes for each instruction
    '''
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
        self.m = m


class Opcode(enum.Enum):
    '''
    All Lua 5.4.4 opcodes
    '''
    MOVE         = 1
    LOADI        = 2
    LOADF        = 3
    LOADK        = 4
    LOADKX       = 5
    LOADFALSE    = 6
    LFALSESKIP   = 7
    LOADTRUE     = 8
    LOADNIL      = 9
    GETUPVAL     = 10
    SETUPVAL     = 11
    GETTABUP     = 12
    GETTABLE     = 13
    GETI         = 14
    GETFIELD     = 15
    SETTABUP     = 16
    SETTABLE     = 17
    SETI         = 18
    SETFIELD     = 19
    NEWTABLE     = 20
    SELF         = 21
    ADDI         = 22
    ADDK         = 23
    SUBK         = 24
    MULK         = 25
    MODK         = 26
    POWK         = 27
    DIVK         = 28
    IDIVK        = 29
    BANDK        = 30
    BORK         = 31
    BXORK        = 32
    SHRI         = 33
    SHLI         = 34
    ADD          = 35
    SUB          = 36
    MUL          = 37
    MOD          = 38
    POW          = 39
    DIV          = 40
    IDIV         = 41
    BAND         = 42
    BOR          = 43
    BXOR         = 44
    SHL          = 45
    SHR          = 46
    MMBIN        = 47
    MMBINI       = 48
    MMBINK       = 49
    UNM          = 50
    BNOT         = 51
    NOT          = 52
    LEN          = 53
    CONCAT       = 54
    CLOSE        = 55
    TBC          = 56
    JMP          = 57
    EQ           = 58
    LT           = 59
    LE           = 60
    EQK          = 61
    EQI          = 62
    LTI          = 63
    LEI          = 64
    GTI          = 65
    GEI          = 66
    TEST         = 67
    TESTSET      = 68
    CALL         = 69
    TAILCALL     = 70
    RETURN       = 71
    RETURN0      = 72
    RETURN1      = 73
    FORLOOP      = 74
    FORPREP      = 75
    TFORPREP     = 76
    TFORCALL     = 77
    TFORLOOP     = 78
    SETLIST      = 79
    CLOSURE      = 80
    VARARG       = 81
    VARARGPREP   = 82
    EXTRAARG     = 83

    # Array of Opmodes for each instruction
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



