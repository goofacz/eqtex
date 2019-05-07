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

from common import *
from eqtex import *


class GlobalConfig(TestCase):
    def test_disable_all(self):
        global eqtex_config
        eqtex_config.enabled = False

        @eqtex(output=self.buffer)
        def func():
            pass

        self.assertFalse(hasattr(self.buffer, 'sym'))
        self.assertFalse(hasattr(self.buffer, 'num'))

    def test_disable_sym(self):
        global eqtex_config
        eqtex_config.sym_equation = False

        @eqtex(output=self.buffer)
        def func():
            pass

        self.assertFalse(hasattr(self.buffer, 'sym'))
        self.assertTrue(hasattr(self.buffer, 'num'))

    def test_disable_num(self):
        global eqtex_config
        eqtex_config.val_equation = False

        @eqtex(output=self.buffer)
        def func():
            pass

        self.assertTrue(hasattr(self.buffer, 'sym'))
        self.assertFalse(hasattr(self.buffer, 'num'))

    def test_disable_skip_self(self):
        global eqtex_config
        eqtex_config.skip_self = False

        class TestClass:
            def __init__(self):
                self.a = 1
                self.b = 0

            @eqtex(output=self.buffer)
            def func(self):
                self.b = self.a + 2

        self.assertEqual(self.buffer.sym,
                         ['self.b=self.a + 2'])
        self.assertEqual(self.buffer.num,
                         ['self.b=self.a + 2'])


if __name__ == '__main__':
    ut.main()
