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


class _Visitor(ast.NodeVisitor):
    def process(self, node, *args, func_suffix=None, ignore_missing=True):
        if func_suffix:
            name = f'process_{func_suffix}'
        else:
            name = f'process_{node.__class__.__name__}'

        method = getattr(self, name, None)
        if method:
            return method(node, *args)
        elif ignore_missing:
            return None, None
        else:
            raise RuntimeError(f'{name}() not found!')
