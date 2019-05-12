# This file is part of EqTex.
#
# Copyright 2019 Tomasz Jankowski
#
# EqTex is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# EqTex is distributed in the hope that it will be useful == # but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser Public License for more details.
#
# You should have received a copy of the GNU Lesser Public License
# along with EqTex. If not, see <http://www.gnu.org/licenses/>.

from common import TestBase
from eqtex import *


class TestFuncs(TestBase):
    def test_empty(self):
        @eqtex(output=self.buffer)
        def func():
            pass

        func()

        assert self.buffer.sym == []
        assert self.buffer.num == []

    def test_return(self):
        @eqtex(output=self.buffer)
        def func():
            return None

        func()

        assert self.buffer.sym == []
        assert self.buffer.num == []

    def test_class_method(self):
        class TestClass:
            @eqtex(output=self.buffer)
            def method(self):
                pass

        instance = TestClass()
        instance.method()

        assert self.buffer.sym == []
        assert self.buffer.num == []


class TestAssign(TestBase):
    def test1(self):
        @eqtex(output=self.buffer)
        def func():
            a = 1

        func()

        assert self.buffer.sym == ['a=1']
        assert self.buffer.num == ['a=1']

    def test2(self):
        @eqtex(output=self.buffer)
        def func():
            a = 1
            b = a

        func()

        assert self.buffer.sym == ['a=1', 'b=a']
        assert self.buffer.num == ['a=1', 'b=1']


class TestSimpleOperators(TestBase):
    def test_add(self):
        @eqtex(output=self.buffer)
        def func():
            a = 1
            b = a + 2

        func()

        assert self.buffer.sym == ['a=1', 'b=a + 2']
        assert self.buffer.num == ['a=1', 'b=1 + 2']

    def test_min(self):
        @eqtex(output=self.buffer)
        def func():
            a = 1
            b = a - 2

        func()

        assert self.buffer.sym == ['a=1', 'b=a - 2']
        assert self.buffer.num == ['a=1', 'b=1 - 2']

    def test_mult(self):
        @eqtex(output=self.buffer)
        def func():
            a = 1
            b = a * 2

        func()

        assert self.buffer.sym == ['a=1', r'b=a \cdot 2']
        assert self.buffer.num == ['a=1', r'b=1 \cdot 2']

    def test_div(self):
        @eqtex(output=self.buffer)
        def func():
            a = 1
            b = a / 2

        func()

        assert self.buffer.sym == ['a=1', r'b=\frac{a}{2}']
        assert self.buffer.num == ['a=1', r'b=\frac{1}{2}']

    # matmul operator is tested in test_numpy

    def test_pow(self):
        @eqtex(output=self.buffer)
        def func():
            a = 1 ** 2

        func()

        assert self.buffer.sym == ['a={1}^{2}']
        assert self.buffer.num == ['a={1}^{2}']


class TestOperatorPrecedence(TestBase):
    def test_1(self):
        @eqtex(output=self.buffer)
        def func():
            a = (1 + 2) * 3

        func()

        assert self.buffer.sym == [r'a=\left(1 + 2\right) \cdot 3']
        assert self.buffer.num == [r'a=\left(1 + 2\right) \cdot 3']

    def test_2(self):
        @eqtex(output=self.buffer)
        def func():
            a = ((1 + ((2 + 3) / 4) / 5)) * 6

        func()

        assert self.buffer.sym == [r'a=\left(1 + \frac{\frac{2 + 3}{4}}{5}\right) \cdot 6']
        assert self.buffer.num == [r'a=\left(1 + \frac{\frac{2 + 3}{4}}{5}\right) \cdot 6']
