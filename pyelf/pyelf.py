"""
:file: pyelf.py
:author: Guillaume Sottas
:date: 27/06/2018
"""

from elftools.elf.elffile import ELFFile
from elftools.elf.sections import SymbolTableSection, SUNWSyminfoTableSection
from elftools.elf.sections import Symbol as ElfSymbol


class Address(int):
    def __str__(self):
        return '0x{0:08X}'.format(self)


class Symbol(ElfSymbol):
    def size(self):
        return self.entry.st_size

    def address(self):
        return self.entry.st_value


class ElfException(Exception):
    pass


class ElfFile(ELFFile):
    def __init__(self, path):
        fp = open(path, 'rb')
        super(ElfFile, self).__init__(stream=fp)
        self._symbols = dict()
        for section in self.iter_sections():
            if isinstance(section, SymbolTableSection) or isinstance(section, SUNWSyminfoTableSection):
                for sym in section.iter_symbols():
                    self._symbols[sym.name] = sym.entry

    def path(self):
        """
        returns the full path of the file the current instance is getting information from.
        :return: string
        """
        return self.stream.name

    def files(self):
        """returns a list of strings containing all source files in the ELF file."""
        return [k for k, v in self._symbols.items() if
                hasattr(v, 'st_info') and v.st_info.type == 'STT_FILE']

    def symbols(self):
        """
        returns a list of strings containing all symbols available in the ELF file.
        :return: list of strings
        """
        return [k for k, v in self._symbols.items() if
                hasattr(v, 'st_info') and v.st_info.type == 'STT_OBJECT']

    def get_base_address(self):
        """
        returns the address of the first instruction in the ELF file.
        :return: Address
        """
        for segment in self.iter_segments():
            if segment['p_type'] == 'PT_LOAD':
                return Address(segment['p_paddr'])

    def get_symbol(self, name):
        """
        returns a Symbol object containing the properties of the symbol named 'name' in the ELF file.
        :param name: symbol name as string
        :return: Symbol
        """
        if name in self._symbols.keys():
            return Symbol(self._symbols[name], name)
        raise ElfException('symbol ' + str(name) + ' not found')

    def get_binary(self):
        """
        returns the binary from the ELF file.
        :return: list of pyhon bytes
        """
        data = b''
        for segment in self.iter_segments():
            if segment['p_type'] == 'PT_LOAD':
                data += segment.data()
        return data
