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

import os

from common import *
from eqtex import *


class TestFileOutput(TestBase):
    def setup_method(self):
        os.system('rm *tex -f')

    def teardown_method(self):
        os.system('rm *tex -f')

    def test_enable_single_eq(self):
        global eqtex_config
        eqtex_config.file_output_single_eq = True

        @eqtex()
        def func():
            a = 1
            b = 2

        func()

        assert os.path.exists('TestFileOutput_test_enable_single_eq_func_sym.tex')
        with open('TestFileOutput_test_enable_single_eq_func_sym.tex', 'r') as f:
            assert f.read() == r'a=1\\b=2'

        assert os.path.exists('TestFileOutput_test_enable_single_eq_func_num.tex')
        with open('TestFileOutput_test_enable_single_eq_func_num.tex', 'r') as f:
            assert f.read() == r'a=1\\b=2'

    def test_disable_single_eq(self):
        global eqtex_config
        eqtex_config.file_output_single_eq = False

        @eqtex()
        def func():
            a = 1
            b = 2

        func()

        assert os.path.exists('TestFileOutput_test_disable_single_eq_func_sym_0.tex')
        with open('TestFileOutput_test_disable_single_eq_func_sym_0.tex', 'r') as f:
            assert f.read() == r'a=1'

        assert os.path.exists('TestFileOutput_test_disable_single_eq_func_sym_1.tex')
        with open('TestFileOutput_test_disable_single_eq_func_sym_1.tex', 'r') as f:
            assert f.read() == r'b=2'

        assert os.path.exists('TestFileOutput_test_disable_single_eq_func_num_0.tex')
        with open('TestFileOutput_test_disable_single_eq_func_num_0.tex', 'r') as f:
            assert f.read() == r'a=1'

        assert os.path.exists('TestFileOutput_test_disable_single_eq_func_num_1.tex')
        with open('TestFileOutput_test_disable_single_eq_func_num_1.tex', 'r') as f:
            assert f.read() == r'b=2'
