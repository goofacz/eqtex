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

import copy
import inspect

from .file_output import _FileOutput
from .source import Source
from .source_visitor import SourceVisitor
from .config import eqtex_config

_source = None


def _process_func(func, **kwargs):
    global _source
    global eqtex_config

    func_qualname = func.__qualname__.replace('<locals>.', '')
    output = _FileOutput()
    config = copy.deepcopy(eqtex_config)

    for key, val in kwargs.items():
        if key == 'output':
            output = val
        else:
            setattr(config, key, val)

    v = SourceVisitor(func_qualname, output, config)
    v.visit(_source.tree)


def eqtex(**kwargs):
    file_path = inspect.stack()[1][1]

    def decorator(func):
        if eqtex_config.enabled:
            global _source
            if not _source:
                _source = Source(file_path)
            _process_func(func, **kwargs)
        return func

    return decorator
