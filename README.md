![tests status](https://github.com/Sauci/pyelf/actions/workflows/test.yml/badge.svg)
[![code coverage](https://codecov.io/gh/Sauci/pyelf/branch/master/graph/badge.svg?token=Q5aceZRFXh)](https://codecov.io/gh/Sauci/pyelf)

## package description

the purpose of this package is to provide high level API to work
with [elf](https://en.wikipedia.org/wiki/Executable_and_Linkable_Format) files.

## installation

### using `pip`

install the package by running the following command:
`pip install git+https://github.com/Sauci/pyelf.git@master`

### from source

this package uses [pyelftools](https://pypi.org/project/pyelftools) package. if it is not already installed, install it
first. once the above prerequisite is installed:

- download the [pyelf](https://github.com/Sauci/pyelf/archive/master.zip) package
- unzip it
- move to the directory containing the setup.py file
- run the command `python setup.py install`

**note:** the above command might require privileged access to succeed.

## example of usage

the bellow code snippet shows how to load an elf file and get some of its properties.

```python
from pyelf import ElfFile

elf = ElfFile('tests/input.elf')

# get a list of all symbols in file tests/input.elf.
symbols = elf.symbols()
assert 'symbol_uint8' in symbols

# get an instance of Symbol class for symbol named symbol_uint8.
symbol = elf.get_symbol('symbol_uint8')

# get address of symbol symbol_uint8.
assert isinstance(symbol.address, int)

# get size of symbol symbol_uint8.
assert symbol.size == 1

```
