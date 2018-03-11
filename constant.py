from operation import Operation


class Constant(Operation):

    KEY = 'constant'

    @property
    def key(cls):
        return Constant.KEY

    def __init__(self):
        self.value = None

    def add_operand(self, operand, _):
        self.value = int(operand)

    def evaluate(self):
        if self.value is None:
            raise ValueError("Value of this constant is not set")
        return self.value

    def __call__(self):
        self.evaluate()