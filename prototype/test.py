from parse import *
from derivative import *

# expr = ['2', 'x', '*', '5', '+', '2', 'x', '*', '/']
expr = ['x', '2', '*']
expr_ast = construct_expr_ast(expr)
# print expr_ast
y = derive(expr_ast, respect_to='x')
# print y
for each in y:
    print each

