
from .Types import *

class Function():
    """
    Used to track function attributes
    """
    def __init__(self):
        self.num_params = None  # Number of fixed parameters
        self.is_vararg = None
        self.max_stack_size = None  # Registers needed by this function
        self.constants = [] # Constants
        self.line_info = None
        self.line_defined = None
        self.last_line_defined = None
        self.code = []  # opcodes
        self.protos = []  # Functions defined inside this function
        self.upvalues = []  # Upvalue information
        self.local_vars = []  # Local Variables
        self.source = None  # Source name - function name?

    def add_proto(self, new_proto):
        self.proto.append(new_proto)
    
    def add_constant(self, t, v):
        '''
        Add a constant to the list
        :param t: The constant type (see Constant class)
        :param v: The constant value
        '''
        self.constants.append(Constant(t, v))

    def add_upvalue(self, name, instack, idx, kind):
        '''
        Add an upvalue to the list
        :param instack: whether it is in the stack (a register)
        :param idx: index of upvalue (in stack or outer function's list)

        '''
        self.upvalues.append(Upvalue(name, instack, idx, kind))

    def add_proto(self, proto):
        '''
        Add a function to the protos list
        :param proto: The function to be added to the list:
        '''
        self.protos.append(proto)

    def add_abs_line_info(self, pc, line):
        '''
        Add an entry to the abs_line_info list
        :param pc: Instruction address
        :param line: Source file line
        '''
        self.abs_line_info.append(AbsLineInfo(pc, line))

    def add_local_var(self, name, start_pc, end_pc):
        '''
        Add an entry to the local_vars list
        :param name: Variable name
        :param start_pc: start PC
        :param end_pcL end pc
        '''
        self.local_vars.append(LocalVar(name, start_pc, end_pc))

