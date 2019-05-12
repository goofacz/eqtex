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
import ast
import sys

from .file_output import _FileOutput
from .source_visitor import SourceVisitor
from .config import eqtex_config
from .cache import cache

_source = None


def _process_func(file_path, func, **kwargs):
    global eqtex_config

    func_qualname = func.__qualname__.replace('<locals>.', '')
    output = _FileOutput()
    config = copy.deepcopy(eqtex_config)

    for key, val in kwargs.items():
        if key == 'output':
            output = val
        else:
            setattr(config, key, val)

    with open(file_path) as handle:
        tree = ast.parse(handle.read())

    v = SourceVisitor(func_qualname, output, config)
    v.visit(tree)

def _trace_handler(frame, event, arg):
    pass

def eqtex(**eqtex_kwargs):
    file_path = inspect.stack()[1][1]

    def decorator(func):
        def wrapped(*args, **kwargs):
            global eqtex_config

            if eqtex_config.enabled:
                global cache

                if not cache.has_func(func.__qualname__):
                    try:
                        sys.settrace(_trace_handler)
                        result = func(*args, **kwargs)
                    except:
                        raise
                    finally:
                        sys.settrace(None)

                    _process_func(file_path, func, **eqtex_kwargs)

                    return result

            return func(*args, **kwargs)

        return wrapped

    return decorator
