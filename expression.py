
"""
Expression
    Units (unitless)
        Extract units from subexpressions
    Evaluate Expression (Provide partial evaluation)
    Simplify
    Derive Expression
"""

class Expression:
    pass

class Constant_Expression(object):
    def __init__(self, value):
        self.value = value

    def bind(self, values):
        # Ignore values, because this is a constant
        return Constant_Expression(self.value)

    def evaluate(self, values={}):
        return self.value

    def __str__(self):
        return str(self.value)

class Variable_Expression():
    def __init__(self, variable_name):
        self.variable = variable_name

    def bind(self, values):
        if values.get(self.variable):
            return values.get(self.variable)
        else:
            # This creates another node to promote immutability of expressions
            # Currently I want expressions to be completly immutable
            return Variable_Expression(self.variable)

    def evaluate(self, values={}):
        return self.bind(values)

    def __str__(self):
        return str(self.variable)

class Addition_Expression():
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def bind(self, values):
        return Addition_Expression(self.lhs.bind(values),
                                   self.rhs.bind(values)
                                  )

    def evaluate(self, values={}):
        intermediate = self.bind(values)
        if (isinstance(intermediate.lhs, Constant_Expression) and
            isinstance(intermediate.rhs, Constant_Expression)):
                return Constant_Expression(intermediate.lhs.value + intermediate.rhs.value)
        # Otherwise
        return intermediate

    def __str__(self):
        return "({0} + {1})".format(self.lhs, self.rhs)

class Subtraction_Expression():
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def bind(self, values):
        return Subtraction_Expression(self.lhs.bind(values),
                                      self.rhs.bind(values)
                                     )

    def evaluate(self, values={}):
        intermediate = self.bind(values)
        if (isinstance(intermediate.lhs, Constant_Expression) and
            isinstance(intermediate.rhs, Constant_Expression)):
                return Constant_Expression(intermediate.lhs.value - intermediate.rhs.value)
        # Otherwise
        return intermediate

    def __str__(self):
        return "({0} - {1})".format(self.lhs, self.rhs)

class Multiplication_Expression():
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def bind(self, values):
        return Multiplication_Expression(self.lhs.bind(values),
                                         self.rhs.bind(values)
                                        )

    def evaluate(self, values={}):
        intermediate = self.bind(values)
        if (isinstance(intermediate.lhs, Constant_Expression) and
            isinstance(intermediate.rhs, Constant_Expression)):
                return Constant_Expression(intermediate.lhs.value * intermediate.rhs.value)
        # Otherwise
        return intermediate

    def __str__(self):
        return "({0} * {1})".format(self.lhs, self.rhs)

class Division_Expression():
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def bind(self, values):
        return Division_Expression(self.lhs.bind(values),
                                   self.rhs.bind(values)
                                  )

    def evaluate(self, values={}):
        intermediate = self.bind(values)
        if (isinstance(intermediate.lhs, Constant_Expression) and
            isinstance(intermediate.rhs, Constant_Expression)):
                return Constant_Expression(intermediate.lhs.value / intermediate.rhs.value)
        # Otherwise
        return intermediate

    def __str__(self):
        return "({0} / {1})".format(self.lhs, self.rhs)

class Exponent_Expression():
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def bind(self, values):
        return Exponent_Expression(self.lhs.bind(values),
                                   self.rhs.bind(values)
                                  )

    def evaluate(self, values={}):
        intermediate = self.bind(values)
        if (isinstance(intermediate.lhs, Constant_Expression) and
            isinstance(intermediate.rhs, Constant_Expression)):
                return Constant_Expression(pow(intermediate.lhs.value, intermediate.rhs.value))
        # Otherwise
        return intermediate

    def __str__(self):
        return "({0}^{1})".format(self.lhs, self.rhs)
