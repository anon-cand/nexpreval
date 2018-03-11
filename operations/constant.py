from operations.operation import Operation


class Constant(Operation):

    TAG = 'constant'

    def __init__(self):
        self.value = None

    def add_operand(self, operand, _):
        self.value = int(operand)

    def evaluate(self):
        if self.value is None:
            raise ValueError("Value of this constant is not set")
        return self.value
