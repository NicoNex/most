#!/bin/bash

# Loop Command Runner.
# Runs a given commands in all directories given in input.
# e.g. ./mcr.sh directory/* "my command"


GREEN='\033[1;32m'
NC='\033[0m'

for d in $@; do
	if [[ -d $d ]]; then
		( printf "$GREEN  Entering: $d $NC\n" && cd $d && ${!#})
	fi
done

