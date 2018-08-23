"""
Chapter 4. Naive Bayesian Classification
Text tokenizer
#* Goal of class is to extract words into a stream to keep a low memory profile as opposed to simply returning an array.

#* Class does two things/has two responsibilities:
#*  1: lowercase all words
#*  2: instead of returning an array, uses a block.
"""
import re


class Tokenizer:
  """
  Splits lines by whitespaces, converts to lower case and builds n-grams.
  """
  NULL = u'\u0000'

  @staticmethod
  def tokenize(string):
    return re.findall("\w+", string.lower())

  #! uses the set() method to only return unique tokens
  @staticmethod
  def unique_tokenizer(string):
    return set(Tokenizer.tokenize(string))

  #! An ngram is a contiguous sequence of n items from a given sample of text or speech.
  #TODO: Explore method in more detail, why is there shifting and padding involved?
  @staticmethod
  def ngram(string, ngram):
    tokens = Tokenizer.tokenize(string)

    ngrams = []

    for i in range(len(tokens)):
      shift = i - ngram + 1
      padding = max(-shift, 0)
      first_idx = max(shift, 0)
      last_idx = first_idx + ngram - padding

      ngrams.append(Tokenizer.pad(tokens[first_idx:last_idx], padding))

    return ngrams

  @staticmethod
  def pad(tokens, padding):
    padded_tokens = []

    for i in range(padding):
      padded_tokens.append(Tokenizer.NULL)

    return padded_tokens + tokens
