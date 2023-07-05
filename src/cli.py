"""
:file: cli.py
:author: Guillaume Sottas
:date: 24/10/2019
"""

import argparse
import json

from pyelf.parser import ElfFile


def main():
    parser = argparse.ArgumentParser(prog='pya2l', description='python command line utility for elf-formatted files.')
    parser.add_argument('input_file', help='input file path')
    parser.add_argument('-O',
                        dest='output_format',
                        metavar='output format',
                        action='store',
                        default='binary',
                        nargs='?',
                        help='output file format')

    args = parser.parse_args()

    elf = ElfFile(args.input_file)
    result = list()
    for variable in elf.variables():
        # result.append(variable.to_json())
        try:
            result.append(variable.to_json())
        except RecursionError as e:
            print(f'{variable.name} | {str(e)}')
            continue
    with open('output2.json', 'w') as fp:
        json.dump(result, fp, indent=2, sort_keys=True)

    # if args.output_format == 'binary':
    #     args.output_file.write(elf.binary)


if __name__ == '__main__':
    main()
