import operator as ops

FILES = {
    '100': list(range(1, 20)),
    '200': [],
    '400': []
}

COMMANDS = [
    'COPY',
    'ADDI',
    'SUBI',
    'MULI',
    'DIVI',
    'MODI',
    'TEST',
    'MARK',
    'JUMP',
    'TJMP',
    'FJMP',
    'GRAB',
    'FILE',
    'SEEK',
    'VOID',
    'DROP',

]

REGISTERS = [
    'X',
    'T',
    'F',

]


class EXAError(SyntaxError):
    pass


class State:
    """ Return the state of the EXA registers
    """

    def __init__(self):

        self._registry = {
            register: 0 for register in REGISTERS
        }
        self._labels = {}
        self._next_statement = 0
        self._file_id = ''
        self.EOF = 0

    def __str__(self):
        return f"Registers: T = {self.T:5,} | X = {self.X:5,}"

    def __repr__(self):
        return f"<Registers: T = {self.T:5,} | X = {self.X:5,}>"

    def store(self, register, value):
        self._registry[register] = value

    @property
    def file_id(self):
        return self._registry["file_id"]

    @property
    def T(self):
        return self._registry["T"]

    @property
    def X(self):
        return self._registry["X"]

    def get_value(self, val, line_num):
        if val in self._registry:
            return self._registry[val]
        else:
            val = int(val)
            if not -9999 <= val <= 9999:
                error = f'Integer {val} out of range [-9999, 9999]'
                raise RuntimeError(error)
            return val

    def set_label(self, label, line):
        self._labels[label] = line

    def get_label(self, label):
        return self._labels[label]


class Statement:

    _exp_val = 3

    def __init__(self, data):
        num_of_val = len(data[-1])
        if num_of_val != self._exp_val:
            error = f'Expected {self._exp_val} values, \
got {num_of_val} instead'
            raise RuntimeError(error)

    def __repr__(self):
        return f'<{self.cmd} {" ".join( i for i in self.values)}>'

    def __str__(self):
        return f'{self.cmd} {" ".join( i for i in self.values)}'

    def do(self, state):
        raise NotImplementedError(f'method - {self.do.__name__}')


class MathStatement(Statement):

    def __init__(self, data):
        (
            self.line,
            self.cmd,
            self.values,
        ) = data
        (
            self._a,
            self._b,
            self._to,
        ) = self.values

    def do(self, state):

        a = state.get_value(self._a, self.line)
        b = state.get_value(self._b, self.line)
        state.store(self._to, self.exe(a, b))
        state._next_statement += 1


class ADDI(MathStatement):
    def exe(self, a, b):
        return a + b


class SUBI(MathStatement):
    def exe(self, a, b):
        return a - b


class MULI(MathStatement):
    def exe(self, a, b):
        return a * b


class DIVI(MathStatement):
    def exe(self, a, b):
        return a // b


class MODI(MathStatement):
    def exe(self, a, b):
        return a % b


class COPY(Statement):

    _exp_val = 2

    def __init__(self, data):
        (
            self.line,
            self.cmd,
            self.values,
        ) = data
        (
            self._from,
            self._to,
        ) = self.values

    def do(self, state):
        _from = state.get_value(self._from, self.line)
        state.store(self._to, _from)
        state._next_statement += 1


class EQ:
    def exe(self, a, b):
        return 1 if ops.eq(a, b) else 0


class LT:
    def exe(self, a, b):
        return 1 if ops.lt(a, b) else 0


class GT:
    def exe(self, a, b):
        return 1 if ops.gt(a, b) else 0


class TEST(Statement):
    _exp_val = 3

    OPS = {
        '=': EQ,
        '<': LT,
        '>': GT,
    }

    def __init__(self, data):
        (
            self.line,
            self.cmd,
            self.values,
        ) = data
        (
            self._a,
            self._eval,
            self._b,

        ) = self.values

    def do(self, state):
        a = state.get_value(self._a, self.line)
        b = state.get_value(self._b, self.line)
        for condition, node in self.OPS.items():
            if self._eval == condition:
                val = node().exe(a, b)

        state.store(state.T, val)
        state._next_statement += 1


class MARK(Statement):

    _exp_val = 1

    def __init__(self, data):
        (
            self.line,
            self.cmd,
            self.values,
        ) = data
        self._label = self.values[0]

    def do(self, state):
        state.set_label(self._label, self.line)
        state._next_statement += 1


class JUMP(Statement):

    _exp_val = 1

    def __init__(self, data):
        (
            self.line,
            self.cmd,
            self.values,
        ) = data
        self._label = self.values[-1]

    def do(self, state):
        line = state.get_label(self._label)
        state._next_statement = line


class TJMP(JUMP):
    def do(self, state):
        if state.T:
            super().do(state)
        else:
            state._next_statement += 1


class FJMP(JUMP):
    def do(self, state):
        if not state.T:
            super().do(state)
        else:
            state._next_statement += 1


class FILE(Statement):
    _exp_val = 1

    def __init__(self, data):
        (
            self.line,
            self.cmd,
            self.values,
        ) = data
        self.reg = self.values[0]

    def do(self, state):
        state.store(self.reg, state.file_id)
        state._next_statement += 1


class GRAB(Statement):
    pass


class SEEK(Statement):
    pass


class VOID(Statement):
    pass


class DROP(Statement):
    pass


class Parser:
    """ Parse file and check data"""

    def __init__(self, file):

        self.file = file
        self.code = self.parse()

    def parse(self):
        with open(self.file, 'r') as data:
            return [
                [
                    idx+1,
                    self._check_command(idx+1, line.strip().split()[0]),
                    self._check_register(idx+1, line.strip().split()[1:]),
                ] for idx, line in enumerate(data)
                if line.strip().split()[0] != 'NOTE'
            ]

    def _check_command(self, line, command):
        if command not in COMMANDS:
            error = f"'{command}' in line {line} of {self.file} \
is not a recognized EXA command"
            raise EXAError(error)
        return command

    def _check_register(self, line, vals):
        if len(vals) == 1:
            return vals
        for val in vals:
            if val not in REGISTERS and not val.isdigit() \
                    and val not in TEST.OPS.keys():
                error = f"'{val}' in line {line} of {self.file} \
is not a valid exa register or value"
                raise EXAError(error)
        return vals


class Interpreter:

    _commands = {cmd: eval(cmd) for cmd in COMMANDS}

    def __init__(self, filename):
        self.filename = filename

    def run(self):

        state = State()
        p = Parser(self.filename)

        # Match second param to subclass and pass appropriate 'data' as args.
        program = [self._commands[data[1]](data) for data in p.code]

        lines = len(program)

        while True:
            if state._next_statement == lines:
                break

            stmt = program[state._next_statement]
            stmt.do(state)

        return state
