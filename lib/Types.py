
import enum


class Type(enum.IntEnum):
    '''
    Basic types, from lua.h
    '''
    TNIL            = 0
    TBOOLEAN        = 1
    TLIGHTUSERDATA  = 2
    TNUMBER         = 3
    TSTRING         = 4
    TTABLE          = 5
    TFUNCTION       = 6
    TUSERDATA       = 7
    TTHREAD         = 8


class Variant(enum.IntEnum):
    '''
    bits 0-3: actual tag (a LUA_T* constant)
    bits 4-5: variant bits
    bit 6: whether value is collectable
    '''
    def _make_variant(t, v):
        return (t | ((v) << 4))

    VNIL = _make_variant(Type.TNIL, 0)
    VFALSE = _make_variant(Type.TBOOLEAN, 0)
    VTRUE = _make_variant(Type.TBOOLEAN, 1)
    VNUMINT = _make_variant(Type.TNUMBER, 0)
    VNUMFLT = _make_variant(Type.TNUMBER, 1)
    VSHRSTR = _make_variant(Type.TSTRING, 0)
    VLNGSTR = _make_variant(Type.TSTRING, 1)


class Upvalue():
    '''
    Defines an upvalue, similar to a C static variable
    '''
    def __init__(self, instack, idx, kind):
        '''
        :param instack: whether it is in the stack (a register)
        :param idx: index of upvalue (in stack or outer function's list)
        :param kind: kind (type?) of corresponding variable
        '''
        self.instack = instack
        self.idx = idx
        self.kind = kind

