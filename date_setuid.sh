#!/bin/bash
fisier="/usr/bin/sudo"
flags=("-A" "-B" "-b" "-C" "-D" "-E" "-e" "-g" "-H" "-h" "-i" "-K" "-k" "-l" "-N" "-n" "-P" "-p" "-R" "-r" "-S"  "-s" "-t" "-U" "-T" "-u" "-V" "-v")
nume=$(basename "$fisier")
#i=0;
#for flag in "${flags[@]}"; do
	#i=$((i+1))
#	sudo strace -c "$fisier" "$flag" > /dev/null 2>> "${nume}_date.txt"
#done
sudo strace -c "$fisier" -A > /dev/null 2>> "${nume}_date.txt"
