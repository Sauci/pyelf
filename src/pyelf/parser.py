"""
:file: pyelf.py
:author: Guillaume Sottas
:date: 27/06/2018
"""
import abc
import typing

from elftools.common.exceptions import DWARFError
from elftools.dwarf.descriptions import describe_form_class
from elftools.elf.elffile import ELFFile as ELF
from elftools.elf.sections import Symbol as ElfSymbol
from elftools.dwarf.die import DIE


class Address(int):
    """
    represents an address.
    """

    def __str__(self):
        return '{0}0x{1:08X}'.format('-' if self < 0 else '', abs(self))


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


class NamedProperty(abc.ABC):
    def __init__(self, name: str):
        self._name = name

    @property
    def name(self):
        return self._name


class TypedProperty(NamedProperty):
    def __init__(self, name: str, type_name: str, parent):
        super().__init__(name)
        self._type_name = type_name
        self._parent = parent

    @property
    def type(self):
        return self._parent.get_type_from_type_name(self._type_name)


class BaseType(NamedProperty):
    def __init__(self, name: str, size: int):
        super().__init__(name)
        self._size = size

    @property
    def size(self):
        return self._size

    def to_json(self):
        return dict(_type=self.__class__.__name__, name=self.name, size=self.size)


class TypedefType(TypedProperty):
    def __init__(self, name: str, type_name: str, parent):
        super().__init__(name, type_name, parent)

    def to_json(self):
        return dict(_type=self.__class__.__name__, name=self.name, type=self.type.to_json())


class Union(NamedProperty):
    class Member(TypedProperty):
        def __init__(self, name: str, type_name: str, parent):
            super().__init__(name, type_name, parent)

        def to_json(self):
            return dict(_type=self.__class__.__name__, name=self.name, type=self.type.to_json())

    def __init__(self, name: str, size: int, members: typing.Tuple[Member]):
        super().__init__(name)
        self._size = size
        self._members = members

    @property
    def size(self):
        return self._size

    @property
    def members(self):
        return self._members

    def to_json(self):
        return dict(_type=self.__class__.__name__, name=self.name, size=self.size, members=[m.to_json() for m in self.members])


class Structure(NamedProperty):
    class Field(TypedProperty):
        def __init__(self,
                     name: str,
                     type_name: str,
                     parent,
                     offset: int,
                     bit_offset: typing.Union[int, None] = None,
                     bit_size: typing.Union[int, None] = None):
            super().__init__(name, type_name, parent)
            self._offset = offset
            self._bit_offset = bit_offset
            self._bit_size = bit_size

        @property
        def offset(self):
            return self._offset

        @property
        def bit_offset(self):
            return self._bit_offset

        @property
        def bit_size(self):
            return self._bit_size

        def to_json(self):
            try:
                return dict(_type=self.__class__.__name__,
                            name=self.name,
                            offset=self.offset,
                            bit_offset=self.bit_offset,
                            bit_size=self.bit_size,
                            type=self.type.to_json())
            except AttributeError as e:
                return None

    """
    represents a structure.
    """

    def __init__(self, name: str, size: int, fields: typing.Tuple[Field]):
        super().__init__(name)
        self._size = size
        self._fields = fields

    @property
    def size(self):
        return self._size

    @property
    def fields(self):
        return self._fields

    def to_json(self):
        return dict(_type=self.__class__.__name__,
                    name=self.name,
                    size=self.size,
                    fields=[m.to_json() for m in self.fields])


class Enumeration(NamedProperty):
    class Enumerator(NamedProperty):
        def __init__(self, name: str, value: int):
            super().__init__(name)
            self._value = value

        @property
        def value(self):
            return self._value

        def to_json(self):
            return dict(_type=self.__class__.__name__, name=self.name, value=self.value)

    def __init__(self, name: str, size: int, enumerators: typing.Tuple[Enumerator]):
        super().__init__(name)
        self._size = size
        self._enumerators = enumerators

    @property
    def size(self):
        return self._size

    @property
    def enumerators(self):
        return self._enumerators

    def to_json(self):
        return dict(_type=self.__class__.__name__,
                    name=self.name,
                    size=self.size,
                    enumerators=[e.to_json() for e in self.enumerators])


class Array(TypedProperty):
    def __init__(self, name: str, type_name: str, parent, dimension: typing.List[int]):
        super().__init__(name, type_name, parent)
        self._dimension = dimension

    @property
    def dimension(self):
        return self._dimension

    def to_json(self):
        return dict(_type=self.__class__.__name__, name=self.name, type=self.type.to_json(), dimension=self.dimension)


class Variable(TypedProperty):
    """
    represents a variable.
    """

    def __init__(self, name: str, type_name: str, parent, address: int):
        super().__init__(name, type_name, parent)
        self._address = address

    @property
    def address(self) -> int:
        return self._address

    def to_json(self):
        return dict(_type=self.__class__.__name__, name=self.name, address=self.address, type=self.type.to_json())


class Pointer(TypedProperty):
    def __init__(self, name, type_name: str, parent):
        super().__init__(name, type_name, parent)

    def to_json(self):
        return dict(_type=self.__class__.__name__, name=self.name, type=self.type.to_json())


class Constant(TypedProperty):
    def __init__(self, name: str, type_name: str, parent):
        super().__init__(name, type_name, parent)

    def to_json(self):
        return dict(_type=self.__class__.__name__, name=self.name, type=self.type.to_json())


class SubRoutine(object):
    def __init__(self, name: str):
        self._name = name

    @property
    def name(self):
        return self._name

    def to_json(self):
        return dict(_type=self.__class__.__name__, name=self.name)


class AbiInfo(object):
    """
    represents the header of the file.
    """

    def __init__(self, e_machine=None, e_version=None, *_args, **_kwargs):
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


class ElfFile(ELF):
    """

    """

    def __init__(self, path):
        fp = open(path, 'rb')
        super(ElfFile, self).__init__(stream=fp)
        self.path = self.stream.name
        self.endianness = self.little_endian
        self._symbols = dict()
        self._type_definitions = dict()
        self._base_types = dict()
        self._enumerations = dict()
        self._structures = dict()
        self._unions = dict()
        self._pointers = dict()
        self._arrays = dict()
        self._variables = dict()
        self._sub_routines = dict()
        self._constants = dict()
        for section in self.iter_sections():
            if hasattr(section, 'iter_symbols'):
                for sym in section.iter_symbols():
                    self._symbols[sym.name] = sym.entry
        for cu in self.get_dwarf_info().iter_CUs():
            iter_dies = cu.iter_DIEs()
            for die in iter_dies:
                # if die.offset == 303421:
                #     print(die)
                if die.tag:
                    self._factory(die.tag, die, iter_dies)

    def _factory(self, tag: typing.Union[str, None], die: DIE, die_iterator: typing.Iterator[DIE]):
        try:
            fcn = dict(DW_TAG_typedef=self._create_type_definition,
                       DW_TAG_base_type=self._create_base_type,
                       DW_TAG_enumeration_type=self._create_enumeration_type,
                       DW_TAG_structure_type=self._create_structure_type,
                       DW_TAG_union_type=self._create_union_type,
                       DW_TAG_pointer_type=self._create_pointer_type,
                       DW_TAG_variable=self._create_variable,
                       DW_TAG_const_type=self._create_const_type,
                       DW_TAG_array_type=self._create_array_type,
                       DW_TAG_subroutine_type=self._create_subroutine_type,
                       DW_TAG_volatile_type=self._unhandled_type,
                       DW_TAG_subprogram=self._unhandled_type,
                       DW_TAG_formal_parameter=self._unhandled_type,
                       DW_TAG_lexical_block=self._unhandled_type,
                       DW_TAG_compile_unit=self._unhandled_type)[tag]
        except KeyError as e:
            print(f'{e} | {die.get_parent()}')
            return None
        else:
            return fcn(die, die_iterator)

    @staticmethod
    def _get_element_name_from_die(die: DIE) -> str:
        if 'DW_AT_name' in die.attributes.keys():
            name = die.attributes['DW_AT_name'].value.decode()
        else:
            name = 'anonymous_{}'.format(die.offset)
        return name

    @staticmethod
    def _get_element_type_name_from_die(die: DIE) -> str:
        # if 'DW_AT_name' in die.attributes.keys():
        #     type_name = die.attributes['DW_AT_name'].value.decode()
        # else:
        t = die.get_DIE_from_attribute('DW_AT_type')
        if t.tag in ('DW_TAG_array_type', 'DW_TAG_pointer_type', 'DW_TAG_const_type'):
            type_name = f'anonymous_{t.offset}'
        else:
            while 'DW_AT_name' not in t.attributes.keys() and 'DW_AT_type' in t.attributes.keys():
                t = t.get_DIE_from_attribute('DW_AT_type')
            if 'DW_AT_name' in t.attributes.keys():
                type_name = t.attributes['DW_AT_name'].value.decode()
            else:
                type_name = f'anonymous_{t.offset}'
        return type_name

    @staticmethod
    def _unhandled_type(_die: DIE, _die_iterator: typing.Iterator[DIE]):
        pass

    def _create_subroutine_type(self, die: DIE, die_iterator: typing.Iterator[DIE]):
        name = self._get_element_name_from_die(die)
        next_die = next(die_iterator)
        while next_die.tag is not None:
            next_die = next(die_iterator)
        self._sub_routines[name] = SubRoutine(name)

    def _create_type_definition(self, die: DIE, _: typing.Iterator[DIE]):
        name = self._get_element_name_from_die(die)
        type_name = self._get_element_type_name_from_die(die)
        self._type_definitions[name] = TypedefType(name, type_name, self)

    def _create_base_type(self, die: DIE, _: typing.Iterator[DIE]):
        name = self._get_element_name_from_die(die)
        size = die.attributes['DW_AT_byte_size'].value
        self._base_types[name] = BaseType(name, size)

    def _create_enumeration_type(self, die: DIE, die_iterator: typing.Iterator[DIE]):
        name = self._get_element_name_from_die(die)
        size = die.attributes['DW_AT_byte_size'].value
        # type_name = die.get_DIE_from_attribute('DW_AT_type').attributes['DW_AT_name'].value.decode()
        next_die = next(die_iterator)
        enumerators = list()
        while next_die.tag == "DW_TAG_enumerator":
            enumerators.append(Enumeration.Enumerator(next_die.attributes['DW_AT_name'].value.decode(),
                                                      next_die.attributes['DW_AT_const_value'].value))
            next_die = next(die_iterator)
        self._enumerations[name] = Enumeration(name, size, tuple(enumerators))

    def _create_structure_type(self, die: DIE, die_iterator: typing.Iterator[DIE]):
        name = self._get_element_name_from_die(die)
        if 'DW_AT_byte_size' in die.attributes.keys():
            size = die.attributes['DW_AT_byte_size'].value
        else:
            size = 0
        fields = list()
        next_die = next(die_iterator)
        while next_die.tag == 'DW_TAG_member':
            field_name = self._get_element_name_from_die(next_die)
            field_type_name = self._get_element_type_name_from_die(next_die)
            field_offset = self.get_location_from_attribute(next_die.attributes['DW_AT_data_member_location'])
            field_bit_offset = None
            if 'DW_AT_bit_offset' in next_die.attributes.keys():
                field_bit_offset = next_die.attributes['DW_AT_bit_offset'].value
            field_bit_size = None
            if 'DW_AT_bit_size' in next_die.attributes.keys():
                field_bit_size = next_die.attributes['DW_AT_bit_size'].value
            fields.append(Structure.Field(field_name, field_type_name, self, field_offset, field_bit_offset,
                                          field_bit_size))
            next_die = next(die_iterator)
        self._structures[name] = Structure(name, size, tuple(fields))

    def _create_union_type(self, die: DIE, die_iterator: typing.Iterator[DIE]):
        name = self._get_element_name_from_die(die)
        members = list()
        next_die = next(die_iterator)
        while next_die.tag == 'DW_TAG_member':
            member_name = self._get_element_name_from_die(next_die)
            member_type_name = self._get_element_type_name_from_die(next_die)
            members.append(Union.Member(member_name, member_type_name, self))
            next_die = next(die_iterator)
        self._unions[name] = Union(name, die.attributes['DW_AT_byte_size'].value, tuple(members))

    def _create_pointer_type(self, die: DIE, _: typing.Iterator[DIE]):
        name = self._get_element_name_from_die(die)
        type_name = self._get_element_type_name_from_die(die)
        self._pointers[name] = Pointer(name, type_name, self)

    def _create_variable(self, die: DIE, _: typing.Iterator[DIE]):
        name = self._get_element_name_from_die(die)
        type_name = self._get_element_type_name_from_die(die)
        if name in self._symbols.keys():
            self._variables[name] = Variable(name, type_name, self, self._symbols[name].st_value)

    def _create_const_type(self, die: DIE, _: typing.Iterator[DIE]):
        name = self._get_element_name_from_die(die)
        type_name = self._get_element_type_name_from_die(die)
        self._constants[name] = Constant(name, type_name, self)

    def _create_array_type(self, die: DIE, die_iterator: typing.Iterator[DIE]):
        name = self._get_element_name_from_die(die)
        type_name = self._get_element_type_name_from_die(die)
        next_die = next(die_iterator)
        dimension = list()
        while next_die.tag == 'DW_TAG_subrange_type':
            if 'DW_AT_upper_bound' in next_die.attributes.keys():
                dimension.append(next_die.attributes['DW_AT_upper_bound'].value)
            next_die = next(die_iterator)
        self._arrays[name] = Array(name, type_name, self, dimension)

    @staticmethod
    def get_location_from_attribute(attribute) -> int:
        if attribute.form == 'DW_FORM_block':
            return attribute.value[1]
        elif attribute.form == 'DW_FORM_data1':
            return attribute.value
        else:
            raise AttributeError(attribute.form)

    def get_type_from_type_name(self, type_name: str):
        if type_name in self._type_definitions.keys():
            return self._type_definitions[type_name]
        elif type_name in self._base_types.keys():
            return self._base_types[type_name]
        elif type_name in self._enumerations.keys():
            return self._enumerations[type_name]
        elif type_name in self._structures.keys():
            return self._structures[type_name]
        elif type_name in self._unions.keys():
            return self._unions[type_name]
        elif type_name in self._pointers.keys():
            return self._pointers[type_name]
        elif type_name in self._arrays.keys():
            return self._arrays[type_name]
        elif type_name in self._sub_routines.keys():
            return self._sub_routines[type_name]
        elif type_name in self._constants.keys():
            return self._constants[type_name]
        return type_name

    @property
    def abi_info(self) -> AbiInfo:
        """
        returns the ABI information.
        """
        return AbiInfo(**dict((k, self.header[k]) for k in ('e_machine', 'e_version')))

    @property
    def base_address(self) -> Address:
        """
        returns the address of the first instruction in the ELF file.
        """
        return Address(self.header.e_entry)

    @property
    def binary_address(self) -> Address:
        """
        returns the lowest address of the binary from the ELF file.
        """
        address = Address(-1)
        for segment in self.iter_segments():
            if segment['p_type'] == 'PT_LOAD':
                if (address == -1) or (segment.header['p_paddr'] < address):
                    address = segment.header['p_paddr']
        return address

    @property
    def binary(self) -> bytes:
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
    def endianness(self) -> str:
        """
        endianness of the binary.

        :getter: returns the endianness of the binary
        :setter: sets the endianness of the binary
        :type: str
        """
        return self._endianness

    @endianness.setter
    def endianness(self, value: str):
        if value:
            self._endianness = 'little'
        else:
            self._endianness = 'big'

    def files(self) -> typing.Iterator[str]:
        """
        returns an iterator containing all source files in the ELF file.

        :return: list of file name
        """
        return (k for k, v in self._symbols.items() if hasattr(v, 'st_info') and v.st_info.type == 'STT_FILE')

    def variables(self) -> typing.Iterator[Variable]:
        """
        returns an iterator on all variables available in the ELF file.
        """
        return (e for e in sorted(self._variables.values(), key=lambda v: v.name))

    def get_variable(self, name: str) -> typing.Any:
        return self._variables[name]

    @property
    def path(self) -> str:
        """
        returns the full path of the elf file.
        """
        return self._path

    @path.setter
    def path(self, value: str):
        self._path = value

    def symbols(self) -> typing.Iterator[Symbol]:
        """
        returns an iterator on all symbols available in the ELF file.
        """
        return (k for k, v in self._symbols.items() if
                hasattr(v, 'st_info') and v.st_info.type == 'STT_OBJECT')

    def get_symbol(self, name: str) -> Symbol:
        """
        returns a Symbol object containing the properties of the symbol named 'name' in the ELF file.

        :param name: symbol name
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
