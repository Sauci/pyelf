"""
:file: __init__.py
:author: Guillaume Sottas
:date: 27/06/2018
"""

__version__ = '0.0.1'
__title__ = 'pyelf'
__author__ = 'Guillaume Sottas'
__copyright__ = 'Copyright 2018 Guillaume Sottas.'
__license__ = 'BSD-3'
__url__ = 'http://www.github.com/Sauci/pyelf'
__description__ = ''
__long_description__ = ''''''

from .cli import main
from .pyelf import Address, ElfException, ElfFile, Symbol
