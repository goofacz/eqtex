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

import argparse
import ast
import os

from .file_output import _FileOutput
from .source_visitor import _SourceVisitor


def _handle_cmg_args():
    p = argparse.ArgumentParser()
    p.add_argument('sources', help='Python file or src directory', type=str)
    return p.parse_args()


def _find_file_paths(cmd_args):
    if os.path.isfile(cmd_args.sources):
        return [cmd_args.sources]
    else:
        raise RuntimeError('TODO')


def _process_file(file_path):
    with open(file_path, 'r') as file:
        global eqtex_config
        tree = ast.parse(file.read())
        output = _FileOutput()
        _SourceVisitor(None, output, eqtex_config).visit(tree)


def _process_files(file_paths):
    for file_path in file_paths:
        _process_file(file_path)


def _main():
    cmd_args = _handle_cmg_args()
    file_paths = _find_file_paths(cmd_args)
    _process_files(file_paths)

