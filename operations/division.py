from operations.operation import Operation


class Division(Operation):

    TAG = 'division'
    OPERANDS = ('dividend', 'divisor')

    def __init__(self):
        self.dividend = None
        self.divisor = None

    def add_operand(self, operand, tag):
        if not isinstance(operand, Operation):
            raise TypeError("Operand of type Operator is expected")
        if tag not in Division.OPERANDS:
            raise ValueError("Tag value cannot only be one of following: %s")
        if tag == 'dividend':
            self.dividend = operand
        elif tag == 'divisor':
            self.divisor = operand

    def evaluate(self):
        if self.dividend is None or self.divisor is None:
            raise ValueError("Either of dividend or divisor is not set")
        numerator = self.dividend.evaluate()
        denominator = self.divisor.evaluate()
        return numerator // denominator