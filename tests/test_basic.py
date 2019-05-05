import unittest as ut

from eqtex.eqtex import *


class Buffer(Output):
    def process(self, func_name, cls_prefix, eq_type, tex, config):
        if eq_type == Output.EqType.SYM:
            self.sym = tex
        elif eq_type == Output.EqType.NUM:
            self.num = tex


class TestCase(ut.TestCase):
    def setUp(self):
        self.buffer = Buffer()


class EmptyFunc(TestCase):
    def test_empty(self):
        @eqtex(output=self.buffer)
        def func():
            pass

        self.assertEqual(self.buffer.sym, [])
        self.assertEqual(self.buffer.num, [])


class Assign(TestCase):
    def test1(self):
        @eqtex(output=self.buffer)
        def func():
            a = 1

        self.assertEqual(self.buffer.sym,
                         ['a=1'])
        self.assertEqual(self.buffer.num,
                         ['a=1'])

    def test2(self):
        @eqtex(output=self.buffer)
        def func():
            a = 1
            b = a

        self.assertEqual(self.buffer.sym,
                         ['a=1',
                          'b=a'])
        self.assertEqual(self.buffer.num,
                         ['a=1',
                          'b=1'])


class SimpleOperators(TestCase):
    def test_add(self):
        @eqtex(output=self.buffer)
        def func():
            a = 1
            b = a + 2

        self.assertEqual(self.buffer.sym,
                         ['a=1',
                          'b=a + 2'])
        self.assertEqual(self.buffer.num,
                         ['a=1',
                          'b=1 + 2'])

    def test_min(self):
        @eqtex(output=self.buffer)
        def func():
            a = 1
            b = a - 2

        self.assertEqual(self.buffer.sym,
                         ['a=1',
                          'b=a - 2'])
        self.assertEqual(self.buffer.num,
                         ['a=1',
                          'b=1 - 2'])

    def test_mult(self):
        @eqtex(output=self.buffer)
        def func():
            a = 1
            b = a * 2

        self.assertEqual(self.buffer.sym,
                         ['a=1',
                          r'b=a \cdot 2'])
        self.assertEqual(self.buffer.num,
                         ['a=1',
                          r'b=1 \cdot 2'])

    def test_div(self):
        @eqtex(output=self.buffer)
        def func():
            a = 1
            b = a / 2

        self.assertEqual(self.buffer.sym,
                         ['a=1',
                          r'b=\frac{a}{2}'])
        self.assertEqual(self.buffer.num,
                         ['a=1',
                          r'b=\frac{1}{2}'])

    def test_matmul(self):
        @eqtex(output=self.buffer)
        def func():
            a = 1
            b = a @ 2

        self.assertEqual(self.buffer.sym,
                         ['a=1',
                          r'b=a \, 2'])
        self.assertEqual(self.buffer.num,
                         ['a=1',
                          r'b=1 \, 2'])

    def test_pow(self):
        @eqtex(output=self.buffer)
        def func():
            a = 1 ** 2

        self.assertEqual(self.buffer.sym,
                         ['a={1}^{2}'])
        self.assertEqual(self.buffer.num,
                         ['a={1}^{2}'])


class OperatorPrecedence(TestCase):
    def test_1(self):
        @eqtex(output=self.buffer)
        def func():
            a = (1 + 2) * 3

        self.assertEqual(self.buffer.sym,
                         [r'a=\left(1 + 2\right) \cdot 3'])
        self.assertEqual(self.buffer.num,
                         [r'a=\left(1 + 2\right) \cdot 3'])

    def test_2(self):
        @eqtex(output=self.buffer)
        def func():
            a = ((1 + ((2 + 3) / 4) / 5)) * 6

        self.assertEqual(self.buffer.sym,
                         [r'a=\left(1 + \frac{\frac{2 + 3}{4}}{5}\right) \cdot 6'])
        self.assertEqual(self.buffer.num,
                         [r'a=\left(1 + \frac{\frac{2 + 3}{4}}{5}\right) \cdot 6'])


if __name__ == '__main__':
    ut.main()
