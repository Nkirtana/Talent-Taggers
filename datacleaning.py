import re
from string import punctuation
# NLTK imports
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.util import ngrams

stopwords = stopwords.words('english')


# By default, stopwords from nltk corpus are used, we can pass our own list of stopwords if required when creating
# the class object. Punctuations are removed from text by default, when creating class keep_punctutation argument can
# be used to keep punctuation.
class CleanData:
    def __init__(self, stop_words=stopwords, punctuations=punctuation,
                 keep_punctuation=False, keep_stopwords=False):
        self.input_text = None
        self.input_text_temp = None
        self.keep_punctuation = keep_punctuation
        self.keep_stopwords = keep_stopwords
        self.stop_words = stop_words    # Custom stopwords list
        self.punctuations = punctuations    # Custom punctuation list
        self.output = dict()

    def initialize_text(self, input_text):
        self.input_text = input_text.strip()
        self.input_text_temp = input_text.strip()
        self.output = dict()

    # Remove non-alphanumeric characters, punctuation flag to keep or remove punctuation
    def remove_non_alphanumeric(self):
        if self.keep_punctuation:
            self.input_text = re.sub(f"[^a-zA-Z0-9_{self.punctuations}]", " ", self.input_text)
        else:
            self.input_text = re.sub(f"[^a-zA-Z0-9_]", " ", self.input_text)
        print(f"Removed Non-alphanumeric characters, keep_punctuation:{self.keep_punctuation}")

    def remove_whitespace(self):
        self.input_text = re.sub("[\t\n\r\f\v]", " ", self.input_text)
        print("removed white spaces")

    def remove_stopwords(self):
        tokens = word_tokenize(self.input_text)
        output = list()
        for token in tokens:
            if token.lower() not in self.stop_words:
                output.append(token)
        self.input_text = " ".join(output)
        print("removed stopwords")

    # Removes extra spaces from text
    def remove_extra_spaces(self):
        self.input_text = re.sub('[ ]+', ' ', self.input_text)
        print("Removed extra spaces")

    def generate_ngram(self, n):
        n_grams = ngrams(word_tokenize(self.input_text), n)
        n_grams = [' '.join(grams) for grams in n_grams]
        if n == 1:
            self.output["unigrams"] = n_grams
        elif n == 2:
            self.output["bigrams"] = n_grams
        elif n == 3:
            self.output["trigrams"] = n_grams
        else:
            self.output['ngram'] = n_grams

    def clean_text(self):
        self.remove_non_alphanumeric()
        self.remove_whitespace()
        self.remove_stopwords()
        self.remove_extra_spaces()
        self.output["output_text"] = self.input_text
        self.output["input_text"] = self.input_text_temp
        self.generate_ngram(2)

    def get_output(self):
        return self.output

    def __str__(self):
        return f"Keep punctuation flag: {self.keep_punctuation}\nKeep stopwords flag: {self.keep_stopwords}" \
               f"\nCustom punctuations: {self.punctuations}"


# Testing
from filereader import ReadFiles
# rf = ReadFiles(r"C:\Users\manoj\Downloads\INFORMATION-TECHNOLOGY\10089434.pdf")
# rf.read_input()
# input_text = list(rf.text_dict.values())[0]
# cd = CleanData(keep_stopwords=False, keep_punctuation=False)
# cd.initialize_text(input_text)
# cd.clean_text()
# f = open("test.json", "w")
# import json
# json.dump(cd.output, f, indent = 4)
# f.close()
# print(cd)
