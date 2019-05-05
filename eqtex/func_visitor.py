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

from .visitor import Visitor


class FuncVisitor(Visitor):
    def __init__(self):
        self.tokens = {}
        self.func_name = None
        self.sym_tex = []
        self.val_tex = []

    def get_precedense(self, op):
        return {
            ast.Pow: 2,
            ast.MatMult: 1,
            ast.Mult: 1,
            ast.Div: 1,
            ast.Add: 0,
            ast.Sub: 0,
        }[op.__class__]

    def create_matrix(self, args, val):
        rows = args[0].elts[0].n
        cols = args[0].elts[1].n
        p = r'\begin{{bmatrix}}{0}\end{{bmatrix}}'
        vals = r'\\'.join(rows * [r'&'.join(cols * [val])])
        return p.format(vals), p.format(vals)

    def process_Name(self, val):
        return val.id, self.tokens.get(val.id, val.id)

    def process_Num(self, val):
        return str(val.n), str(val.n)

    def process_numpy_invert(self, args):
        sym, val = self.process(args[0])
        if isinstance(args[0], ast.BinOp):
            p = r'{{\left({0}\right)}}^{{-1}}'
        else:
            p = r'{{{0}}}^{{-1}}'

        return p.format(sym), p.format(val)

    def process_numpy_transpose(self, args):
        sym = args[0].id
        val = self.tokens.get(sym, sym)
        p = '{{{0}}}^{{T}}'
        return p.format(sym), p.format(val)

    def process_numpy_eye(self, args):
        size = args[0].n
        rows = []
        row = [str(val) for val in [1] + (size - 1) * [0]]
        for _ in range(size):
            rows.append('&'.join(row))
            row = row[-1:] + row[:-1]

        return r'I_{{{0}}}'.format(str(size)), \
               r'\begin{{bmatrix}}{0}\end{{bmatrix}}_{{{1}}}'.format(r'\\'.join(rows), str(size))

    def process_numpy_divide(self, args):
        l_sym, l_val = self.process(args[0])
        r_sym, r_val = self.process(args[1])
        p = r'\frac{{{0}}}{{{1}}}'
        return p.format(l_sym, r_sym), p.format(l_val, r_val)

    def process_numpy_ones(self, args):
        return self.create_matrix(args, '1')

    def process_numpy_zeros(self, args):
        return self.create_matrix(args, '0')

    def process_numpy_array(self, args):
        sym_rows = []
        val_rows = []

        if isinstance(args[0].elts[0], ast.List):
            for row in args[0].elts:
                syms, vals = zip(*[self.process(val) for val in row.elts])
                sym_rows.append('&'.join(syms))
                val_rows.append('&'.join(vals))
        else:
            syms, vals = zip(*[self.process(val) for val in args[0].elts])
            sym_rows.append('&'.join(syms))
            val_rows.append('&'.join(vals))

        p = r'\begin{{bmatrix}}{0}\end{{bmatrix}}'
        return p.format(r'\\'.join(sym_rows)), p.format(r'\\'.join(val_rows))

    def process_Call(self, val):
        if isinstance(val.func, ast.Name):
            return self.process(val.args, func_suffix=f'numpy_{val.func.id}')
        elif isinstance(val.func, ast.Attribute):
            return self.process(val.args, func_suffix=f'numpy_{val.func.attr}')

    def process_BinOp(self, val):
        l = self.process(val.left)
        r = self.process(val.right)
        p = r'\left({0}\right)'

        if isinstance(val.left, ast.BinOp):
            l_sym, l_val = l
            if (self.get_precedense(val.left.op) < self.get_precedense(val.op)) and not isinstance(val.op, ast.Div):
                l = [p.format(l_sym), p.format(l_val)]
        if isinstance(val.right, ast.BinOp):
            r_sym, r_val = r
            if (self.get_precedense(val.right.op) < self.get_precedense(val.op)) and not isinstance(val.op, ast.Div):
                l = [p.format(r_sym), p.format(r_val)]

        return self.process(val.op, l, r)

    def process_UnaryOp(self, stmt):
        return self.process(stmt.op, stmt.operand)

    def process_Mult(self, _, l, r):
        l_sym, l_val = l
        r_sym, r_val = r
        p = r'{0} \cdot {1}'
        return p.format(l_sym, r_sym), p.format(l_val, r_val)

    def process_Sub(self, _, l, r):
        l_sym, l_val = l
        r_sym, r_val = r
        p = r'{0} - {1}'
        return p.format(l_sym, r_sym), p.format(l_val, r_val)

    def process_Div(self, _, l, r):
        l_sym, l_val = l
        r_sym, r_val = r
        p = r'\frac{{{0}}}{{{1}}}'
        return p.format(l_sym, r_sym), p.format(l_val, r_val)

    def process_Add(self, _, l, r):
        l_sym, l_val = l
        r_sym, r_val = r
        p = r'{0} + {1}'
        return p.format(l_sym, r_sym), p.format(l_val, r_val)

    def process_MatMult(self, _, l, r):
        l_sym, l_val = l
        r_sym, r_val = r
        p = r'{0} \, {1}'
        return p.format(l_sym, r_sym), p.format(l_val, r_val)

    def process_USub(self, _, stmt):
        sym, val = self.process(stmt)

        if isinstance(stmt, ast.BinOp):
            p = r'\left({0}\right)'
            sym, val = p.format(sym), p.format(val)

        p = r' - {0}'
        return p.format(sym), p.format(val)

    def process_Pow(self, _, l, r):
        l_sym, l_val = l
        r_sym, r_val = r

        p = r'{{{0}}}^{{{1}}}'
        return p.format(l_sym, r_sym), p.format(l_val, r_val)

    def process_Assign(self, stmt):
        if len(stmt.targets) > 2:
            vals = stmt.value.elts
        else:
            vals = [stmt.value]

        for target, val in zip(stmt.targets, vals):
            name, _ = self.process(target)
            sym, val = self.process(val)
            self.tokens[name] = val
            return f'{name}={sym}', f'{name}={val}'

    def process_Attribute(self, attr):
        if attr.value.id == 'self':
            return attr.attr, self.tokens.get(attr.attr, attr.attr)
        elif attr.attr == 'T':
            return self.process_numpy_transpose([attr.value])
        else:
            raise RuntimeError(f'Unknow attribute: {attr.attr}')

    def visit_FunctionDef(self, func):
        if self.func_name:
            return  # TODO Skip internal functions

        self.func_name = func.name

        for stmt in func.body:
            sym, val = self.process(stmt)
            if sym:
                self.sym_tex.append(sym)
            if val:
                self.val_tex.append(val)
