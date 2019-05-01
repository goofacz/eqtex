import ast
import argparse
import os
from pylatex import Document
from pylatex.utils import NoEscape
from pylatex.package import Package


class _NodeVisitor(ast.NodeVisitor):
    def __init__(self):
        self.tokens = {}

    def process(self, node, ignore_missing=False):
        name = 'process_' + node.__class__.__name__
        method = getattr(self, name, None)
        if method:
            return method(node)
        elif not ignore_missing:
            raise RuntimeError(f'{name}() not found!')

    def process_Name(self, val):
        return val.id

    def process_Num(self, val):
        return str(val.n)

    def process_numpy_array(self, args):
        rows = []

        if isinstance(args[0].elts[0], ast.List):
            for row in args[0].elts:
                vals = [self.process(val) for val in row.elts]
                rows.append('&'.join(vals))
        else:
            vals = [self.process(val) for val in args[0].elts]
            rows.append('&'.join(vals))

        return r'\begin{bmatrix}' + r'\\'.join(rows) + r'\end{bmatrix}'

    def process_Call(self, val):
        if val.func.id == 'array':
            return self.process_numpy_array(val.args)
        else:
            raise RuntimeError(f'Unknown func: {val.func.id}')

    def process_BinOp(self, val):
        pass

    def process_Pass(self, _):
        pass

    def process_Assign(self, stmt):
        if len(stmt.targets) > 2:
            vals = stmt.value.elts
        else:
            vals = [stmt.value]

        for target, val in zip(stmt.targets, vals):
            name = target.id
            val = self.process(val)

            self.tokens[name] = val

            return f'{name}={val}'

    def visit_FunctionDef(self, node):
        if len(node.decorator_list) == 0:
            return

        doc = Document()
        doc.packages.append(Package('amsmath'))

        for stmt in node.body:
            doc.append(NoEscape(r'\begin{equation}'))
            doc.append(NoEscape(self.process(stmt)))
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
