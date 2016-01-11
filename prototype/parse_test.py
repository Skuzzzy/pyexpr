import unittest
from parse import label, numerical

class TestParse(unittest.TestCase):

    def test_label_operator_plus(self):
        expected = ('+', 'OPERATOR')
        result = label('+')
        self.assertEqual(expected, result)

    def test_label_operator_minus(self):
        expected = ('-', 'OPERATOR')
        result = label('-')
        self.assertEqual(expected, result)

    def test_label_operator_pow(self):
        expected = ('^', 'OPERATOR')
        result = label('^')
        self.assertEqual(expected, result)

    def test_label_operator_mult(self):
        expected = ('*', 'OPERATOR')
        result = label('*')
        self.assertEqual(expected, result)

    def test_label_operator_div(self):
        expected = ('/', 'OPERATOR')
        result = label('/')
        self.assertEqual(expected, result)

    def test_label_num1(self):
        expected = ('5.5', 'CONSTANT')
        result = label('5.5')
        self.assertEqual(expected, result)

    def test_label_num2(self):
        expected = ('67', 'CONSTANT')
        result = label('67')
        self.assertEqual(expected, result)

    def test_label_ident1(self):
        expected = ('x', 'IDENTIFIER')
        result = label('x')
        self.assertEqual(expected, result)

    def test_label_ident2(self):
        expected = ('apples', 'IDENTIFIER')
        result = label('apples')
        self.assertEqual(expected, result)

    def test_label_bad(self):
        expected = ('pear95', 'UNKNOWN')
        result = label('pear95')
        self.assertEqual(expected, result)

    def test_numerical_false(self):
        param = 'ff5.5'
        self.assertFalse(numerical(param))

    def test_numerical_true(self):
        param = '5.5'
        self.assertTrue(numerical(param))

if __name__ == '__main__':
    unittest.main()
