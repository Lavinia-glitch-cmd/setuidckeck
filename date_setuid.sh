#!/bin/bash
fisier="/usr/bin/sudo"
flags=("-A" "-B" "-b" "-C" "-D" "-E" "-e" "-g" "-H" "-h" "-i" "-K" "-k" "-l" "-N" "-n" "-P" "-p" "-R" "-r" "-S" "-t" "-U" "-T" "-u" "-V" "-v")
nume=$(basename "$fisier")
for flag in "${flags[@]}"; do
	f=${flag#-}
	output="${nume}_${f}"
	sudo strace -c "$fisier" "$flag" > /dev/null 2> "$output"
done
