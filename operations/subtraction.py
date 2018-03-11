from operations.operation import Operation


class Subtraction(Operation):

    TAG = 'subtraction'
    OPERANDS = ('minuend', 'subtrahend')

    def __init__(self):
        self.minuend = None
        self.subtrahend = None

    def __hash__(self):
        """ To optimize calls to evaluation. Assumes consistent evaluation for same internal state """
        return hash(tuple([hash(x) for x in (self.minuend, self.subtrahend)]))

    def __bool__(self):
        """ Returns true if the object is initialized """
        return self.minuend is not None and self.subtrahend is not None

    def add_operand(self, operand, tag):
        if not isinstance(operand, Operation):
            raise TypeError("Operand of type Operator is expected")
        if tag not in Subtraction.OPERANDS:
            raise ValueError("Tag value cannot only be one of following: %s")
        if tag == 'minuend':
            self.minuend = operand
        elif tag == 'subtrahend':
            self.subtrahend = operand

    def evaluate(self):
        if self.minuend is None or self.subtrahend is None:
            raise ValueError("Either of minuend or subtrahend is not set")
        m = self.minuend.evaluate()
        s = self.subtrahend.evaluate()
        return m - s