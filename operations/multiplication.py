from operations.operation import Operation
from functools import reduce

class Multiplication(Operation):

    TAG = 'multiplication'
    OPERANDS = ('factor')

    def __init__(self):
        self.factors = []

    def __hash__(self):
        """ To optimize calls to evaluation. Assumes consistent evaluation for same internal state """
        return hash(tuple([hash(factor) for factor in self.factors]))

    def __bool__(self):
        """ Returns true if the object is initialized """
        return len(self.factors) > 0 and all(self.factors)

    def add_operand(self, operand, tag):
        if not isinstance(operand, Operation):
            raise TypeError("Operand of type Operator is expected")
        if tag not in Multiplication.OPERANDS:
            raise ValueError("Tag value can only be one of following: %s")
        self.factors.append(operand)
        return True

    def evaluate(self):
        if self:
            value = 1
            for f in self.factors:
                value *= f.evaluate()
            return value
        return self.NAN
