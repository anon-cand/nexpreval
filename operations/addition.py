from operations.operation import Operation


class Addition(Operation):

    TAG = 'addition'
    OPERANDS = ('item')

    def __init__(self):
        self.items = []

    def __hash__(self):
        """ To optimize calls to evaluation. Assumes consistent evaluation for same internal state """
        return hash(tuple([hash(item) for item in self.items]))

    def __bool__(self):
        """ Returns true if the object is initialized """
        return len(self.items) > 0

    def add_operand(self, operand, tag):
        if not isinstance(operand, Operation):
            raise TypeError("Operand of type Operator is expected")
        if tag not in Addition.OPERANDS:
            raise ValueError("Tag value can only be one of following: %s")
        self.items.append(operand)

    def evaluate(self):
        if len(self.items) == 0:
            raise ValueError("No items have been supplied")
        value = 0
        for item in self.items:
            value += item.evaluate()
        return value

