#!/usr/bin/zsh

origFile=filep.01.10000.txt
encodeFile=${origFile}.encode
decodeFile=${origFile}.decode

rm $encodeFile $decodeFile
python squash.py < $origFile > $encodeFile
wc $encodeFile
python unsquash.py < $encodeFile > $decodeFile
diff $origFile $decodeFile
