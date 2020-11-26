# Literally gap filler

from Bio import SeqIO
from collections import defaultdict
import sys

def main():
    reads = defaultdict(dict)
    # To do: Convert sys.argv to argparse
    # Open reads.fasta
    with open(sys.argv[1]) as in_file:
        for record in SeqIO.parse(in_file, 'fasta'):
            reads[record.id]['record'] = record

    # Open reads.coor
    with open(sys.argv[2]) as in_file:
        for line in in_file:
            line = line.split()
            if 'hit' in reads[line[0]].keys():
                continue
            reads[line[0]]['hit'] = line

    # Calculate offset value
    for identifier, value in reads.items():
        if value['hit'][5] == 'plus':
            offset = int(value['hit'][3])-int(value['hit'][1])
        else:
            continue
#             offset = int(value['hit'][4])-int(value['hit'][2])
        reads[identifier]['offset'] = offset

    output_string = ''

    # Justify offset
    min_offset = min([value['offset'] if value['hit'][5]=='plus' else 99999 for value in reads.values()])
    for identifier, value in reads.items():
        if value['hit'][5] == 'minus':
            continue
        reads[identifier]['offset'] -= min_offset
        output_string += f'>{identifier}\n'
        output_string += '-'*reads[identifier]['offset']
        output_string += str(value['record'].seq.upper())
        output_string += '\n'

    # with open(sys.arg[3], 'w') as out_file:
    #     out_file.write(output_string)
    print(output_string)

if __name__ == "__main__":
    main()
