#!/usr/bin/env python3

import sqlite3

import db

def _hash_wordlist(wordlist, hashing_algorithm):
  """Hashes each of the words in the wordlist and yields the digests for each
  word.

  Parameters:
    - wordlist: The wordlist which we'll be hashing.
    - hashing_obj: The hashlib hashing algorithm which we'll be passing to the
      appropriate function to actually hash the word.

  Yields:
    - Hexadecimal digest of the given word.

  """
  for word in wordlist:
    # Create a copy of the hashing algorithm so the digest doesn't become
    # corrupted.
    hashing_obj = hashing_algorithm.copy()
    hashing_obj.update(word.encode())

    return_string = hashing_obj.hexdigest() + ":" + word
    yield return_string

def create_rainbow_table(
  wordlist, hashing_algorithm, output, use_database=False):
  """Creates the rainbow table from the given plaintext wordlist.

  Parameters:
    - wordlist: The plaintext wordlist to hash.
    - hashing_algorithm: The algorithm to use when hashing the wordlist.
    - output: The name of the output file.
    - db: Flag whether the output is an SQLite DB or not (default=False).

  """
  # Create the database, if necessary.
  if use_database:
    db_file = output + ".db"
    db_connection = sqlite3.connect(db_file)
    db.create_table(db_connection)
  else:
    # Otherwise, create the plaintext file.
    txt_file = open(output + ".txt", "a")

  # Now actually hash the words in the wordlist.
  try:
    with open(wordlist, "r", encoding="utf-8") as wl:
      for entry in _hash_wordlist(wl, hashing_algorithm):
        if use_database:
          entries = entry.split(":")
          db.save_pair(db_connection, entries[0], entries[1])
        else:
          txt_file.write(entry)
      txt_file.close()
  except IOError as err:
    print("File error: " + str(err))
