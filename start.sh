#!/bin/sh

source $HOME/.cache/wal/colors.sh

if [[ "$1" == "-k" ]]; then
    python ./lemoney.py -k
else
    python ./lemoney.py -b "$background" -f "$foreground" -bc "$foreground" -bw 1
fi

