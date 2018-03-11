from operation import Operation


class Division(Operation):

    KEY = 'division'
    TAG = ('dividend', 'divisor')

    @property
    def key(cls):
        return Division.KEY

    def __init__(self):
        self.dividend = None
        self.divisor = None

    def add_operand(self, operand, tag):
        if not isinstance(operand, Operation):
            raise TypeError("Operand of type Operator is expected")
        if tag not in Division.TAG:
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

    def __call__(self):
        self.evaluate()