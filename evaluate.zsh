rm filep.01.10000.txt.encode filep.01.10000.txt.decode
python squash.py < filep.01.10000.txt > filep.01.10000.txt.encode
python unsquash.py < filep.01.10000.txt.encode > filep.01.10000.txt.decode
wc filep.01.10000.txt.encode
diff filep.01.10000.txt filep.01.10000.txt.decode
