# Literally gap filler

from Bio import SeqIO
from collections import defaultdict
import sys

def find_start_base(SeqRecord):
    start = 0
    for nuc in SeqRecord.seq:
        if nuc == '-':
            start += 1
        else:
            break
    return start

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
                match_len = int(line[2])-int(line[1])
                old_match_len = int(reads[line[0]]['hit'][2])-int(reads[line[0]]['hit'][1])
                if match_len > old_match_len:
                    reads[line[0]]['hit'] = line
            else:
                reads[line[0]]['hit'] = line

    # Calculate offset value
    for identifier, value in reads.items():
        if value['hit'][5] == 'plus':
            offset = int(value['hit'][3])-int(value['hit'][1])
        else:
            offset = int(value['hit'][4])+int(value['hit'][2])-len(reads[identifier]['record'])-1
        reads[identifier]['offset'] = offset

    output_string = ''

    # Justify offset
    min_offset = min([value['offset'] for value in reads.values()])

    gapped_records = []
    for identifier, value in reads.items():
        if value['hit'][5] == 'minus':
            seq = str(reads[identifier]['record'].seq.reverse_complement().upper())
        else:
            seq = str(value['record'].seq.upper())
        reads[identifier]['offset'] -= min_offset
        seq = '-'*reads[identifier]['offset'] + seq
        gapped_records.append(SeqIO.SeqRecord(seq, id=identifier))

    gapped_records = sorted(gapped_records, key=lambda x: find_start_base(x))
    for record in gapped_records:
        print(f'>{record.id}')
        print(f'{record.seq.upper()}')
    print()


if __name__ == "__main__":
    main()
