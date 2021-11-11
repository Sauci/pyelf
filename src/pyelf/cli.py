"""
:file: cli.py
:author: Guillaume Sottas
:date: 24/10/2019
"""

import argparse

from .pyelf import ElfFile


def main():
    parser = argparse.ArgumentParser(prog='pya2l', description='python command line utility for elf-formatted files.')
    parser.add_argument('input_file', help='input file path')
    parser.add_argument('output_file', type=argparse.FileType('wb'), help='output file path')
    parser.add_argument('-O',
                        dest='output_format',
                        metavar='output format',
                        action='store',
                        default='binary',
                        nargs='?',
                        help='output file format')

    args = parser.parse_args()

    elf = ElfFile(args.input_file)

    if args.output_format == 'binary':
        args.output_file.write(elf.binary)


if __name__ == '__main__':
    main()
