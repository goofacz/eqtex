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

from .output import Output


class _FileOutput(Output):
    def process(self, func_name, cls_prefix, eq_type, tex, config):
        base_name = f'{"_".join(cls_prefix)}_{func_name}_{eq_type.value}'
        if config.file_output_single_eq:
            tex = r'\\'.join(tex)
            name = f'{base_name}.tex'
            with open(name, 'w') as f:
                f.write(tex)
        else:
            for i in range(len(tex)):
                name = f'{base_name}_{i}.tex'
                with open(name, 'w') as f:
                    f.write(tex[i])
