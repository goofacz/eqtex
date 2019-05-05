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

from .func_visitor import FuncVisitor
from .output import Output
from .visitor import Visitor


class SourceVisitor(Visitor):
    def __init__(self, target_func_qualname, output, config):
        self.prefix = []
        self.target_func_qualname = target_func_qualname
        self.output = output
        self.config = config

    def store_tex(self, visitor):
        if not self.config.store_tex:
            return

        if self.config.sym_equation:
            self.output.process(visitor.func_name, self.prefix, Output.EqType.SYM, visitor.sym_tex, self.config)

        if self.config.val_equation:
            self.output.process(visitor.func_name, self.prefix, Output.EqType.NUM, visitor.val_tex, self.config)

    def visit_FunctionDef(self, func):
        tag = next((t for t in func.decorator_list if t.func.id == 'eqtex'), None)
        if tag:
            if self.target_func_qualname:
                func_qualname = f'{".".join(self.prefix)}.{func.name}'
                if func_qualname != self.target_func_qualname:
                    return

            v = FuncVisitor()
            v.visit(func)

            self.store_tex(v)
        else:
            self.prefix.append(func.name)
            for node in func.body:
                self.visit(node)
            self.prefix.pop()

    def visit_ClassDef(self, cls):
        self.prefix.append(cls.name)
        for node in cls.body:
            self.visit(node)
        self.prefix.pop()
