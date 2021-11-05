"""
:file: pyelf_test.py
:author: Guillaume Sottas
:date: 27/06/2018
"""

import os

import pytest

from pyelf.pyelf import Address, ElfException, ElfFile

elf_files = (
    os.path.join('test_input', 'big_endian.elf'),
    os.path.join('test_input', 'little_endian.elf'))


def test_address_string_format():
    address = Address(12)
    assert str(address) == '0x0000000C'


@pytest.mark.parametrize('elf_file', elf_files)
def test_path(elf_file):
    assert ElfFile(elf_file).path == elf_file


@pytest.mark.parametrize('elf_file', elf_files)
@pytest.mark.parametrize('source_file', ('dummy_0.c',))
def test_files(elf_file, source_file):
    elf_file = ElfFile(elf_file)
    assert source_file in elf_file.files()


@pytest.mark.parametrize('elf_file', elf_files)
@pytest.mark.parametrize('symbol', ('dummy_var_no_init_uint8',
                                    'dummy_var_no_init_uint16',
                                    'dummy_var_no_init_uint32',
                                    'dummy_var_no_init_sint8',
                                    'dummy_var_no_init_sint16',
                                    'dummy_var_no_init_sint32'))
def test_symbols(elf_file, symbol):
    elf_file = ElfFile(elf_file)
    assert symbol in elf_file.symbols()


@pytest.mark.parametrize('elf_file', elf_files)
def test_get_base_address(elf_file):
    elf_file = ElfFile(elf_file)
    assert elf_file.base_address == 0x00000020


@pytest.mark.parametrize('elf_file', elf_files)
def test_get_abi_info(elf_file):
    elf_file = ElfFile(elf_file)
    abi_info = elf_file.abi_info
    assert abi_info.machine == 'EM_ARM'
    assert abi_info.version == 'EV_CURRENT'


@pytest.mark.parametrize('elf_file, expected_endianness', (
        ('big_endian.elf', 'big'),
        ('little_endian.elf', 'little')))
def test_get_endianness(elf_file, expected_endianness):
    elf_file = ElfFile(os.path.join('test_input', elf_file))
    endianness = elf_file.endianness
    assert endianness == expected_endianness


@pytest.mark.parametrize('elf_file', elf_files)
@pytest.mark.parametrize('symbol, size, address', ((
        ('dummy_var_no_init_uint8', 1, 0x08400014),
        ('dummy_var_no_init_uint16', 2, 0x0840000e),
        ('dummy_var_no_init_uint32', 4, 0x08400010),
        ('dummy_var_no_init_sint8', 1, 0x0840000c),
        ('dummy_var_no_init_sint16', 2, 0x08400004),
        ('dummy_var_no_init_sint32', 4, 0x08400008))))
def test_get_symbol(elf_file, symbol, size, address):
    elf_file = ElfFile(elf_file)
    assert elf_file.get_symbol(symbol).size == size
    assert elf_file.get_symbol(symbol).address == address


@pytest.mark.parametrize('elf_file', elf_files)
def test_get_not_existent_symbol(elf_file):
    elf_file = ElfFile(elf_file)
    with pytest.raises(ElfException):
        elf_file.get_symbol('not_valid_symbol')


@pytest.mark.parametrize('elf_file, bin_file', (
        (os.path.join('test_input', 'big_endian.elf'), os.path.join('test_input', 'big_endian.bin')),
        (os.path.join('test_input', 'little_endian.elf'), os.path.join('test_input', 'little_endian.bin'))))
def test_get_binary(elf_file, bin_file):
    elf_file = ElfFile(elf_file)
    with open(bin_file, 'rb') as fp:
        binary = fp.read()
    assert elf_file.binary == binary


@pytest.mark.parametrize('elf_file', elf_files)
@pytest.mark.parametrize('address, expected_source_file, expected_line, expected_func_name', (
        (0x30, '/usr/project/pyelf/test_input/main.c', 12, 'main'),))
def test_get_source_info(elf_file, address, expected_source_file, expected_line, expected_func_name):
    elf_file = ElfFile(elf_file)
    source_file, line, func_name = elf_file.get_source_info(address)
    assert source_file == expected_source_file
    assert line == expected_line
    assert func_name == expected_func_name
