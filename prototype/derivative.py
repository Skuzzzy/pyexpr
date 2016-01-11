
from parse import get_token_type, get_token_value, label
from aux_derive import derive_mult, derive_div, derive_add, derive_sub, derive_pow

bin_operators_impl = {
        '+' : derive_add,
        '-' : derive_sub,
        '*' : derive_mult,
        '/' : derive_div,
        '^' : derive_pow
}

def derive(expression, respect_to):
    # TODO Fix access for operator expressions
    # EX * 5 x
    token_type = get_token_type(expression[0])
    token_value = get_token_value(expression[0])

    if token_type in ['CONSTANT']:
        return label('0')
    if token_type in ['IDENTIFIER']:
        # Check if in respect to identifier
        if token_value == respect_to:
            return label('1')
        else:
            return label('0')
    if token_type in ['OPERATOR']:
        # TODO implement this monster by implementing each operator individually
        # raise Exception('TODO Not Implemented')
        method = bin_operators_impl[token_value]
        return method(expression, respect_to)

    raise Exception('wat')

