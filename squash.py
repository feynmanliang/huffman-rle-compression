import pickle
import sys

from HuffmanEncoder import HuffmanEncoder

def codebookFromEmpirical(inPath, outPath):
    """Constructs Huffman codebook from empirical probabilities."""
    encoder = HuffmanEncoder(maxLength=69)
    with open(inPath, "r") as inFile:
        codebook = encoder.makeHuffmanCode(inFile)
    with open(outPath, "w") as outFile:
        pickle.dump(codebook, outFile)

def codebookFromGeometric():
    # TODO: we know that run lengths are geometrically distributed, so can reduce variance using theory
    pass

if __name__ == "__main__":
        # TODO: vary maxLength and look at performance
        # see http://www.inference.phy.cam.ac.uk/mackay/LoverH.pdf

        codebookFromEmpirical("filep.01.10000.txt", "filep_01_1000_codebook.pickle")

        # Use empirical probabilities for decoding
        with open("filep_01_1000_codebook.pickle", "r") as codebookFile:
            codebook = pickle.load(codebookFile)
        inFile = sys.stdin
        encoder = HuffmanEncoder(maxLength=69, codebook=codebook)
        encodedFile = encoder.encode(inFile)
        sys.stdout.write(encodedFile)
