BEGIN{
	rc["A"]="T"
	rc["T"]="A"
	rc["C"]="G"
	rc["G"]="C"
}
{
	if($0~/^>/)
	{
		print
	}
	else
	{
		split($0, chars, "")
		for(i=1; i<=length($0); i++)
		{
			printf(rc[chars[i]])
		}
		print("")
	}
}
