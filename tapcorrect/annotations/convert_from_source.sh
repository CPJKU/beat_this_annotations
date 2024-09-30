#!/bin/bash
here="${0%/*}"
if [ "$#" -lt 1 ]; then
    echo "Usage: $0 INPUT_DIR"
    echo "    INPUT_DIR: location of the 'dataset/csv' directory of the"
    echo "      tapcorrect repository (github.com/chordify/tapcorrect)"
    exit
fi
d="$1"
mkdir -p "$here"/beats
for fn in "$d"/*/03-fully_corrected_taps.csv; do
    outfn="${fn%/*.csv}"
    outfn="${outfn##*/}"
    outfn="$here"/beats/"$outfn".beats
    sed -Ee 's/,"(.+)"/\t\1/' "$fn" > "$outfn"
done
