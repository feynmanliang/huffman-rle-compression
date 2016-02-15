#!/usr/bin/zsh

origFile=filep.01.10000.txt
encodeFile=${origFile}.encode
decodeFile=${origFile}.decode

empiricalCodebook=filep_01_1000_codebook.pickle
geometricCodebook=geometric_codebook.pickle

print "maxRunLength,codebook,numBits,numBitErrors"
for maxRunLength in {3..180}; do
  for codebook in $empiricalCodebook $geometricCodebook; do
    rm $encodeFile $decodeFile
    python squash.py \
      --maxRunLength $maxRunLength --codebook $codebook --genCodebooks \
      < $origFile > $encodeFile
    numBits=$(wc $encodeFile | tr -s ' ' | cut -d ' ' -f 4)
    python unsquash.py \
      --maxRunLength $maxRunLength --codebook $codebook \
      < $encodeFile > $decodeFile
    delta=$(diff $origFile $decodeFile)
    print "${maxRunLength},${codebook},$numBits,${#delta}"
  done
done
