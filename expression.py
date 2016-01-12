
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
        return self.bind(values)

    def derive(self, respect_to):
        return Constant_Expression(0)

    def __str__(self):
        return str(self.value)

class Variable_Expression(object):
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
        return self.bind(values) # TODO Circular evaluation when bind creates variables

    def derive(self, respect_to):
        if self.variable == respect_to:
            return Constant_Expression(1)
        else:
            return Constant_Expression(0)

    def __str__(self):
        return str(self.variable)

class Addition_Expression(object):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def bind(self, values):
        return Addition_Expression(self.lhs.bind(values),
                                   self.rhs.bind(values)
                                  )

    def evaluate(self, values={}):
        intermediate = self.bind(values)
        intermediate = Addition_Expression(
                            intermediate.lhs.evaluate(values),
                            intermediate.rhs.evaluate(values)
                        )
        # TODO Is there a better way
        # TODO Ordered list of constraints of conditions and transformations applied on said conditions
        if (isinstance(intermediate.lhs, Constant_Expression) and intermediate.lhs.value == 0):
                return intermediate.rhs
        elif (isinstance(intermediate.rhs, Constant_Expression) and intermediate.rhs.value == 0):
                return intermediate.lhs
        elif (isinstance(intermediate.lhs, Constant_Expression) and
            isinstance(intermediate.rhs, Constant_Expression)):
                return Constant_Expression(intermediate.lhs.value + intermediate.rhs.value)
        # Otherwise
        return intermediate

    def derive(self, respect_to):
        return Addition_Expression(
                    self.lhs.derive(respect_to),
                    self.rhs.derive(respect_to)
                )

    def __str__(self):
        return "({0} + {1})".format(self.lhs, self.rhs)

class Subtraction_Expression(object):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def bind(self, values):
        return Subtraction_Expression(self.lhs.bind(values),
                                      self.rhs.bind(values)
                                     )

    def evaluate(self, values={}):
        intermediate = self.bind(values)
        intermediate = Subtraction_Expression(
                            intermediate.lhs.evaluate(values),
                            intermediate.rhs.evaluate(values)
                        )
        # TODO Is there really not a better way of doing this
        if (isinstance(intermediate.rhs, Constant_Expression) and intermediate.rhs.value == 0):
                return intermediate.lhs
        elif (isinstance(intermediate.lhs, Constant_Expression) and
              isinstance(intermediate.rhs, Constant_Expression)):
                return Constant_Expression(intermediate.lhs.value - intermediate.rhs.value)
        # Otherwise
        return intermediate

    def derive(self, respect_to):
        return Subtraction_Expression(
                    self.lhs.derive(respect_to),
                    self.rhs.derive(respect_to)
                )

    def __str__(self):
        return "({0} - {1})".format(self.lhs, self.rhs)

class Multiplication_Expression(object):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def bind(self, values):
        return Multiplication_Expression(self.lhs.bind(values),
                                         self.rhs.bind(values)
                                        )

    def evaluate(self, values={}):
        intermediate = self.bind(values)
        intermediate = Multiplication_Expression(
                            intermediate.lhs.evaluate(values),
                            intermediate.rhs.evaluate(values)
                        )
        # TODO Is there really not a better way of doing this
        if (isinstance(intermediate.lhs, Constant_Expression) and intermediate.lhs.value == 1):
                return intermediate.rhs
        elif (isinstance(intermediate.rhs, Constant_Expression) and intermediate.rhs.value == 1):
                return intermediate.lhs
        elif ((isinstance(intermediate.lhs, Constant_Expression) and intermediate.lhs.value == 0) or
            (isinstance(intermediate.rhs, Constant_Expression) and intermediate.rhs.value == 0)):
                return Constant_Expression(0)
        elif (isinstance(intermediate.lhs, Constant_Expression) and
            isinstance(intermediate.rhs, Constant_Expression)):
                return Constant_Expression(intermediate.lhs.value * intermediate.rhs.value)
        # Otherwise
        return intermediate

    def derive(self, respect_to):
        return Addition_Expression(
                    Multiplication_Expression(
                        self.lhs.derive(respect_to),
                        self.rhs
                    ),
                    Multiplication_Expression(
                        self.lhs,
                        self.rhs.derive(respect_to)
                    )
                )

    def __str__(self):
        return "({0} * {1})".format(self.lhs, self.rhs)

class Division_Expression(object):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def bind(self, values):
        return Division_Expression(self.lhs.bind(values),
                                   self.rhs.bind(values)
                                  )

    def evaluate(self, values={}):
        intermediate = self.bind(values)
        intermediate = Division_Expression(
                            intermediate.lhs.evaluate(values),
                            intermediate.rhs.evaluate(values)
                        )
        if (isinstance(intermediate.lhs, Constant_Expression) and
            isinstance(intermediate.rhs, Constant_Expression)):
                return Constant_Expression(intermediate.lhs.value / intermediate.rhs.value)
        # Otherwise
        return intermediate

    def derive(self, respect_to):
        return Division_Expression(
                    Subtraction_Expression(
                        Multiplication_Expression(
                            self.lhs.derive(respect_to),
                            self.rhs
                        ),
                        Multiplication_Expression(
                            self.lhs,
                            self.rhs.derive(respect_to)
                        )
                    ),
                    Exponent_Expression(
                        self.rhs,
                        Constant_Expression(2)
                    )
                )

    def __str__(self):
        return "({0} / {1})".format(self.lhs, self.rhs)

class Exponent_Expression(object):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def bind(self, values):
        return Exponent_Expression(self.lhs.bind(values),
                                   self.rhs.bind(values)
                                  )

    def evaluate(self, values={}):
        intermediate = self.bind(values)
        intermediate = Exponent_Expression(
                            intermediate.lhs.evaluate(values),
                            intermediate.rhs.evaluate(values)
                        )
        if (isinstance(intermediate.lhs, Constant_Expression) and
            isinstance(intermediate.rhs, Constant_Expression)):
                return Constant_Expression(pow(intermediate.lhs.value, intermediate.rhs.value))
        # Otherwise
        return intermediate

    def derive(self, respect_to):
        # TODO
        raise Exception('Not Implemented')

    def __str__(self):
        return "({0}^{1})".format(self.lhs, self.rhs)
