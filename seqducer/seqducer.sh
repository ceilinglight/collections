#!/bin/bash

function fastq2fasta() {
awk '
{
	counter++
	if(counter==1)
	{
		print(">"substr($0,2,length($0)))
	}
	else if(counter==2)
	{
		print
	}
	else if(counter==4)
	{
		counter=0
	}
}'
}

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
File_prefix=$PWD/${1##*/}
Coor_file=${File_prefix}.coor
Id_file=${File_prefix}.id
Fasta_file=${File_prefix}.fasta

declare -A Filetype_array
Filetype_array=(['gzip']=1 ['ASCII']=1)

Filetype=$(file -b $1 | cut -d ' ' -f 1)
if [[ ${Filetype_array[$Filetype]} ]]
then
	Fastq_command='zless $1 | fastq2fasta'
else
	exit 1
fi

blastn \
	-query <(eval $Fastq_command) \
	-subject $2 \
	-dust no \
	-outfmt "6 qaccver qstart qend sstart send sstrand" \
	-word_size 32 \
	-reward 1 \
	-penalty -1 \
	-gapopen 4 \
	-gapextend 1 > $Coor_file

cut -f 1 $Coor_file | sort | uniq > $Id_file

zless $1 | grep -A3 -f $Id_file --no-group-separator | fastq2fasta > $Fasta_file

python3 $DIR/gapFiller.py $Fasta_file $Coor_file
