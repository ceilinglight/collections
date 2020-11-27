# Seqducer
A script to gather similar sequences and make a rough msa in FASTA format.

## Requirements
The script has the following requirements:

* [NCBI BLAST+][1] version 2.10.0

* [python][2] version 3.8

Python library:
* [BioPython][3] version 1.78

## Usage
```
$ ./seqducer.sh sequences.fasta/fastq reference.fasta > msa_output.fasta
```


[1]: https://blast.ncbi.nlm.nih.gov/Blast.cgi?CMD=Web&PAGE_TYPE=BlastDocs&DOC_TYPE=Download
[2]: https://www.python.org/
[3]: https://biopython.org/
