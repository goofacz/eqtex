import argparse
import ast
import os

from pylatex import Document
from pylatex.package import Package
from pylatex.utils import NoEscape


class _NodeVisitor(ast.NodeVisitor):
    def __init__(self):
        self.tokens = {}

    def get_precedense(self, op):
        return {
            ast.Pow: 2,
            ast.MatMult: 1,
            ast.Mult: 1,
            ast.Div: 1,
            ast.Add: 0,
            ast.Sub: 0,
        }[op.__class__]

    def process(self, node, *args, func_suffix=None, ignore_missing=False):
        if func_suffix:
            name = f'process_{func_suffix}'
        else:
            name = f'process_{node.__class__.__name__}'

        method = getattr(self, name, None)
        if method:
            return method(node, *args)
        elif not ignore_missing:
            raise RuntimeError(f'{name}() not found!')

    def process_Name(self, val):
        return val.id, self.tokens.get(val.id,val.id)

    def process_Num(self, val):
        return str(val.n), str(val.n)

    def process_numpy_invert(self, args):
        sym = args[0].id
        val = self.tokens.get(sym, sym)

        return '{' + sym + '}^{-1}', \
               '{' + val + '}^{-1}'

    def process_numpy_transpose(self, args):
        sym = args[0].id
        val = self.tokens.get(sym, sym)

        return '{' + sym + '}^{T}', \
               '{' + val + '}^{T}'

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

        return r'\begin{bmatrix}' + r'\\'.join(sym_rows) + r'\end{bmatrix}', \
               r'\begin{bmatrix}' + r'\\'.join(val_rows) + r'\end{bmatrix}'

    def process_Call(self, val):
        return self.process(val.args, func_suffix=f'numpy_{val.func.id}', ignore_missing=False)

    def process_BinOp(self, val):
        l = self.process(val.left)
        r = self.process(val.right)

        if isinstance(val.left, ast.BinOp):
            l_sym, l_val = l
            if (self.get_precedense(val.left.op) < self.get_precedense(val.op)) and not isinstance(val.op, ast.Div):
                l = (r'\left(' + l_sym + r'\right)', r'\left(' + l_val + r'\right)')
        if isinstance(val.right, ast.BinOp):
            r_sym, r_val = r
            if (self.get_precedense(val.right.op) < self.get_precedense(val.op)) and not isinstance(val.op, ast.Div):
                r = (r'\left(' + r_sym + r'\right)', r'\left(' + r_val + r'\right)')
        return self.process(val.op, l, r)

    def process_Pass(self, _):
        pass

    def process_Mult(self, _, l, r):
        l_sym, l_val = l
        r_sym, r_val = r
        return l_sym + r' \cdot ' + r_sym,\
               l_val + r' \cdot ' + r_val

    def process_Sub(self, _, l, r):
        l_sym, l_val = l
        r_sym, r_val = r
        return l_sym + r' - ' + r_sym,\
               l_val + r' - ' + r_val

    def process_Div(self, _, l, r):
        l_sym, l_val = l
        r_sym, r_val = r
        return r'\frac{' + l_sym + r'}{' + r_sym + r'}', \
               r'\frac{' + l_val + r'}{' + r_val + r'}'

    def process_Assign(self, stmt):
        if len(stmt.targets) > 2:
            vals = stmt.value.elts
        else:
            vals = [stmt.value]

        for target, val in zip(stmt.targets, vals):
            name = target.id
            sym, val = self.process(val)
            self.tokens[name] = val
            return f'{name}={sym}', f'{name}={val}'

    def process_Attribute(self, attr):
        if attr.attr == 'T':
            return self.process_numpy_transpose([attr.value])
        else:
            raise RuntimeError(f'Unknow attribute: {attr.attr}')

    def visit_FunctionDef(self, node):
        if len(node.decorator_list) == 0:
            return

        doc = Document()
        doc.packages.append(Package('amsmath'))

        for stmt in node.body:
            sym, val = self.process(stmt)
            doc.append(NoEscape(r'\begin{equation}'))
            doc.append(NoEscape(sym))
            doc.append(NoEscape(r'\end{equation}'))
            doc.append(NoEscape(r'\begin{equation}'))
            doc.append(NoEscape(val))
            doc.append(NoEscape(r'\end{equation}'))

        doc.generate_pdf('numpy_ex', clean_tex=False)


def eqtex():
    pass


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
        tree = ast.parse(file.read())
        _NodeVisitor().visit(tree)


def _process_files(file_paths):
    for file_path in file_paths:
        _process_file(file_path)


def _main():
    cmd_args = _handle_cmg_args()
    file_paths = _find_file_paths(cmd_args)
    _process_files(file_paths)


if __name__ == '__main__':
    _main()