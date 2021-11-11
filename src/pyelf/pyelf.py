"""
:file: pyelf.py
:author: Guillaume Sottas
:date: 27/06/2018
"""

from elftools.common.exceptions import DWARFError
from elftools.dwarf.descriptions import describe_form_class
from elftools.elf.elffile import ELFFile
from elftools.elf.sections import Symbol as ElfSymbol
from elftools.elf.sections import SymbolTableSection, SUNWSyminfoTableSection


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
        return self.header.e_entry

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

    def get_source_info(self, address):
        """
        returns the full path to the source file containing the code for the specified address, as well as the line
        number (1-based), and the function name (if in a function).

        :param address: requested address
        :type address: int
        :return: a tuple containing the source file path, the source file line (1-based) and the function name (None if
        not in a function)
        :rtype: tuple
        """
        file_path, line, func_name = None, -1, None
        line = -1
        func_name = None
        dwarf_info = self.get_dwarf_info()
        for CU in dwarf_info.iter_CUs():
            try:
                line_program = dwarf_info.line_program_for_CU(CU)
            except DWARFError:
                continue
            if line_program is None:
                continue
            prev_state = None
            if line == -1:
                for entry in line_program.get_entries():
                    if entry.state is None:
                        continue
                    if prev_state and prev_state.address <= address < entry.state.address:
                        file_path = CU.get_top_DIE().get_full_path()
                        line = prev_state.line
                    if entry.state.end_sequence:
                        prev_state = None
                    else:
                        prev_state = entry.state
            if func_name is None:
                for DIE in CU.iter_DIEs():
                    try:
                        if DIE.tag == 'DW_TAG_subprogram':
                            low_pc = DIE.attributes['DW_AT_low_pc'].value
                            high_pc_attr = DIE.attributes['DW_AT_high_pc']
                            high_pc_attr_class = describe_form_class(high_pc_attr.form)
                            if high_pc_attr_class == 'address':
                                high_pc = high_pc_attr.value
                            elif high_pc_attr_class == 'constant':
                                high_pc = low_pc + high_pc_attr.value
                            else:
                                continue
                            if low_pc <= address < high_pc:
                                func_name = DIE.attributes['DW_AT_name'].value.decode()
                                break
                    except KeyError:
                        continue
                if func_name is not None:
                    break
        return file_path, line - 1 if line != -1 else -1, func_name
