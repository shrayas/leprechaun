#!/usr/bin/env python3

from itertools import product
from string import ascii_lowercase

def letter_generator(limit):
  for length in range(1, limit+1):
    for letters in product(ascii_lowercase, repeat=length):
      yield ''.join(letters)

for letters in letter_generator(2):
  print(letters)
