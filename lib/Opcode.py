
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


class Arg(enum.IntEnum):
    '''
    Used to define the arguments B, C, and k uses for specific instructions
    '''
    # Arg not used
    N = 0
    # Arg used - unsigned
    U = 1
    # Arg used - signed
    S = 2


class Opmode():
    '''
    Opmodes for each instruction
    '''
    # Array of Opmodes for each instruction
    def __init__(self, mm, ot, it, t, a, m, has_A, has_B, has_C, has_k):
        # BEGIN unused internal Lua stuff
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
        # END unused internal Lua stuff

        # Op mode (InstFormat)
        self.mode = InstFormat(m)

        # These two instruction formats cannot have an A argument
        if self.mode == InstFormat.iAx or self.mode == InstFormat.isJ:
            if has_A != Arg.N:
                print("INVALID INSTRUCTION! {}".format(self.mode))

        if has_k == Arg.S:
                print("INVALID INSTRUCTION! {}".format(self.mode))

        self.has_A = has_A

        if self.mode == InstFormat.iABC:
            # Whether the instruction uses the B operand
            self.has_B = has_B
            # Whether the instruction uses the C operand
            self.has_C = has_C
            # Whether the instruction uses the k operand
            self.has_k = has_k
        else:
            # Non-iABC formats should not have B, C, or k arguments
            if has_B != Arg.N or has_C != Arg.N or has_k != Arg.N:
                print("INVALID INSTRUCTION! {}".format(self.mode))
            self.has_B = Arg.N
            self.has_C = Arg.N
            self.has_k = Arg.N


class Opmodes():
    ''' 
    Storage class for the opmodes array which contains instruction
    details like instruction format

    Defined in the Opmode class
    '''
    opmodes = [
        #      [internal lua] [            Used by SLAAD             ]
        #      MM OT IT T  A  Mode              A      B      C      k        opcode
        Opmode(0, 0, 0, 0, 1, InstFormat.iABC,  Arg.U, Arg.U, Arg.N, Arg.N),  # MOVE
        Opmode(0, 0, 0, 0, 1, InstFormat.iAsBx, Arg.U, Arg.N, Arg.N, Arg.N),  # LOADI
        Opmode(0, 0, 0, 0, 1, InstFormat.iAsBx, Arg.U, Arg.N, Arg.N, Arg.N),  # LOADF
        Opmode(0, 0, 0, 0, 1, InstFormat.iABx,  Arg.U, Arg.N, Arg.N, Arg.N),  # LOADK
        Opmode(0, 0, 0, 0, 1, InstFormat.iABx,  Arg.U, Arg.N, Arg.N, Arg.N),  # LOADKX
        Opmode(0, 0, 0, 0, 1, InstFormat.iABC,  Arg.U, Arg.N, Arg.N, Arg.N),  # LOADFALSE
        Opmode(0, 0, 0, 0, 1, InstFormat.iABC,  Arg.U, Arg.N, Arg.N, Arg.N),  # LFALSESKIP
        Opmode(0, 0, 0, 0, 1, InstFormat.iABC,  Arg.U, Arg.N, Arg.N, Arg.N),  # LOADTRUE
        Opmode(0, 0, 0, 0, 1, InstFormat.iABC,  Arg.U, Arg.U, Arg.N, Arg.N),  # LOADNIL
        Opmode(0, 0, 0, 0, 1, InstFormat.iABC,  Arg.U, Arg.U, Arg.N, Arg.N),  # GETUPVAL
        Opmode(0, 0, 0, 0, 0, InstFormat.iABC,  Arg.U, Arg.U, Arg.N, Arg.N),  # SETUPVAL
        Opmode(0, 0, 0, 0, 1, InstFormat.iABC,  Arg.U, Arg.U, Arg.U, Arg.N),  # GETTABUP
        Opmode(0, 0, 0, 0, 1, InstFormat.iABC,  Arg.U, Arg.U, Arg.U, Arg.N),  # GETTABLE
        Opmode(0, 0, 0, 0, 1, InstFormat.iABC,  Arg.U, Arg.U, Arg.U, Arg.N),  # GETI
        Opmode(0, 0, 0, 0, 1, InstFormat.iABC,  Arg.U, Arg.U, Arg.U, Arg.N),  # GETFIELD
        Opmode(0, 0, 0, 0, 0, InstFormat.iABC,  Arg.U, Arg.U, Arg.U, Arg.N),  # SETTABUP
        Opmode(0, 0, 0, 0, 0, InstFormat.iABC,  Arg.U, Arg.U, Arg.U, Arg.N),  # SETTABLE
        Opmode(0, 0, 0, 0, 0, InstFormat.iABC,  Arg.U, Arg.U, Arg.U, Arg.N),  # SETI
        Opmode(0, 0, 0, 0, 0, InstFormat.iABC,  Arg.U, Arg.U, Arg.U, Arg.N),  # SETFIELD
        Opmode(0, 0, 0, 0, 1, InstFormat.iABC,  Arg.U, Arg.U, Arg.U, Arg.U),  # NEWTABLE
        Opmode(0, 0, 0, 0, 1, InstFormat.iABC,  Arg.U, Arg.U, Arg.U, Arg.N),  # SELF
        Opmode(0, 0, 0, 0, 1, InstFormat.iABC,  Arg.U, Arg.U, Arg.S, Arg.N),  # ADDI
        Opmode(0, 0, 0, 0, 1, InstFormat.iABC,  Arg.U, Arg.U, Arg.U, Arg.N),  # ADDK
        Opmode(0, 0, 0, 0, 1, InstFormat.iABC,  Arg.U, Arg.U, Arg.U, Arg.N),  # SUBK
        Opmode(0, 0, 0, 0, 1, InstFormat.iABC,  Arg.U, Arg.U, Arg.U, Arg.N),  # MULK
        Opmode(0, 0, 0, 0, 1, InstFormat.iABC,  Arg.U, Arg.U, Arg.U, Arg.N),  # MODK
        Opmode(0, 0, 0, 0, 1, InstFormat.iABC,  Arg.U, Arg.U, Arg.U, Arg.N),  # POWK
        Opmode(0, 0, 0, 0, 1, InstFormat.iABC,  Arg.U, Arg.U, Arg.U, Arg.N),  # DIVK
        Opmode(0, 0, 0, 0, 1, InstFormat.iABC,  Arg.U, Arg.U, Arg.U, Arg.N),  # IDIVK
        Opmode(0, 0, 0, 0, 1, InstFormat.iABC,  Arg.U, Arg.U, Arg.U, Arg.N),  # BANDK
        Opmode(0, 0, 0, 0, 1, InstFormat.iABC,  Arg.U, Arg.U, Arg.U, Arg.N),  # BORK
        Opmode(0, 0, 0, 0, 1, InstFormat.iABC,  Arg.U, Arg.U, Arg.U, Arg.N),  # BXORK
        Opmode(0, 0, 0, 0, 1, InstFormat.iABC,  Arg.U, Arg.U, Arg.S, Arg.N),  # SHRI
        Opmode(0, 0, 0, 0, 1, InstFormat.iABC,  Arg.U, Arg.U, Arg.S, Arg.N),  # SHLI
        Opmode(0, 0, 0, 0, 1, InstFormat.iABC,  Arg.U, Arg.U, Arg.U, Arg.N),  # ADD
        Opmode(0, 0, 0, 0, 1, InstFormat.iABC,  Arg.U, Arg.U, Arg.U, Arg.N),  # SUB
        Opmode(0, 0, 0, 0, 1, InstFormat.iABC,  Arg.U, Arg.U, Arg.U, Arg.N),  # MUL
        Opmode(0, 0, 0, 0, 1, InstFormat.iABC,  Arg.U, Arg.U, Arg.U, Arg.N),  # MOD
        Opmode(0, 0, 0, 0, 1, InstFormat.iABC,  Arg.U, Arg.U, Arg.U, Arg.N),  # POW
        Opmode(0, 0, 0, 0, 1, InstFormat.iABC,  Arg.U, Arg.U, Arg.U, Arg.N),  # DIV
        Opmode(0, 0, 0, 0, 1, InstFormat.iABC,  Arg.U, Arg.U, Arg.U, Arg.N),  # IDIV
        Opmode(0, 0, 0, 0, 1, InstFormat.iABC,  Arg.U, Arg.U, Arg.U, Arg.N),  # BAND
        Opmode(0, 0, 0, 0, 1, InstFormat.iABC,  Arg.U, Arg.U, Arg.U, Arg.N),  # BOR
        Opmode(0, 0, 0, 0, 1, InstFormat.iABC,  Arg.U, Arg.U, Arg.U, Arg.N),  # BXOR
        Opmode(0, 0, 0, 0, 1, InstFormat.iABC,  Arg.U, Arg.U, Arg.U, Arg.N),  # SHL
        Opmode(0, 0, 0, 0, 1, InstFormat.iABC,  Arg.U, Arg.U, Arg.U, Arg.N),  # SHR
        Opmode(1, 0, 0, 0, 0, InstFormat.iABC,  Arg.U, Arg.U, Arg.U, Arg.N),  # MMBIN
        Opmode(1, 0, 0, 0, 0, InstFormat.iABC,  Arg.U, Arg.U, Arg.S, Arg.U),  # MMBINI
        Opmode(1, 0, 0, 0, 0, InstFormat.iABC,  Arg.U, Arg.U, Arg.U, Arg.U),  # MMBINK
        Opmode(0, 0, 0, 0, 1, InstFormat.iABC,  Arg.U, Arg.N, Arg.N, Arg.N),  # UNM
        Opmode(0, 0, 0, 0, 1, InstFormat.iABC,  Arg.U, Arg.U, Arg.N, Arg.N),  # BNOT
        Opmode(0, 0, 0, 0, 1, InstFormat.iABC,  Arg.U, Arg.U, Arg.N, Arg.N),  # NOT
        Opmode(0, 0, 0, 0, 1, InstFormat.iABC,  Arg.U, Arg.U, Arg.N, Arg.N),  # LEN
        Opmode(0, 0, 0, 0, 1, InstFormat.iABC,  Arg.U, Arg.U, Arg.N, Arg.N),  # CONCAT
        Opmode(0, 0, 0, 0, 0, InstFormat.iABC,  Arg.U, Arg.N, Arg.N, Arg.N),  # CLOSE
        Opmode(0, 0, 0, 0, 0, InstFormat.iABC,  Arg.U, Arg.N, Arg.N, Arg.N),  # TBC
        Opmode(0, 0, 0, 0, 0, InstFormat.isJ,   Arg.N, Arg.N, Arg.N, Arg.N),  # JMP
        Opmode(0, 0, 0, 1, 0, InstFormat.iABC,  Arg.U, Arg.U, Arg.N, Arg.U),  # EQ
        Opmode(0, 0, 0, 1, 0, InstFormat.iABC,  Arg.U, Arg.U, Arg.N, Arg.U),  # LT
        Opmode(0, 0, 0, 1, 0, InstFormat.iABC,  Arg.U, Arg.U, Arg.N, Arg.U),  # LE
        Opmode(0, 0, 0, 1, 0, InstFormat.iABC,  Arg.U, Arg.U, Arg.N, Arg.U),  # EQK
        Opmode(0, 0, 0, 1, 0, InstFormat.iABC,  Arg.U, Arg.S, Arg.N, Arg.U),  # EQI
        Opmode(0, 0, 0, 1, 0, InstFormat.iABC,  Arg.U, Arg.S, Arg.N, Arg.U),  # LTI
        Opmode(0, 0, 0, 1, 0, InstFormat.iABC,  Arg.U, Arg.S, Arg.N, Arg.U),  # LEI
        Opmode(0, 0, 0, 1, 0, InstFormat.iABC,  Arg.U, Arg.S, Arg.N, Arg.U),  # GTI
        Opmode(0, 0, 0, 1, 0, InstFormat.iABC,  Arg.U, Arg.S, Arg.N, Arg.U),  # GEI
        Opmode(0, 0, 0, 1, 0, InstFormat.iABC,  Arg.U, Arg.N, Arg.N, Arg.U),  # TEST
        Opmode(0, 0, 0, 1, 1, InstFormat.iABC,  Arg.U, Arg.U, Arg.N, Arg.U),  # TESTSET
        Opmode(0, 1, 1, 0, 1, InstFormat.iABC,  Arg.U, Arg.U, Arg.U, Arg.N),  # CALL
        Opmode(0, 1, 1, 0, 1, InstFormat.iABC,  Arg.U, Arg.U, Arg.U, Arg.U),  # TAILCALL
        Opmode(0, 0, 1, 0, 0, InstFormat.iABC,  Arg.U, Arg.U, Arg.U, Arg.U),  # RETURN
        Opmode(0, 0, 0, 0, 0, InstFormat.iABC,  Arg.U, Arg.N, Arg.N, Arg.N),  # RETURN0
        Opmode(0, 0, 0, 0, 0, InstFormat.iABC,  Arg.U, Arg.N, Arg.N, Arg.N),  # RETURN1
        Opmode(0, 0, 0, 0, 1, InstFormat.iABx,  Arg.U, Arg.N, Arg.N, Arg.N),  # FORLOOP
        Opmode(0, 0, 0, 0, 1, InstFormat.iABx,  Arg.U, Arg.N, Arg.N, Arg.N),  # FORPREP
        Opmode(0, 0, 0, 0, 0, InstFormat.iABx,  Arg.U, Arg.N, Arg.N, Arg.N),  # TFORPREP
        Opmode(0, 0, 0, 0, 0, InstFormat.iABC,  Arg.U, Arg.N, Arg.U, Arg.N),  # TFORCALL
        Opmode(0, 0, 0, 0, 1, InstFormat.iABx,  Arg.U, Arg.N, Arg.N, Arg.N),  # TFORLOOP
        Opmode(0, 0, 1, 0, 0, InstFormat.iABC,  Arg.U, Arg.U, Arg.U, Arg.U),  # SETLIST
        Opmode(0, 0, 0, 0, 1, InstFormat.iABx,  Arg.U, Arg.N, Arg.N, Arg.N),  # CLOSURE
        Opmode(0, 1, 0, 0, 1, InstFormat.iABC,  Arg.U, Arg.N, Arg.U, Arg.N),  # VARARG
        Opmode(0, 0, 1, 0, 1, InstFormat.iABC,  Arg.U, Arg.N, Arg.N, Arg.N),  # VARARGPREP
        Opmode(0, 0, 0, 0, 0, InstFormat.iAx,   Arg.N, Arg.N, Arg.N, Arg.N),  # EXTRAARG
    ]

