#!/usr/bin/env python

from collections import Counter, defaultdict
from heapq import heapify, heappush, heappop
import itertools
import operator
import sys

PROB_ONE = 0.01 # f, probability of a bit being a 1

class HuffmanEncoder:
    """Compression using run-length encoding and Huffman Coding."""

    def __init__(self, fileSize=10000, maxLength = sys.maxint, codebook = None):
        """

        >>> huff = HuffmanEncoder()
        >>> huff.maxLength == sys.maxint
        True
        >>> huff.codebook == None
        True
        """
        self.maxLength = maxLength
        self.codebook = codebook
        self.fileSize = fileSize

    def encode(self, f):
        """Encodes a corpus. Uses self.codebook if available, otherwise computes self.codebook from
        the empirical symbol occurrences in `f`.

        Args:
            f (File): The file object where each line is a '0' or '1'.

        Returns:
            string: The corpus encoded according to the supplied codebook.

        >>> huff = HuffmanEncoder()
        >>> huff.encode(["0","0","0","1","0","0","1"])
        '10'
        >>> huff.codebook
        {2: '0', 3: '1'}
        """
        runLengths = self.__rle(f)
        if not self.codebook:
            self.codebook = self.makeHuffmanCodeFromFile(f)
        return ''.join(map(lambda sym: self.codebook[sym], runLengths))

    def decode(self, f):
        """Undoes a Huffman + RLE using self.codebook

        Args:
            f (File): The file object containing the compressed data.

        Returns:
            string: A string representation of the uncompressed data where each line is a 0 or 1.

        >>> huff = HuffmanEncoder(fileSize=7, codebook={2: '0', 3: '1'})
        >>> ''.join(huff.decode(['10']).split('\\n'))
        '0001001'
        """
        assert self.codebook is not None, "Cannot decode with empty codebook"
        invertedIndex = { self.codebook[sym]:sym for sym in self.codebook }

        currBlock = ""
        runLengths = []
        for c in f[0]: # assumes `f` has single line of '0' and '1'
            currBlock = currBlock + c
            if currBlock in invertedIndex:
                runLengths.append(invertedIndex[currBlock])
                currBlock = ""
        assert currBlock == "", "Finished decoding without consuming all input"
        return "\n".join(self.__rld(runLengths)) + "\n"

    def makeHuffmanCodeFromFile(self, f):
        """Overload which first converts File object `f` into empirical probabilities. """
        corpus = self.__rle(f)
        codes = defaultdict(str)
        counts = Counter(corpus)
        return self.makeHuffmanCode(counts)

    def makeHuffmanCode(self, counts):
        """Constructs a Huffman code using empirical symbol occurrences. One leaf
        of the Huffman tree represents `self.maxLength` contiguous zeros, the others
        represents a run of zeros (< `self.maxLength`) terminated by a one.

        Args:
            counts (Dict[int,float]): Occurence counts for source symbols.

        Returns:
            Dict[int,string]: A map from symbols to Huffman code codewords.

        >>> huff = HuffmanEncoder()
        >>> huff.makeHuffmanCode(Counter([1, 1, 1, 1, 2, 2, 3, 3]))
        {1: '0', 2: '10', 3: '11'}
        """
        # entries in heap: (probability of entry, [(symbol, huffmanCode)])
        heap = map(lambda x: (x[1], [(x[0], '')]), counts.items())
        heapify(heap)

        while len(heap) > 1:
            e1 = heappop(heap)
            e2 = heappop(heap)
            merged = HuffmanEncoder.__merge(e1, e2)
            heappush(heap, merged)
        return dict(heap[0][1])

    @staticmethod
    def __merge(e1, e2):
        """Merges two entries while building a huffman tree.

        Args:
            e1, e2 ((float, List[(int, string)])): Huffman subtrees. The first coordinate is the
                probability of all run lengths in the subtree, and the second contains an
                associative list between run lengths to Huffman codewords.

        Returns:
            (float, List[(string, string)]): A Huffman subtree obtained by adding the
                probabilities and prefixing all subtree codewords with '0' or '1'.

        >>> huff = HuffmanEncoder(fileSize = 7)
        >>> huff._HuffmanEncoder__merge((0.3, [(7, '0'), (3, '1')]), (0.2, [(1, '0'), (2, '1')]))
        (0.5, [(7, '00'), (3, '01'), (1, '10'), (2, '11')])
        """
        mergedProb = e1[0] + e2[0]
        mergedCodes = map(lambda x: (x[0], '0' + x[1]), e1[1]) + \
                map(lambda x: (x[0], '1' + x[1]), e2[1])
        return (mergedProb, mergedCodes)

    def __rle(self, f):
        """Performs run-length encoding for runs of zeros.

        Args:
            f (File): The file object where each line is a '0' or '1'.

        Returns:
            List[int]: A list of the '0' symbol run lengths in `f`.

        >>> huff = HuffmanEncoder(fileSize = 7)
        >>> huff._HuffmanEncoder__rle('000100001')
        [3, 4]
        >>> huff._HuffmanEncoder__rle('00010000')
        [3]
        """
        rle = []
        currRunLength = 0
        for rawLine in f:
            line = int(rawLine.strip())
            if line == 0:
                if currRunLength < self.maxLength-2:
                    currRunLength += 1
                else: # need to decide to use all zeros or 1 terminated
                    # TODO: check f.hasNext()
                    nextSymb = int(next(f).strip())
                    if nextSymb == 0:
                        rle.append(currRunLength+2)
                    else:
                        rle.append(currRunLength+1)
                    currRunLength = 0
            else:
                rle.append(currRunLength)
                currRunLength = 0
        # don't include last run because decoding pads with zeros to self.fileSize
        return rle

    def __rld(self, runLengths):
        """ Undoes run-length encoding.

        Args:
            runLengths (List[int]): A list of the '0' symbol run lengths in `f`.


        Returns:
            string: The original bit string, padded with zeros to self.fileSize.

        >>> huff = HuffmanEncoder(fileSize = 9)
        >>> huff._HuffmanEncoder__rld([3, 4])
        '000100001'
        >>> huff = HuffmanEncoder(fileSize = 12)
        >>> huff._HuffmanEncoder__rld([3, 4])
        '000100001000'
        """
        def rlToSymbols(l):
            """Converts a run-length `l` into a List of symbols, by decoding into runs of '0's
            terminated by '1' for `l < self.maxLength` and a contiguous run of '0's for
            `l == self.maxLength`.
            """
            if l < self.maxLength:
                return "0"*l + "1"
            else:
                return "0"*l
        decoding = reduce(operator.add, map(rlToSymbols, runLengths))

        # pad with final '0' run to self.fileSize source symbols
        return decoding + "0"*(self.fileSize- len(decoding))

if __name__ == "__main__":
    import doctest
    doctest.testmod()
