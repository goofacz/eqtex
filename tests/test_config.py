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

from eqtex import *


class Buffer(Output):
    def __init__(self):
        self.sym = False
        self.num = False

    def process(self, func_name, cls_prefix, eq_type, tex, config):
        if eq_type == Output.EqType.SYM:
            self.sym = True
        elif eq_type == Output.EqType.NUM:
            self.num = True


class GlobalConfig(ut.TestCase):
    def setUp(self):
        self.buffer = Buffer()

        global eqtex_config
        eqtex_config.enabled = False
        eqtex_config.sym_equation = False
        eqtex_config.val_equation = False

    def tearDown(self):
        global eqtex_config
        eqtex_config.enabled = True
        eqtex_config.sym_equation = True
        eqtex_config.val_equation = True

    def test_disable_all(self):
        @eqtex(output=self.buffer)
        def func():
            pass

        self.assertFalse(self.buffer.sym)
        self.assertFalse(self.buffer.num)

    def test_disable_sym(self):
        global eqtex_config
        eqtex_config.enabled = True
        eqtex_config.sym_equation = True

        @eqtex(output=self.buffer)
        def func():
            pass

        self.assertTrue(self.buffer.sym)
        self.assertFalse(self.buffer.num)

    def test_disable_num(self):
        global eqtex_config
        eqtex_config.enabled = True
        eqtex_config.val_equation = True

        @eqtex(output=self.buffer)
        def func():
            pass

        self.assertFalse(self.buffer.sym)
        self.assertTrue(self.buffer.num)


if __name__ == '__main__':
    ut.main()
