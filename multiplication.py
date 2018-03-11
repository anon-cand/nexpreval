from operation import Operation


class Multiplication(Operation):

    KEY = 'multiplication'

    @property
    def key(cls):
        return Multiplication.KEY

    def __init__(self):
        self.factors = []

    def add_operand(self, operand, _):
        if not isinstance(operand, Operation):
            raise TypeError("Operand of type Operator is expected")
        self.factors.append(operand)
        return True

    def evaluate(self):
        if len(self.factors) == 0:
            raise ValueError("No factors has been supplied")
        value = 1
        for factor in self.factors:
            value *= factor.evaluate()
        return value

    def __call__(self):
        self.evaluate()
