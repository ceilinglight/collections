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

declare -A Filetype_array
for constant in ASCII gzip
do
    array[$constant]=1
done

Filetype=$(file -b $1 | cut -d ' ' -f 1)
if [[ ${Filetype_array[$Filetype] ]]
then
	Fastq_command='zless $1 | fastq2fasta'
else
	exit 1
	

blastn \
	-query <(eval $Fastq_command) \
	-subject $2 \
	-dust no \
	-outfmt "6 qaccver qstart qend sstart send sstrand" \
	-word_size 32 > $3
