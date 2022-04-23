

class Function():
    """
    Used to track function attributes
    """
    def __init__(self):
        self.num_params = None  # Number of fixed parameters
        self.is_vararg = None
        self.max_stack_size = None  # Registers needed by this function
        self.size_upvalues = None  # size of upvalues
        self.size_k = None  # size of 'k'
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

