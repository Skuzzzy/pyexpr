from sets import Set
import re

# + * 3 x * ^ x 2 2
# 2 x 2 ^ *

binary_operators = ['*', '/', '+', '^', '-']
operator_set = Set(binary_operators)


def label_tokens(tok_arr):
    labeled = []
    for token in tok_arr:
        labeled.append(label(token))
    return labeled

def construct_binary_ast_node(op_token, expr1, expr2):
    return (op_token, expr1, expr2)

def construct_const_ast_node(const_token):
    return (const_token,)

def get_token_type(token):
    return token[1]

def get_token_value(token):
    return token[0]

def construct_ast(labeled_arr):
    param_stack = []
    for labeled in labeled_arr:
        token_type = get_token_type(labeled)
        token_value = get_token_value(labeled)

        if token_type == 'UNKNOWN':
            raise Exception('Unknown Token Type')
        if token_type in ['OPERATOR']:
            if token_value in binary_operators:
                node = construct_binary_ast_node(labeled, param_stack.pop(), param_stack.pop())
                param_stack.append(node)
            else:
                # TODO
                raise Exception('TODO Not Implemented')
        if token_type in ['CONSTANT', 'IDENTIFIER']:
            param_stack.append(construct_const_ast_node(labeled))

    if len(param_stack) != 1:
        print "\n".join([str(x) for x in param_stack])
        raise Exception('Param stack at unexpected size')

    return param_stack.pop()

def numerical(string):
    try:
        float(string)
        return True
    except (TypeError, ValueError):
        return False

def label(token):
    # ( TOKEN, TYPE )
    if token in operator_set:
        return (token, 'OPERATOR')
    if numerical(token):
        return (token, 'CONSTANT')
    if re.match(r'^[a-zA-Z]+$', token):
        return (token, 'IDENTIFIER')

    return (token, 'UNKNOWN')

def construct_expr_ast(token_list):
    return construct_ast(label_tokens(token_list))


# test = ['2', 'x', '2', '^', '*']
# test = ['x', '2', '*']
# test = ['2']
# labeled = label_tokens(test)
# print labeled
# ast = construct_ast(labeled)
# print ast
