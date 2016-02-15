import operator
import pickle
import sys

from HuffmanEncoder import HuffmanEncoder, PROB_ONE

def codebookFromEmpirical(inPath, outPath, maxLength):
    """Constructs Huffman codebook from empirical probabilities."""
    encoder = HuffmanEncoder(maxLength=maxLength)
    with open(inPath, "r") as inFile:
        codebook = encoder.makeHuffmanCodeFromFile(inFile)
    with open(outPath, "w") as outFile:
        pickle.dump(codebook, outFile)

def codebookFromGeometric(outPath, maxLength):
    """Computes the PMF of the Geometric distribution renormalized to $0 <= k <= maxLength"""
    def pmf(k, p):
        if k < maxLength:
            return reduce(operator.mul, [(1-p) for _ in range(k-1)], 1)*p
        else:
            return reduce(operator.mul, [(1-p) for _ in range(maxLength)], 1)
    probs = { k: pmf(k, PROB_ONE) for k in range(maxLength+1) }

    encoder = HuffmanEncoder(maxLength=maxLength)
    codebook = encoder.makeHuffmanCode(probs)
    with open(outPath, "w") as outFile:
        pickle.dump(codebook, outFile)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='RLE+Huffman compress a file.')
    parser.add_argument('--maxRunLength', type=int, default=69, help='length of maximum run in RLE')
    parser.add_argument('--codebook', type=str, default="geometric_codebook.pickle",
            help='pickle of the codebook to use')
    parser.add_argument('--genCodebooks', action="store_true", default=False, help='regenerate the codebooks')
    args = parser.parse_args()

    maxLength = args.maxRunLength
    codebookPath= args.codebook

    if args.genCodebooks:
        codebookFromEmpirical("filep.01.10000.txt", "filep_01_1000_codebook.pickle", maxLength)
        codebookFromGeometric("geometric_codebook.pickle", maxLength)

    with open(codebookPath, "r") as codebookFile:
        codebook = pickle.load(codebookFile)
    encoder = HuffmanEncoder(maxLength=maxLength, codebook=codebook)
    encodedFile = encoder.encode(sys.stdin)
    sys.stdout.write(encodedFile)
