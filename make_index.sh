#!/bin/bash

function read_dir() {
	for file in `ls $1`
	do
		if [ -d $1"/"$file ];then
			if [ "${file##*.}" != "." ];then
				echo -e ""
				echo -e "### "$file
			fi
			read_dir $1"/"$file
		else
			extension="${file##*.}"
			filename="${file%.*}"
			if [ $extension = "md" -a $filename != "index" ];then 
				echo -e "- ["$filename"]("$1"/"$filename")"
			fi
		fi
	done
}

# read_dir $1
read_dir . > index.md
