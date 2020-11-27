# Only works for FASTA file with one line of sequence
# Issue#2
BEGIN{
	rc["A"]="T"
	rc["T"]="A"
	rc["C"]="G"
	rc["G"]="C"
	rc["R"]="Y"
	rc["Y"]="R"
	rc["M"]="K"
	rc["K"]="M"
	rc["S"]="S"
	rc["W"]="W"
	rc["H"]="D"
	rc["D"]="H"
	rc["B"]="V"
	rc["V"]="B"
	rc["N"]="N"
	rc["-"]="-"
	rc["."]="."
}
{
	if($0~/^>/)
	{
		print
	}
	else
	{
		split($0, chars, "")
		for(i=length($0); i>=1; i--)
		{
			printf(rc[chars[i]])
		}
		print("")
	}
}
