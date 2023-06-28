"""
:file: pyelf_test.py
:author: Guillaume Sottas
:date: 27/06/2018
"""

import os

import pytest

from pyelf.parser import Address, ElfException, ElfFile, Variable

elf_files = (
    os.path.join(os.path.dirname(__file__), '..', 'tests', 'big_endian.elf'),
    os.path.join(os.path.dirname(__file__), '..', 'tests', 'little_endian.elf'))


@pytest.mark.parametrize('address, expected_string', ((-1, '-0x00000001'), (12, '0x0000000C')))
def test_address_string_format(address, expected_string):
    address = Address(address)
    assert str(address) == expected_string


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
    assert isinstance(elf_file.base_address, Address)


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
    elf_file = ElfFile(os.path.join(os.path.dirname(__file__), '..', 'tests', elf_file))
    endianness = elf_file.endianness
    assert endianness == expected_endianness


@pytest.mark.parametrize('elf_file', elf_files)
@pytest.mark.parametrize('symbol, size, address', (
        ('dummy_var_no_init_uint8', 1, 0x08400000),
        ('dummy_var_no_init_uint16', 2, 0x08400004),
        ('dummy_var_no_init_uint32', 4, 0x08400008),
        ('dummy_var_no_init_sint8', 1, 0x0840000C),
        ('dummy_var_no_init_sint16', 2, 0x08400010),
        ('dummy_var_no_init_sint32', 4, 0x08400014),
        ('dummy_struct', 520, 0x08400018),
        ('dummy_typedef_struct', 16, 0x08400220),
        ('dummy_typedef_enum', 1, 0x8400230)))
def test_get_symbol(elf_file, symbol, size, address):
    elf_file = ElfFile(elf_file)
    assert elf_file.get_symbol(symbol).size == size
    assert elf_file.get_symbol(symbol).address == address


@pytest.mark.parametrize('elf_file', [elf_files[0]])
@pytest.mark.parametrize('variable, value', (
        ('dummy_var_no_init_uint8', {
            '_type': 'Variable',
            'address': 0x08400000,
            'name': 'dummy_var_no_init_uint8',
            'type': {
                '_type': 'BaseType',
                'name': 'unsigned char',
                'size': 1
            }
        }),
        ('dummy_var_no_init_uint16', {
            '_type': 'Variable',
            'address': 0x08400004,
            'name': 'dummy_var_no_init_uint16',
            'type': {
                '_type': 'BaseType',
                'name': 'short unsigned int',
                'size': 2
            }
        }),
        ('dummy_var_no_init_uint32', {
            '_type': 'Variable',
            'address': 0x08400008,
            'name': 'dummy_var_no_init_uint32',
            'type': {
                '_type': 'BaseType',
                'name': 'unsigned int',
                'size': 4
            }
        }),
        ('dummy_var_no_init_sint8', {
            '_type': 'Variable',
            'address': 0x0840000C,
            'name': 'dummy_var_no_init_sint8',
            'type': {
                '_type': 'BaseType',
                'name': 'signed char',
                'size': 1
            }
        }),
        ('dummy_var_no_init_sint16', {
            '_type': 'Variable',
            'address': 0x08400010,
            'name': 'dummy_var_no_init_sint16',
            'type': {
                '_type': 'BaseType',
                'name': 'short int',
                'size': 2
            }
        }),
        ('dummy_var_no_init_sint32', {
            '_type': 'Variable',
            'address': 0x08400014,
            'name': 'dummy_var_no_init_sint32',
            'type': {
                '_type': 'BaseType',
                'name': 'int',
                'size': 4
            }
        }),
        ('dummy_struct', {
            '_type': 'Variable',
            'name': 'dummy_struct',
            'address': 138412056,
            'type': {
                '_type': 'Structure',
                'name': 'dummy_struct_type',
                'size': 520,
                'fields': [
                    {
                        '_type': 'Field',
                        'name': 'field_uint8',
                        'offset': 0,
                        'bit_offset': None,
                        'bit_size': None,
                        'type': {
                            '_type': 'BaseType',
                            'name': 'unsigned char',
                            'size': 1
                        }
                    },
                    {
                        '_type': 'Field',
                        'name': 'field_uint16',
                        'offset': 2,
                        'bit_offset': None,
                        'bit_size': None,
                        'type': {
                            '_type': 'BaseType',
                            'name': 'short unsigned int',
                            'size': 2
                        }
                    },
                    {
                        '_type': 'Field',
                        'name': 'field_uint32',
                        'offset': 4,
                        'bit_offset': None,
                        'bit_size': None,
                        'type': {
                            '_type': 'BaseType',
                            'name': 'unsigned int',
                            'size': 4
                        }
                    },
                    {
                        '_type': 'Field',
                        'name': 'field_int8',
                        'offset': 8,
                        'bit_offset': None,
                        'bit_size': None,
                        'type': {
                            '_type': 'BaseType',
                            'name': 'signed char',
                            'size': 1
                        }
                    },
                    {
                        '_type': 'Field',
                        'name': 'field_int16',
                        'offset': 10,
                        'bit_offset': None,
                        'bit_size': None,
                        'type': {
                            '_type': 'BaseType',
                            'name': 'short int',
                            'size': 2
                        }
                    },
                    {
                        '_type': 'Field',
                        'name': 'field_int32',
                        'offset': 12,
                        'bit_offset': None,
                        'bit_size': None,
                        'type': {
                            '_type': 'BaseType',
                            'name': 'int',
                            'size': 4
                        }
                    },
                    {
                        '_type': 'Field',
                        'name': 'field_u8',
                        'offset': 16,
                        'bit_offset': None,
                        'bit_size': None,
                        'type': {
                            '_type': 'TypedefType',
                            'name': 'u8',
                            'type': {
                                '_type': 'BaseType',
                                'name': 'unsigned char',
                                'size': 1
                            }
                        }
                    },
                    {
                        '_type': 'Field',
                        'name': 'field_u16',
                        'offset': 18,
                        'bit_offset': None,
                        'bit_size': None,
                        'type': {
                            '_type': 'TypedefType',
                            'name': 'u16',
                            'type': {
                                '_type': 'BaseType',
                                'name': 'short unsigned int',
                                'size': 2
                            }
                        }
                    },
                    {
                        '_type': 'Field',
                        'name': 'field_u32',
                        'offset': 20,
                        'bit_offset': None,
                        'bit_size': None,
                        'type': {
                            '_type': 'TypedefType',
                            'name': 'u32',
                            'type': {
                                '_type': 'BaseType',
                                'name': 'unsigned int',
                                'size': 4
                            }
                        }
                    },
                    {
                        '_type': 'Field',
                        'name': 'field_s8',
                        'offset': 24,
                        'bit_offset': None,
                        'bit_size': None,
                        'type': {
                            '_type': 'TypedefType',
                            'name': 's8',
                            'type': {
                                '_type': 'BaseType',
                                'name': 'signed char',
                                'size': 1
                            }
                        }
                    },
                    {
                        '_type': 'Field',
                        'name': 'field_s16',
                        'offset': 26,
                        'bit_offset': None,
                        'bit_size': None,
                        'type': {
                            '_type': 'TypedefType',
                            'name': 's16',
                            'type': {
                                '_type': 'BaseType',
                                'name': 'short int',
                                'size': 2
                            }
                        }
                    },
                    {
                        '_type': 'Field',
                        'name': 'field_s32',
                        'offset': 28,
                        'bit_offset': None,
                        'bit_size': None,
                        'type': {
                            '_type': 'TypedefType',
                            'name': 's32',
                            'type': {
                                '_type': 'BaseType',
                                'name': 'int',
                                'size': 4
                            }
                        }
                    },
                    {
                        '_type': 'Field',
                        'name': 'bit_field_0_size_1',
                        'offset': 32,
                        'bit_offset': 0,
                        'bit_size': 1,
                        'type': {
                            '_type': 'BaseType',
                            'name': 'short unsigned int',
                            'size': 2
                        }
                    },
                    {
                        '_type': 'Field',
                        'name': 'bit_field_1_size_2',
                        'offset': 32,
                        'bit_offset': 1,
                        'bit_size': 2,
                        'type': {
                            '_type': 'BaseType',
                            'name': 'short unsigned int',
                            'size': 2
                        }
                    },
                    {
                        '_type': 'Field',
                        'name': 'bit_field_2_size_3',
                        'offset': 32,
                        'bit_offset': 3,
                        'bit_size': 3,
                        'type': {
                            '_type': 'BaseType',
                            'name': 'short unsigned int',
                            'size': 2
                        }
                    },
                    {
                        '_type': 'Field',
                        'name': 'bit_field_3_size_4',
                        'offset': 32,
                        'bit_offset': 6,
                        'bit_size': 4,
                        'type': {
                            '_type': 'BaseType',
                            'name': 'short unsigned int',
                            'size': 2
                        }
                    },
                    {
                        '_type': 'Field',
                        'name': 'bit_field_4_size_6',
                        'offset': 32,
                        'bit_offset': 10,
                        'bit_size': 6,
                        'type': {
                            '_type': 'BaseType',
                            'name': 'short unsigned int',
                            'size': 2
                        }
                    },
                    {
                        '_type': 'Field',
                        'name': 'anonymous_639',
                        'offset': 36,
                        'bit_offset': None,
                        'bit_size': None,
                        'type': {
                            '_type': 'Structure',
                            'name': 'anonymous_359',
                            'size': 484, 'fields': [
                                {
                                    '_type': 'Field',
                                    'name': 'field_uint8_nesting_0',
                                    'offset': 0,
                                    'bit_offset': None,
                                    'bit_size': None,
                                    'type': {
                                        '_type': 'BaseType',
                                        'name': 'unsigned int',
                                        'size': 4
                                    }
                                },
                                {
                                    '_type': 'Field',
                                    'name': 'anonymous_382',
                                    'offset': 4,
                                    'bit_offset': None,
                                    'bit_size': None,
                                    'type': {
                                        '_type': 'Structure',
                                        'name': 'anonymous_295',
                                        'size': 480, 'fields': [
                                            {
                                                '_type': 'Field',
                                                'name': 'field_uint16_nesting_1',
                                                'offset': 0,
                                                'bit_offset': None,
                                                'bit_size': None,
                                                'type': {
                                                    '_type': 'Array',
                                                    'name': 'anonymous_319',
                                                    'type': {
                                                        '_type': 'BaseType',
                                                        'name': 'int',
                                                        'size': 4},
                                                    'dimension': [
                                                        4,
                                                        3,
                                                        2,
                                                        1,
                                                        0]
                                                }
                                            }
                                        ]
                                    }
                                }
                            ]
                        }
                    }
                ]
            }
        }),
        ('dummy_typedef_enum', {
            '_type': 'Variable',
            'address': 138412592,
            'name': 'dummy_typedef_enum',
            'type': {
                '_type': 'TypedefType',
                'name': 'dummy_typedef_enum_type',
                'type': {
                    '_type': 'BaseType',
                    'name': 'unsigned char',
                    'size': 1
                }
            }
        })
))
def test_get_variable_json_big_endian(elf_file, variable, value):
    elf_file = ElfFile(elf_file)
    assert elf_file.get_variable(variable).to_json() == value


@pytest.mark.parametrize('elf_file', [elf_files[1]])
@pytest.mark.parametrize('variable, value', (
        ('dummy_var_no_init_uint8', {
            '_type': 'Variable',
            'address': 0x08400000,
            'name': 'dummy_var_no_init_uint8',
            'type': {
                '_type': 'BaseType',
                'name': 'unsigned char',
                'size': 1
            }
        }),
        ('dummy_var_no_init_uint16', {
            '_type': 'Variable',
            'address': 0x08400004,
            'name': 'dummy_var_no_init_uint16',
            'type': {
                '_type': 'BaseType',
                'name': 'short unsigned int',
                'size': 2
            }
        }),
        ('dummy_var_no_init_uint32', {
            '_type': 'Variable',
            'address': 0x08400008,
            'name': 'dummy_var_no_init_uint32',
            'type': {
                '_type': 'BaseType',
                'name': 'unsigned int',
                'size': 4
            }
        }),
        ('dummy_var_no_init_sint8', {
            '_type': 'Variable',
            'address': 0x0840000C,
            'name': 'dummy_var_no_init_sint8',
            'type': {
                '_type': 'BaseType',
                'name': 'signed char',
                'size': 1
            }
        }),
        ('dummy_var_no_init_sint16', {
            '_type': 'Variable',
            'address': 0x08400010,
            'name': 'dummy_var_no_init_sint16',
            'type': {
                '_type': 'BaseType',
                'name': 'short int',
                'size': 2
            }
        }),
        ('dummy_var_no_init_sint32', {
            '_type': 'Variable',
            'address': 0x08400014,
            'name': 'dummy_var_no_init_sint32',
            'type': {
                '_type': 'BaseType',
                'name': 'int',
                'size': 4
            }
        }),
        ('dummy_struct', {
            '_type': 'Variable',
            'name': 'dummy_struct',
            'address': 138412056,
            'type': {
                '_type': 'Structure',
                'name': 'dummy_struct_type',
                'size': 520,
                'fields': [
                    {
                        '_type': 'Field',
                        'name': 'field_uint8',
                        'offset': 0,
                        'bit_offset': None,
                        'bit_size': None,
                        'type': {
                            '_type': 'BaseType',
                            'name': 'unsigned char',
                            'size': 1
                        }
                    },
                    {
                        '_type': 'Field',
                        'name': 'field_uint16',
                        'offset': 2,
                        'bit_offset': None,
                        'bit_size': None,
                        'type': {
                            '_type': 'BaseType',
                            'name': 'short unsigned int',
                            'size': 2
                        }
                    },
                    {
                        '_type': 'Field',
                        'name': 'field_uint32',
                        'offset': 4,
                        'bit_offset': None,
                        'bit_size': None,
                        'type': {
                            '_type': 'BaseType',
                            'name': 'unsigned int',
                            'size': 4
                        }
                    },
                    {
                        '_type': 'Field',
                        'name': 'field_int8',
                        'offset': 8,
                        'bit_offset': None,
                        'bit_size': None,
                        'type': {
                            '_type': 'BaseType',
                            'name': 'signed char',
                            'size': 1
                        }
                    },
                    {
                        '_type': 'Field',
                        'name': 'field_int16',
                        'offset': 10,
                        'bit_offset': None,
                        'bit_size': None,
                        'type': {
                            '_type': 'BaseType',
                            'name': 'short int',
                            'size': 2
                        }
                    },
                    {
                        '_type': 'Field',
                        'name': 'field_int32',
                        'offset': 12,
                        'bit_offset': None,
                        'bit_size': None,
                        'type': {
                            '_type': 'BaseType',
                            'name': 'int',
                            'size': 4
                        }
                    },
                    {
                        '_type': 'Field',
                        'name': 'field_u8',
                        'offset': 16,
                        'bit_offset': None,
                        'bit_size': None,
                        'type': {
                            '_type': 'TypedefType',
                            'name': 'u8',
                            'type': {
                                '_type': 'BaseType',
                                'name': 'unsigned char',
                                'size': 1
                            }
                        }
                    },
                    {
                        '_type': 'Field',
                        'name': 'field_u16',
                        'offset': 18,
                        'bit_offset': None,
                        'bit_size': None,
                        'type': {
                            '_type': 'TypedefType',
                            'name': 'u16',
                            'type': {
                                '_type': 'BaseType',
                                'name': 'short unsigned int',
                                'size': 2
                            }
                        }
                    },
                    {
                        '_type': 'Field',
                        'name': 'field_u32',
                        'offset': 20,
                        'bit_offset': None,
                        'bit_size': None,
                        'type': {
                            '_type': 'TypedefType',
                            'name': 'u32',
                            'type': {
                                '_type': 'BaseType',
                                'name': 'unsigned int',
                                'size': 4
                            }
                        }
                    },
                    {
                        '_type': 'Field',
                        'name': 'field_s8',
                        'offset': 24,
                        'bit_offset': None,
                        'bit_size': None,
                        'type': {
                            '_type': 'TypedefType',
                            'name': 's8',
                            'type': {
                                '_type': 'BaseType',
                                'name': 'signed char',
                                'size': 1
                            }
                        }
                    },
                    {
                        '_type': 'Field',
                        'name': 'field_s16',
                        'offset': 26,
                        'bit_offset': None,
                        'bit_size': None,
                        'type': {
                            '_type': 'TypedefType',
                            'name': 's16',
                            'type': {
                                '_type': 'BaseType',
                                'name': 'short int',
                                'size': 2
                            }
                        }
                    },
                    {
                        '_type': 'Field',
                        'name': 'field_s32',
                        'offset': 28,
                        'bit_offset': None,
                        'bit_size': None,
                        'type': {
                            '_type': 'TypedefType',
                            'name': 's32',
                            'type': {
                                '_type': 'BaseType',
                                'name': 'int',
                                'size': 4
                            }
                        }
                    },
                    {
                        '_type': 'Field',
                        'name': 'bit_field_0_size_1',
                        'offset': 32,
                        'bit_offset': 15,
                        'bit_size': 1,
                        'type': {
                            '_type': 'BaseType',
                            'name': 'short unsigned int',
                            'size': 2
                        }
                    },
                    {
                        '_type': 'Field',
                        'name': 'bit_field_1_size_2',
                        'offset': 32,
                        'bit_offset': 13,
                        'bit_size': 2,
                        'type': {
                            '_type': 'BaseType',
                            'name': 'short unsigned int',
                            'size': 2
                        }
                    },
                    {
                        '_type': 'Field',
                        'name': 'bit_field_2_size_3',
                        'offset': 32,
                        'bit_offset': 10,
                        'bit_size': 3,
                        'type': {
                            '_type': 'BaseType',
                            'name': 'short unsigned int',
                            'size': 2
                        }
                    },
                    {
                        '_type': 'Field',
                        'name': 'bit_field_3_size_4',
                        'offset': 32,
                        'bit_offset': 6,
                        'bit_size': 4,
                        'type': {
                            '_type': 'BaseType',
                            'name': 'short unsigned int',
                            'size': 2
                        }
                    },
                    {
                        '_type': 'Field',
                        'name': 'bit_field_4_size_6',
                        'offset': 32,
                        'bit_offset': 0,
                        'bit_size': 6,
                        'type': {
                            '_type': 'BaseType',
                            'name': 'short unsigned int',
                            'size': 2
                        }
                    },
                    {
                        '_type': 'Field',
                        'name': 'anonymous_639',
                        'offset': 36,
                        'bit_offset': None,
                        'bit_size': None,
                        'type': {
                            '_type': 'Structure',
                            'name': 'anonymous_359',
                            'size': 484, 'fields': [
                                {
                                    '_type': 'Field',
                                    'name': 'field_uint8_nesting_0',
                                    'offset': 0,
                                    'bit_offset': None,
                                    'bit_size': None,
                                    'type': {
                                        '_type': 'BaseType',
                                        'name': 'unsigned int',
                                        'size': 4
                                    }
                                },
                                {
                                    '_type': 'Field',
                                    'name': 'anonymous_382',
                                    'offset': 4,
                                    'bit_offset': None,
                                    'bit_size': None,
                                    'type': {
                                        '_type': 'Structure',
                                        'name': 'anonymous_295',
                                        'size': 480, 'fields': [
                                            {
                                                '_type': 'Field',
                                                'name': 'field_uint16_nesting_1',
                                                'offset': 0,
                                                'bit_offset': None,
                                                'bit_size': None,
                                                'type': {
                                                    '_type': 'Array',
                                                    'name': 'anonymous_319',
                                                    'type': {
                                                        '_type': 'BaseType',
                                                        'name': 'int',
                                                        'size': 4},
                                                    'dimension': [
                                                        4,
                                                        3,
                                                        2,
                                                        1,
                                                        0]
                                                }
                                            }
                                        ]
                                    }
                                }
                            ]
                        }
                    }
                ]
            }
        }),
        ('dummy_typedef_enum', {
            '_type': 'Variable',
            'address': 138412592,
            'name': 'dummy_typedef_enum',
            'type': {
                '_type': 'TypedefType',
                'name': 'dummy_typedef_enum_type',
                'type': {
                    '_type': 'BaseType',
                    'name': 'unsigned char',
                    'size': 1
                }
            }
        })
))
def test_get_variable_json_little_endian(elf_file, variable, value):
    elf_file = ElfFile(elf_file)
    assert elf_file.get_variable(variable).to_json() == value


@pytest.mark.parametrize('elf_file', elf_files)
def test_get_not_existent_symbol(elf_file):
    elf_file = ElfFile(elf_file)
    with pytest.raises(ElfException):
        elf_file.get_symbol('not_valid_symbol')


@pytest.mark.parametrize('elf_file', elf_files)
def test_get_binary_address(elf_file):
    elf_file = ElfFile(elf_file)
    assert elf_file.binary_address == 0x00000000


@pytest.mark.parametrize('elf_file, bin_file', (
        (os.path.join(os.path.dirname(__file__), '..', 'tests', 'big_endian.elf'),
         os.path.join(os.path.dirname(__file__), '..', 'tests', 'big_endian.bin')),
        (os.path.join(os.path.dirname(__file__), '..', 'tests', 'little_endian.elf'),
         os.path.join(os.path.dirname(__file__), '..', 'tests', 'little_endian.bin'))))
def test_get_binary(elf_file, bin_file):
    elf_file = ElfFile(elf_file)
    with open(bin_file, 'rb') as fp:
        binary = fp.read()
    assert elf_file.binary == binary


@pytest.mark.parametrize('elf_file', elf_files)
@pytest.mark.parametrize('address, expected_source_file, expected_line, expected_func_name', (
        (0x00000030, os.path.abspath(os.path.join(os.path.dirname(__file__), '../tests', 'main.c')), 78, 'main'),))
def test_get_source_info(elf_file, address, expected_source_file, expected_line, expected_func_name):
    elf_file = ElfFile(elf_file)
    source_file, line, func_name = elf_file.get_source_info(address)
    assert source_file == expected_source_file
    assert line == expected_line
    assert func_name == expected_func_name
