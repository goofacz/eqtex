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

import ast
import os


class _Source:
    def __init__(self, file_path=None):
        self.file_path = file_path
        self.file_name = os.path.splitext(os.path.basename(self.file_path))[0]

        with open(self.file_path) as handle:
            self.tree = ast.parse(handle.read())
