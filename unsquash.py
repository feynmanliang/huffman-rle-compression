import pickle
import sys

from HuffmanEncoder import HuffmanEncoder

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='RLE+Huffman compress a file.')
    parser.add_argument('--maxRunLength', type=int, default=69, help='length of maximum run in RLE')
    parser.add_argument('--codebook', type=str, default="geometric_codebook.pickle",
            help='pickle of the codebook to use')
    args = parser.parse_args()

    maxLength = args.maxRunLength
    codebookPath= args.codebook

    with open(codebookPath, "r") as codebookFile:
        codebook = pickle.load(codebookFile)
    inFile = sys.stdin
    encoder = HuffmanEncoder(maxLength=maxLength, codebook=codebook)
    decodedFile = encoder.decode(inFile)
    sys.stdout.write(decodedFile)
