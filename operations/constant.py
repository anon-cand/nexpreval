from operations.operation import Operation


class Constant(Operation):
    """
    Class to represent a constant
    """
    TAG = 'default'
    __slots__ = 'value'

    def __init__(self, value = None):
        self.value = value

    def __hash__(self):
        return hash(self.value)

    def __call__(self):
        """
        Verify and return the constant stored within the object
        :return: value of this object
        """
        if self.value and isinstance(self.value, (int, float)):
            return self.value
        return self.NAN

    def add_operand(self, operand, _):
        """ Add an operand for this operation """
        try:
            int(operand)
        except ValueError:
            raise TypeError("Operand of type int is expected")
        self.value = int(operand)

