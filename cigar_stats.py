#!/usr/bin/env python3

import argparse
import collections
import re
import sys

def get_args():
    """Argument definition."""

    parser = argparse.ArgumentParser(
            description="Report CIGAR statistics",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter
            )

    parser.add_argument(
            'cigar_file',
            metavar='cigar file',
            nargs='?',
            default=('STR' if sys.stdin.isatty() else sys.stdin),
            type=argparse.FileType('r'),
            help='Text file contains one CIGAR string per line'
            )

    parser.add_argument(
            '-f',
            '--format',
            metavar='STR',
            help='Display only CIGAR string in STR',
            default=''
            )

    parser.add_argument(
            '-H',
            '--hide-header',
            help='Hide header',
            action='store_true'
            )

    parser.add_argument(
            '-d',
            '--delimiter',
            metavar='STR',
            help='Use STR as a delimiter',
            default='[tab]'
            )

    parser.add_argument(
            '-v',
            '--verticle',
            help='Output in verticle instead of tab-delimited',
            action='store_true'
            )

    return parser.parse_args()


def parse_cigar(cigar_lines):
    """Find cigar string on each line and store value"""
    cigar_dict = collections.defaultdict(int)
    pattern = re.compile(r'[0-9]*[A-Z]')
    for line in cigar_lines:
        matches = pattern.findall(line)
        if matches:
            cigar_dict['READ_COUNT'] += 1
        for match in matches:
            nuc_len = int(match[:-1])
            char = match[-1]
            cigar_dict[char] += nuc_len
            cigar_dict['NUC_COUNT'] += nuc_len

    return cigar_dict


def main():
    """main"""
    args = get_args()

    cigar_lines = [line.strip() for line in args.cigar_file]
    cigar_dict = parse_cigar(cigar_lines)

    if not args.format:
        header = ['READ_COUNT', 'NUC_COUNT']
        remain_keys = [key for key in cigar_dict.keys() if key not in header]
        remain_keys.sort()
        header.extend(remain_keys)

    else:
        header = args.format.upper()
        if ' ' in header:
            header = header.split()
        else:
            header = [x for x in header]

    stats = [str(cigar_dict[key]) for key in header]

    if args.delimiter == '[tab]':
        delimiter = '\t'
    else:
        delimiter = args.delimiter

    if not args.verticle:
        header_line = delimiter.join(header)
        stats_line = delimiter.join(stats)

        if not args.hide_header:
            print(header_line)
        print(stats_line)

    else:
        if not args.hide_header:
            for line in zip(header, stats):
                print(delimiter.join(line))
        else:
            for line in stats:
                print(line)


if __name__ == "__main__":
    main()
