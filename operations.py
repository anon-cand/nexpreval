
class Operations:

    def add_operand(self, operand, tag):
        raise NotImplementedError

    def evaluate(self):
        raise NotImplementedError


class Constant(Operations):

    def __init__(self):
        self.value = NotImplemented

    def __str__(self):
        return 'constant'

    def add_operand(self, operand, tag):
        self.value = int(operand)

    def evaluate(self):
        return self.value


class Addition(Operations):

    def __init__(self):
        self.items = []

    def __str__(self):
        return 'addition'

    def add_operand(self, operand, tag):
        self.items.append(operand)

    def evaluate(self):
        value = 0
        for item in self.items:
            value += item.evaluate()
        return value


class Subtraction(Operations):

    def __init__(self):
        self.minuend = Operations()
        self.subtrahend = Operations()

    def __str__(self):
        return 'subtraction'

    def add_operand(self, operand, tag):
        if tag == 'minuend':
            self.minuend = operand
        elif tag == 'subtrahend':
            self.subtrahend = operand
        else:
            raise NotImplementedError

    def evaluate(self):
        m = self.minuend.evaluate()
        s = self.subtrahend.evaluate()
        return m - s

class Multiplication(Operations):

    def __init__(self):
        self.factors = []

    def __str__(self):
        return 'multiplication'

    def add_operand(self, operand, tag):
        self.factors.append(operand)

    def evaluate(self):
        value = 1
        for factor in self.factors:
            value *= factor.evaluate()
        return value


class Division(Operations):

    def __init__(self):
        self.dividend = Operations()
        self.divisor = Operations()

    def __str__(self):
        return 'division'

    def add_operand(self, operand, tag):
        if tag == 'dividend':
            self.dividend = operand
        elif tag == 'divisor':
            self.divisor = operand
        else:
            raise NotImplementedError

    def evaluate(self):
        numerator = self.dividend.evaluate()
        denominator = self.divisor.evaluate()
        return numerator // denominator

