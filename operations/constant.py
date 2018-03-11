from operations.operation import Operation


class Constant(Operation):

    TAG = 'default'

    def __init__(self):
        self.value = None

    def __hash__(self):
        """ To optimize calls to evaluation. Assumes consistent evaluation for same internal state """
        return hash(self.value)

    def __bool__(self):
        """ Returns true if the object is initialized """
        return self.value and isinstance(self.value, (int, float))

    def add_operand(self, operand, _):
        try:
            int(operand)
        except ValueError:
            raise TypeError("Operand of type int is expected")
        self.value = int(operand)

    def evaluate(self):
        return self.value if self else self.NAN
