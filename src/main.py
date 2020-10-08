from collections import Counter
import os
from typing import List

import huffman
from nameko.rpc import rpc

WORDS_ENV_PATH = 'WORDS_PATH'
WORDS_ENV_DEFAULT = 'words'


class OddSquarerService:
    name = "odd_squarer_service"

    @rpc
    def square_odd_numbers(self, numbers: List[int]):
        # Square the odd numbers in the list
        return [x * x if x % 2 == 1 else x for x in numbers]


class HuffmanCodec:
    name = "huffman_codec_service"

    def __init__(self):
        self.codebook = huffman.codebook(
            self.load_frequencies(os.environ.get(
                WORDS_ENV_PATH, WORDS_ENV_DEFAULT)).items()
        )
        self.reverse_codebook = {}
        for (letter, prefix) in self.codebook.items():
            self.reverse_codebook[prefix] = letter

    def load_frequencies(self, path: str) -> huffman.codebook:
        frequencies: Counter = Counter()
        with open(path) as freqs:
            for line in freqs:
                frequencies.update(line.strip())
        return frequencies

    def encode(self, value: str):
        result = "".join([self.codebook[v] for v in value])
        return result

    @rpc
    def compress(self, words: List[str]):
        # Compress the words in the list
        return {
            k: self.encode(k) for k in words
        }
