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

from setuptools import setup

setup(
    name='eqtex',
    version='0.1',
    description='EqTex is a Python module for transforming while functions with math equations to LaTeX',
    packages=['eqtex'],
    url='https://github.com/goofacz/eqtex',
    author='Tomasz Jankowski',
    author_email='tomasz.jankowski.mail@gmail.com',
    keywords='python scientific latex numpy',
    python_requires='>=3.6',
    install_require=['sympy>=1.4'],
    extras_require={
        'test': ['numpy>=1.16', 'pytest>=4.4'],
    },

    # TODO
    # - classifiers
)
