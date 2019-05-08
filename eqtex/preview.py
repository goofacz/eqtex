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

import sympy as sp

from output import Output


class PreviewOutput(Output):
    def process(self, func_name, cls_prefix, eq_type, tex, config):
        base_name = f'{"_".join(cls_prefix)}_{func_name}_{eq_type.value}'
        p = r'\begin{{equation}}' \
            r'\begin{{aligned}}' \
            r'{0}' \
            r'\end{{aligned}}' \
            r'\end{{equation}}'

        if config.file_output_single_eq:
            name = f'{base_name}.png'
            sp.preview(p.format(r'\\'.join(tex)), viewer='file', euler=False, filename=name)
        else:
            for i in range(len(tex)):
                name = f'{base_name}_{i}.png'
                sp.preview(p.format(tex[i]), viewer='file', euler=False, filename=name)
