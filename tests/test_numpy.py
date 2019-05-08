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

import numpy
from numpy import *

from common import TestBase
from eqtex import *


class TestNumpy(TestBase):
    def test_array(self):
        @eqtex(output=self.buffer)
        def func(y, b, a, m, p, D):
            A = array([[y], [2], [b]])
            B = array([[a, 5, (8 / m) ** 4], [2, 7, 9], [b, 5, p]])
            C = A + D

        assert self.buffer.sym == [r'A=\begin{bmatrix}y\\2\\b\end{bmatrix}',
                                   r'B=\begin{bmatrix}a&5&{\left(\frac{8}{m}\right)}^{4}\\2&7&9\\b&5&p\end{bmatrix}',
                                   r'C=A + D']
        assert self.buffer.num == [r'A=\begin{bmatrix}y\\2\\b\end{bmatrix}',
                                   r'B=\begin{bmatrix}a&5&{\left(\frac{8}{m}\right)}^{4}\\2&7&9\\b&5&p\end{bmatrix}',
                                   r'C=\begin{bmatrix}y\\2\\b\end{bmatrix} + D']

    def test_ones(self):
        # This test case also check how eqtex handles different ways of calling functions/methods.

        @eqtex(output=self.buffer)
        def func():
            A = ones([2, 4])
            B = numpy.ones([2, 4])

        assert self.buffer.sym == [r'A=\begin{bmatrix}1&1&1&1\\1&1&1&1\end{bmatrix}',
                                   r'B=\begin{bmatrix}1&1&1&1\\1&1&1&1\end{bmatrix}']
        assert self.buffer.num == [r'A=\begin{bmatrix}1&1&1&1\\1&1&1&1\end{bmatrix}',
                                   r'B=\begin{bmatrix}1&1&1&1\\1&1&1&1\end{bmatrix}']

    def test_eye(self):
        @eqtex(output=self.buffer)
        def func():
            A = eye(5)

        assert self.buffer.sym == [r'A=I_{5}']
        assert self.buffer.num == [
            r'A=\begin{bmatrix}1&0&0&0&0\\0&1&0&0&0\\0&0&1&0&0\\0&0&0&1&0\\0&0&0&0&1\end{bmatrix}_{5}']

    def test_transpose_func(self):
        @eqtex(output=self.buffer)
        def func(a, b):
            A = array([[a], [2], [b]])
            B = transpose(A)

        assert self.buffer.sym == [r'A=\begin{bmatrix}a\\2\\b\end{bmatrix}',
                                   'B={A}^{T}']
        assert self.buffer.num == [r'A=\begin{bmatrix}a\\2\\b\end{bmatrix}',
                                   r'B={\begin{bmatrix}a\\2\\b\end{bmatrix}}^{T}']

    def test_transpose_attr(self):
        @eqtex(output=self.buffer)
        def func(a, b):
            A = array([[a], [2], [b]])
            B = A.T

        assert self.buffer.sym == [r'A=\begin{bmatrix}a\\2\\b\end{bmatrix}',
                                   'B={A}^{T}']
        assert self.buffer.num == [r'A=\begin{bmatrix}a\\2\\b\end{bmatrix}',
                                   r'B={\begin{bmatrix}a\\2\\b\end{bmatrix}}^{T}']

    def test_invert(self):
        @eqtex(output=self.buffer)
        def func(a, b):
            A = array([[a], [2], [b]])
            B = invert(A)

        assert self.buffer.sym == [r'A=\begin{bmatrix}a\\2\\b\end{bmatrix}',
                                   'B={A}^{-1}']
        assert self.buffer.num == [r'A=\begin{bmatrix}a\\2\\b\end{bmatrix}',
                                   r'B={\begin{bmatrix}a\\2\\b\end{bmatrix}}^{-1}']

    def test_divide(self):
        @eqtex(output=self.buffer)
        def func(a, b, c, d, e, f):
            A = array([[a], [2], [b]])
            B = array([[c, d], [3, 4], [e, f]])
            C = divide(A, B)

        assert self.buffer.sym == [r'A=\begin{bmatrix}a\\2\\b\end{bmatrix}',
                                   r'B=\begin{bmatrix}c&d\\3&4\\e&f\end{bmatrix}',
                                   r'C=\frac{A}{B}']
        assert self.buffer.num == [r'A=\begin{bmatrix}a\\2\\b\end{bmatrix}',
                                   r'B=\begin{bmatrix}c&d\\3&4\\e&f\end{bmatrix}',
                                   r'C=\frac{\begin{bmatrix}a\\2\\b\end{bmatrix}}{\begin{bmatrix}c&d\\3&4\\e&f\end{bmatrix}}']

    def test_zeros(self):
        @eqtex(output=self.buffer)
        def func():
            A = zeros([2, 3])
            B = numpy.zeros([2, 3])

        assert self.buffer.sym == [r'A=\begin{bmatrix}0&0&0\\0&0&0\end{bmatrix}',
                                   r'B=\begin{bmatrix}0&0&0\\0&0&0\end{bmatrix}']
        assert self.buffer.num == [r'A=\begin{bmatrix}0&0&0\\0&0&0\end{bmatrix}',
                                   r'B=\begin{bmatrix}0&0&0\\0&0&0\end{bmatrix}']
