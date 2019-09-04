"""
:file: pyelf.py
:author: Guillaume Sottas
:date: 27/06/2018
"""

from elftools.elf.elffile import ELFFile
from elftools.elf.sections import SymbolTableSection, SUNWSyminfoTableSection
from elftools.elf.sections import Symbol as ElfSymbol


class Address(int):
    """
    represents an address.
    """

    def __str__(self):
        return '0x{0:08X}'.format(self)


class Symbol(ElfSymbol):
    """
    represents a symbol.
    """

    @property
    def size(self):
        """
        returns the size of the symbol.

        :return: size in [byte]
        :rtype: int
        """
        return self.entry.st_size

    @property
    def address(self):
        """
        returns the address of the symbol.

        :return: address
        :rtype: int
        """
        return self.entry.st_value


class AbiInfo(object):
    """
    represents the header of the file.
    """

    def __init__(self, e_machine=None, e_version=None, *args, **kwargs):
        self.machine = e_machine
        self.version = e_version

    def get_machine(self):
        return self._machine

    def set_machine(self, value):
        self._machine = value

    def get_version(self):
        return self._version

    def set_version(self, value):
        self._version = value

    machine = property(fget=get_machine, fset=set_machine)
    version = property(fget=get_version, fset=set_version)


class ElfException(Exception):
    pass


class ElfFile(ELFFile):
    """

    """

    def __init__(self, path):
        fp = open(path, 'rb')
        super(ElfFile, self).__init__(stream=fp)
        self.path = self.stream.name
        self.endianness = self.little_endian
        self._symbols = dict()
        for section in self.iter_sections():
            if isinstance(section, SymbolTableSection) or isinstance(section, SUNWSyminfoTableSection):
                for sym in section.iter_symbols():
                    self._symbols[sym.name] = sym.entry

    @property
    def abi_info(self):
        """
        returns the ABI information.
        :return: ABI information
        :rtype: AbiInfo
        """
        return AbiInfo(**dict((k, self.header[k]) for k in ('e_machine', 'e_version')))

    @property
    def base_address(self):
        """
        returns the address of the first instruction in the ELF file.

        :return: first instruction's address
        :rtype: Address
        """
        for segment in self.iter_segments():
            if segment['p_type'] == 'PT_LOAD':
                return Address(segment['p_paddr'])

    @property
    def binary(self):
        """
        returns the binary from the ELF file.
        :return: binary data
        :rtype: bytearray
        """
        data = b''
        for segment in self.iter_segments():
            if segment['p_type'] == 'PT_LOAD':
                data += segment.data()
        return data

    @property
    def endianness(self):
        """
        endianness of the binary.

        :getter: returns the endianness of the binary
        :setter: sets the endianness of the binary
        :type: str
        """
        return self._endianness

    @endianness.setter
    def endianness(self, value):
        if value:
            self._endianness = 'little'
        else:
            self._endianness = 'big'

    def files(self):
        """
        returns an iterator containing all source files in the ELF file.

        :return: list of file name
        :rtype: list
        """
        return (k for k, v in self._symbols.items() if hasattr(v, 'st_info') and v.st_info.type == 'STT_FILE')

    @property
    def path(self):
        """
        returns the full path of the elf file.

        :return: path
        :rtype: str
        """
        return self._path

    @path.setter
    def path(self, value):
        self._path = value

    def symbols(self):
        """
        returns a list of all symbols available in the ELF file.

        :return: list of symbols
        :rtype: list
        """
        return [k for k, v in self._symbols.items() if
                hasattr(v, 'st_info') and v.st_info.type == 'STT_OBJECT']

    def get_symbol(self, name):
        """
        returns a Symbol object containing the properties of the symbol named 'name' in the ELF file.

        :param name: symbol name
        :type name: str
        :return: symbol
        :rtype: Symbol
        """
        if name in self._symbols.keys():
            return Symbol(self._symbols[name], name)
        raise ElfException('symbol ' + str(name) + ' not found')
