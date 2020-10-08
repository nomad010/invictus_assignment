from collections import Counter
import os
from typing import List, Dict

import huffman
from nameko.rpc import rpc

WORDS_ENV_PATH = 'WORDS_PATH'
WORDS_ENV_DEFAULT = 'words'


class OddSquarerService:
    name = "odd_squarer_service"

    @rpc
    def square_odd_numbers(self, numbers: List[int]) -> List[int]:
        # Square the odd numbers in the list
        return [x * x if x % 2 == 1 else x for x in numbers]


# An exception to indicate an error occurred during decoding a string.
class UnableToDecodeStringException(Exception):
    pass


# An exception to indicate an error occurred during encoding a string.
class UnableToEncodeStringException(Exception):
    pass


class HuffmanCodec:
    name = "huffman_codec_service"

    def __init__(self):
        """
        Initialises the huffman codec service with creates and codebook for
        compression and a reverse codebook for decompression
        """
        self.codebook = self.create_codebook(
            os.environ.get(WORDS_ENV_PATH, WORDS_ENV_DEFAULT)
        )
        self.reverse_codebook = {}
        for (letter, prefix) in self.codebook.items():
            self.reverse_codebook[prefix] = letter

    def create_codebook(self, path: str) -> huffman.codebook:
        """
        The huffman package requires one to give it a list of frequencies to
        generate a codebook for use during encoding and decoding. The following
        function loads the frequencies and returns the created codebook. The
        frequency file is given by a list of words seperated by newlines. The
        frequencies of these words are summed up to create the final
        frequencies.
        """
        frequencies: Counter = Counter()
        with open(path) as freqs:
            for line in freqs:
                frequencies.update(line.strip())
        return huffman.codebook(frequencies.items())

    @ rpc
    def encode(self, words: List[str]) -> Dict[str, str]:
        """
        The huffman package is missing an encode function in its API. We
        implement the encode manually here by looking up which letter
        corresponds to which bitstring in the codebook. This can fail if our
        codebook doesn't have a mapping for a given letter.
        """
        try:
            return {
                word: "".join(
                    self.codebook[letter] for letter in word
                ) for word in words
            }
        except KeyError:
            raise UnableToEncodeStringException()

    @ rpc
    def decode(self, word: str):
        """
        The huffman package is missing a decode function in its API. We
        implement the decode manually here by slicing off prefixes that are
        in the codebook. This can fail when codes aren't in the codebook.
        """
        result = ""
        prefix = ""
        for chr in word:
            prefix += chr
            letter = self.reverse_codebook.get(prefix)
            if letter is not None:
                result += letter
                prefix = ""
        if len(prefix) != 0:
            raise UnableToDecodeStringException()
        else:
            return result
