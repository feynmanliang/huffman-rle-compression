from collections import Counter, defaultdict
from heapq import heapify, heappush, heappop
import itertools

class HuffmanEncoder:
    """Compression using run-length encoding and Huffman Coding."""

    def __init__(self, maxLength = sys.maxint, codebook = None):
        self.maxLength = maxLength
        self.codebook = codebook

    def __rle(self, f):
        """Performs run-length encoding for runs of zeros.

        Args:
            f (File): The file object where each line is a '0' or '1'.

        Returns:
            List[int]: A list of the '0' symbol run lengths in `f`.

        """
        rle = []
        currRunLength = 0
        for rawLine in f:
            line = int(rawLine.strip())
            if line == 0 and currRunLength < self.maxLength:
                currRunLength += 1
            else:
                rle.append(currRunLength)
                currRunLength = 0
        return rle

    def makeHuffmanCode(self, f):
        """Constructs a Huffman code using empirical symbol occurrences.

        Args:
            f (File): The file object where each line is a '0' or '1'.

        Returns:
            Dict[int,string]: A map from symbols to Huffman code codewords.

        """
        corpus = self.__rle(f)
        codes = defaultdict(str)
        counts = Counter(corpus)
        N = 1.*sum(counts.values())

        # entries in heap: (probability of entry, [(symbol, huffmanCode)])
        heap = map(lambda x: (x[1]/N, [(x[0], '')]), counts.items())
        heapify(heap)

        while len(heap) > 1:
            e1 = heappop(heap)
            e2 = heappop(heap)
            merged = HuffmanEncoder.__merge(e1, e2)
            heappush(heap, merged)
        return dict(heap[0][1])

    @staticmethod
    def __merge(e1, e2):
        """Merges two entries while building a huffman tree."""
        mergedProb = e1[0] + e2[0]
        mergedCodes = map(lambda x: (x[0], '0' + x[1]), e1[1]) + \
                map(lambda x: (x[0], '1' + x[1]), e2[1])
        return (mergedProb, mergedCodes)

    def encode(self, f):
        """Encodes a corpus. Uses self.codebook if available, otherwise computes self.codebook from
        the empirical symbol occurrences in `f`.

        Args:
            f (File): The file object where each line is a '0' or '1'.

        Returns:
            string: The corpus encoded according to the supplied codebook.

        """
        runLengths = self.__rle(f)
        if not self.codebook:
            self.codebook = HuffmanEncoder.makeHuffmanCode(f)
        return ''.join(map(lambda sym: self.codebook[sym], runLengths))

    def decode(self, f):
        assert(self.codebook, "Cannot decode with empty codebook")
