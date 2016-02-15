import pickle
import sys

from HuffmanEncoder import HuffmanEncoder

if __name__ == "__main__":
    with open("filep_01_1000_codebook.pickle", "r") as codebookFile:
        codebook = pickle.load(codebookFile)
    inFile = sys.stdin
    encoder = HuffmanEncoder(maxLength=69, codebook=codebook)
    decodedFile = encoder.decode(inFile)
    sys.stdout.write(decodedFile)
