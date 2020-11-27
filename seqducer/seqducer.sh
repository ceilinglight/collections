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

Coor_file=${1}.coor

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

cut -f 1 $Coor_file | sort | uniq > ${1}.id

zless $1 | grep -A3 -f ${1}.id --no-group-separator | fastq2fasta > ${1}_hits.fasta

python gapFiller.py ${1}_hits.fasta ${1}.coor
