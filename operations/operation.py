import abc


class Operation(abc.ABC):
    """
    Abstract Base Class to represent an operation following Command Design Pattern
    """

    NAN = float('nan')

    @abc.abstractmethod
    def add_operand(self, operand, tag):
        """
        Allows operands to be added to the given operator
        :param operand: an instance of Operator class that evaluate to a number
        :param tag: extra information on operand interpreted by the subclass
        :return: void
        """