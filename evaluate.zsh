rm filep.01.10000.txt.huffman filep.01.10000.txt.decode
python squash.py < filep.01.10000.txt > filep.01.10000.txt.huffman
python unsquash.py < filep.01.10000.txt.huffman > filep.01.10000.txt.decode
diff filep.01.10000.txt filep.01.10000.txt.decode
