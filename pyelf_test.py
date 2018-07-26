"""
:file: pyelf_test.py
:author: Guillaume Sottas
:date: 27/06/2018
"""

import os
import pytest
from pyelf.pyelf import Address, ElfException, ElfFile


@pytest.fixture
def elf_path():
    for elf in [os.path.join('test_input', f) for f in os.listdir("test_input") if f.endswith('.elf')]:
        yield (elf)


def test_address_string_format():
    address = Address(12)
    assert str(address) == '0x0000000C'


def test_path(elf_path):
    assert ElfFile(elf_path).path() == elf_path


def test_files():
    elf_file = ElfFile(os.path.join('test_input', 'input.elf'))
    assert 'Application.c' in elf_file.files()


def test_symbols():
    elf_file = ElfFile(os.path.join('test_input', 'input.elf'))
    assert 'symbol_uint8' in elf_file.symbols()
    assert 'symbol_uint16' in elf_file.symbols()
    assert 'symbol_uint32' in elf_file.symbols()
    assert 'symbol_sint8' in elf_file.symbols()
    assert 'symbol_sint16' in elf_file.symbols()
    assert 'symbol_sint32' in elf_file.symbols()


def test_get_base_address():
    elf_file = ElfFile(os.path.join('test_input', 'input.elf'))
    assert elf_file.get_base_address() == 0x08000000


def test_get_abi_info():
    elf_file = ElfFile(os.path.join('test_input', 'input.elf'))
    abi_info = elf_file.get_abi_info()
    assert abi_info.machine == 'EM_ARM'
    assert abi_info.version == 'EV_CURRENT'


def test_get_endianness():
    elf_file = ElfFile(os.path.join('test_input', 'input.elf'))
    endianness = elf_file.endianness
    assert endianness == 'big'


@pytest.mark.parametrize('symbol, size, address', ((
        ('symbol_uint8', 1, 0x080154CC),
        ('symbol_uint16', 2, 0x080154CE),
        ('symbol_uint32', 4, 0x080154D0),
        ('symbol_sint8', 1, 0x080154D4),
        ('symbol_sint16', 2, 0x080154D6),
        ('symbol_sint32', 4, 0x080154D8))))
def test_get_symbol(symbol, size, address):
    elf = ElfFile(os.path.join('test_input', 'input.elf'))
    assert elf.get_symbol(symbol).size() == size
    assert elf.get_symbol(symbol).address() == address


def test_get_not_existent_symbol():
    elf = ElfFile(os.path.join('test_input', 'input.elf'))
    with pytest.raises(ElfException):
        elf.get_symbol('not valid symbol')


def test_get_binary():
    elf = ElfFile(os.path.join('test_input', 'input.elf'))
    with open(elf.path().replace('.elf', '.bin'), 'rb') as fp:
        binary = fp.read()
    assert elf.get_binary() == binary
