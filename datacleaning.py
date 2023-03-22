import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.util import ngrams


class CleanData:

    def __init__(self, input_text, stop_words=stopwords):
        self.stop_words = stop_words
        self.input_text = input_text

    def remove_stopwords(self):
        pass

    def clean_text(self, keep_punctuation=False):
        if keep_punctuation:
            pass
        else:
            pass
        re.sub()

    def generate_ngram(self, n):
        n_grams = ngrams(word_tokenize(text), n)
        return [' '.join(grams) for grams in n_grams]
