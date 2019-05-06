# This file is part of EqTex.
#
# Copyright 2019 Tomasz Jankowski
#
# EqTex is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# EqTex is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser Public License for more details.
#
# You should have received a copy of the GNU Lesser Public License
# along with EqTex. If not, see <http://www.gnu.org/licenses/>.

import unittest as ut

import numpy
from numpy import *

from eqtex import *


class Buffer(Output):
    def process(self, func_name, cls_prefix, eq_type, tex, config):
        if eq_type == Output.EqType.SYM:
            self.sym = tex
        elif eq_type == Output.EqType.NUM:
            self.num = tex


class TestCase(ut.TestCase):
    def setUp(self):
        self.buffer = Buffer()


class TestNumpy(TestCase):
    def test_ones(self):
        # This test case also check how eqtex handles different ways of calling functions/methods.

        @eqtex(output=self.buffer)
        def func():
            A = ones([2, 4])
            B = numpy.ones([2, 4])

        self.assertEqual(self.buffer.sym,
                         [r'A=\begin{bmatrix}1&1&1&1\\1&1&1&1\end{bmatrix}',
                          r'B=\begin{bmatrix}1&1&1&1\\1&1&1&1\end{bmatrix}'])
        self.assertEqual(self.buffer.num,
                         [r'A=\begin{bmatrix}1&1&1&1\\1&1&1&1\end{bmatrix}',
                          r'B=\begin{bmatrix}1&1&1&1\\1&1&1&1\end{bmatrix}'])

    def test_eye(self):
        @eqtex(output=self.buffer)
        def func():
            A = eye(5)

        self.assertEqual(self.buffer.sym,
                         [r'A=I_{5}'])
        self.assertEqual(self.buffer.num,
                         [r'A=\begin{bmatrix}1&0&0&0&0\\0&1&0&0&0\\0&0&1&0&0\\0&0&0&1&0\\0&0&0&0&1\end{bmatrix}_{5}'])

    def test_transpose(self):
        @eqtex(output=self.buffer)
        def func(a, b):
            A = array([[a], [2], [b]])
            B = transpose(A)

        self.assertEqual(self.buffer.sym,
                         [r'A=\begin{bmatrix}a\\2\\b\end{bmatrix}',
                          'B={A}^{T}'])
        self.assertEqual(self.buffer.num,
                         [r'A=\begin{bmatrix}a\\2\\b\end{bmatrix}',
                          r'B={\begin{bmatrix}a\\2\\b\end{bmatrix}}^{T}'])

    def test_invert(self):
        @eqtex(output=self.buffer)
        def func(a, b):
            A = array([[a], [2], [b]])
            B = invert(A)

        self.assertEqual(self.buffer.sym,
                         [r'A=\begin{bmatrix}a\\2\\b\end{bmatrix}',
                          'B={A}^{-1}'])
        self.assertEqual(self.buffer.num,
                         [r'A=\begin{bmatrix}a\\2\\b\end{bmatrix}',
                          r'B={\begin{bmatrix}a\\2\\b\end{bmatrix}}^{-1}'])

    def test_divide(self):
        @eqtex(output=self.buffer)
        def func(a, b, c, d, e, f):
            A = array([[a], [2], [b]])
            B = array([[c, d], [3, 4], [e, f]])
            C = divide(A, B)

        self.assertEqual(self.buffer.sym,
                         [r'A=\begin{bmatrix}a\\2\\b\end{bmatrix}',
                          r'B=\begin{bmatrix}c&d\\3&4\\e&f\end{bmatrix}',
                          r'C=\frac{A}{B}'])
        self.assertEqual(self.buffer.num,
                         [r'A=\begin{bmatrix}a\\2\\b\end{bmatrix}',
                          r'B=\begin{bmatrix}c&d\\3&4\\e&f\end{bmatrix}',
                          r'C=\frac{\begin{bmatrix}a\\2\\b\end{bmatrix}}{\begin{bmatrix}c&d\\3&4\\e&f\end{bmatrix}}'])

    def test_zeros(self):
        @eqtex(output=self.buffer)
        def func():
            A = zeros([2, 3])
            B = numpy.zeros([2, 3])

        self.assertEqual(self.buffer.sym,
                         [r'A=\begin{bmatrix}0&0&0\\0&0&0\end{bmatrix}',
                          r'B=\begin{bmatrix}0&0&0\\0&0&0\end{bmatrix}'])
        self.assertEqual(self.buffer.num,
                         [r'A=\begin{bmatrix}0&0&0\\0&0&0\end{bmatrix}',
                          r'B=\begin{bmatrix}0&0&0\\0&0&0\end{bmatrix}'])


if __name__ == '__main__':
    ut.main()
