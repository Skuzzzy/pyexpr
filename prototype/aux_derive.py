from parse import construct_binary_ast_node, label
import derivative

def derive_mult(expression, respect_to):
    # U dv + V du
    return construct_binary_ast_node(
                label('+'),
                construct_binary_ast_node(
                    label('*'),
                    expression[1],
                    derivative.derive(expression[2], respect_to)
                ),
                construct_binary_ast_node(
                    label('*'),
                    derivative.derive(expression[1], respect_to),
                    expression[2]
                )
            )

def derive_div(expression, respect_to):
    return construct_binary_ast_node(
                label('/'),
                construct_binary_ast_node(
                    label('-'),
                    construct_binary_ast_node(
                        label('*'),
                        derivative.derive(expression[1], respect_to),
                        expression[2]
                    ),
                    construct_binary_ast_node(
                        label('*'),
                        expression[1],
                        derivative.derive(expression[2], respect_to)
                    ),
                ),
                construct_binary_ast_node(
                    label('*'),
                    expression[2],
                    expression[2]
                )
            )

def derive_sub(expression, respect_to):
    # TODO Use construct_binary_ast_node
    return (expression[0], derivative.derive(expression[1], respect_to), derivative.derive(expression[2], respect_to))

def derive_add(expression, respect_to):
    # TODO Use construct_binary_ast_node
    return (expression[0], derivative.derive(expression[1], respect_to), derivative.derive(expression[2], respect_to))

def derive_pow(expression, respect_to):
    # TODO CURRENTLY ASSUMES A CONSTANT IN THE EXPONENT, FIX THIS
    # TODO WOW THIS METHOD IS BAD, FIX THIS
    return construct_binary_ast_node(
                label('*'),
                expression[2],
                construct_binary_ast_node(
                    label('*'),
                    construct_binary_ast_node(
                        label('^'),
                        expression[1],
                        (str(float(expression[2][0]) - 1), 'CONSTANT')
                    ),
                    derivative.derive(expression[1], respect_to)
                )
            )
