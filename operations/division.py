import numbers
from operations.operation import Operation


class Division(Operation):
    """
    Representing an operation to perform Division
    """
    TAG = 'division'
    __slots__ = ('dividend', 'divisor')

    def __init__(self):
        self.divisor = None
        self.dividend = None

    def __hash__(self):
        return hash(self.dividend) ^ hash(self.divisor)

    def __call__(self):
        """
        Perform the operation on operands
        :return: a number representing the outcome of operation or NaN
        """
        if self.dividend is not None and self.divisor is not None:
            return self.dividend() // self.divisor()
        return self.NAN

    def add_operand(self, operand, tag):
        if not isinstance(operand, Operation):
            raise TypeError("Operand of type Operator is expected")
        if tag not in self.__slots__:
            raise ValueError("Tag value cannot only be one of following: ", *self.__slots__)
        if tag == 'dividend':
            self.dividend = operand
        elif tag == 'divisor':
            self.divisor = operand
