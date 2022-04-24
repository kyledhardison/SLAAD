
from .Types import Variant

class Function():
    """
    Used to track function attributes
    """
    def __init__(self):
        self.num_params = None  # Number of fixed parameters
        self.is_vararg = None
        self.max_stack_size = None  # Registers needed by this function
        self.size_upvalues = None  # size of upvalues
        self.size_constants = None  # size of constants, maybe unneeded
        self.constants = [] # Constants
        self.size_code = None
        self.size_line_info = None
        self.line_defined = None
        self.last_line_defined = None
        self.code = []  # opcodes
        self.proto = []  # Functions defined inside this function
        self.upvalues = None  # Upvalue information
        self.source = None  # Source name - function name?

    def add_proto(self, new_proto):
        self.proto.append(new_proto)
    
    def add_constant(self, t, v):
        '''
        Add a constant to the list

        :param t: The constant type (see Variant class)
        :param v: The constant value
        '''
        if t not in Variant:
            # TODO error handling
            print("INVALID CONSTANT TYPE")
        self.constants.append({
            'type': t,
            'value': v})

