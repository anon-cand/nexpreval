import abc


class Operation(abc.ABC):

    TAG = "operation"

    @abc.abstractmethod
    def add_operand(self, operand, tag):
        """
        Allows operands to be added to the given operator
        :param operand: an instance of Operator class that evaluate to a number
        :param tag: extra information on operand interpreted by the subclass
        :return: void
        """

    @abc.abstractmethod
    def evaluate(self):
        """
        A subclass applies its algorithm over its operators
        :return: a number
        """
