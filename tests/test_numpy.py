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

from eqtex import *
from numpy import *


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


if __name__ == '__main__':
    ut.main()
