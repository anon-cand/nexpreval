from operation import Operation


class Addition(Operation):

    KEY = 'addition'

    @property
    def key(cls):
        return Addition.KEY

    def __init__(self):
        self.items = []

    def add_operand(self, operand, _):
        if not isinstance(operand, Operation):
            raise TypeError("Operand of type Operator is expected")
        self.items.append(operand)

    def evaluate(self):
        if len(self.items) == 0:
            raise ValueError("No items have been supplied")
        value = 0
        for item in self.items:
            value += item.evaluate()
        return value

    def __call__(self):
        self.evaluate()
