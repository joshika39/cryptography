#!/bin/bash

translate () {
	echo -n  "$*" | tr '\!-~' '\P-~\!-O'
}

main () {
	read -r input
	
	if [ "$input" == "" ]; then
		input="$(xsel -b )"
	fi

	result="$(translate $input )"
	echo $result
	echo -n $result | xsel -b -i
}

while [ 3 == 3 ]; do 
	main
done
