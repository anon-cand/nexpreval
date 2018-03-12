from operations.operation import Operation


class Multiplication(Operation):

    TAG = 'multiplication'
    __slots__ = 'factors'

    def __init__(self):
        self.factors = []

    def __hash__(self):
        hashes = (hash(factor) for factor in self.factors)
        combined = hash(())
        for h in hashes:
            combined ^= h
        return combined

    def __call__(self):
        """
        Perform the operation on operands
        :return: a number representing the outcome of operation or NaN
        """
        if len(self.factors) > 0:
            value = 1
            for factor in self.factors:
                value *= factor()
            return value
        return self.NAN

    def add_operand(self, operand, tag):
        """ Add an operand for this operation """
        if not isinstance(operand, Operation):
            raise TypeError("Operand of type Operator is expected")
        if tag not in self.__slots__:
            raise ValueError("Tag value can only be one of following: ", *self.__slots__)
        self.factors.append(operand)
        return True

