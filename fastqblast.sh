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
	-word_size 32 > $Coor_file

Read_identifiers='cut -f 1 $Coor_file | sort | uniq'

less $1 | grep -A1 -f <(eval $Read_identifiers) --no-group-separator | fastq2fasta > $3
