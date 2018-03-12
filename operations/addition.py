from operations.operation import Operation


class Addition(Operation):
    """
    Representing an operation to perform Addition
    """
    TAG = 'addition'
    __slots__ = 'items'

    def __init__(self):
        self.items = []

    def __hash__(self):
        combined = hash(())
        hashes = (hash(i) for i in self.items)
        for h in hashes:
            combined ^= h
        return combined

    def __call__(self):
        """
        Perform the operation on operands
        :return: a number representing the outcome of operation or NaN
        """
        if len(self.items) > 0:
            return sum(item() for item in self.items)
        return self.NAN

    def add_operand(self, operand, tag):
        """ Add an operand for this operation """
        if not isinstance(operand, Operation):
            raise TypeError("Operand of type Operator is expected")
        if tag not in self.__slots__:
            raise ValueError("Tag value can only be one of following: ", *self.__slots__)
        self.items.append(operand)



