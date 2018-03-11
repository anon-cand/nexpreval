from operations.operation import Operation


class Multiplication(Operation):

    TAG = 'multiplication'
    OPERANDS = ('factor')

    def __init__(self):
        self.factors = []

    def add_operand(self, operand, tag):
        if not isinstance(operand, Operation):
            raise TypeError("Operand of type Operator is expected")
        if tag not in Multiplication.OPERANDS:
            raise ValueError("Tag value can only be one of following: %s")
        self.factors.append(operand)
        return True

    def evaluate(self):
        if len(self.factors) == 0:
            raise ValueError("No factors has been supplied")
        value = 1
        for factor in self.factors:
            value *= factor.evaluate()
        return value

