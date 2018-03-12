from operations.operation import Operation


class Subtraction(Operation):
    """
    Representing an operation to perform Subtraction
    """
    TAG = 'subtraction'
    __slots__ = ('minuend', 'subtrahend')

    def __init__(self):
        self.minuend = None
        self.subtrahend = None

    def __hash__(self):
        return hash(self.minuend) ^ hash(self.subtrahend)

    def __call__(self):
        """
        Perform the operation on operands
        :return: a number representing the outcome of operation or NaN
        """
        if self.minuend is not None and self.subtrahend is not None:
            return self.minuend() - self.subtrahend()
        return self.NAN

    def add_operand(self, operand, tag):
        """ Add an operand for this operation """
        if not isinstance(operand, Operation):
            raise TypeError("Operand of type Operator is expected")
        if tag not in self.__slots__:
            raise ValueError("Tag value cannot only be one of following: ", *self.__slots__)
        if tag == 'minuend':
            self.minuend = operand
        elif tag == 'subtrahend':
            self.subtrahend = operand

