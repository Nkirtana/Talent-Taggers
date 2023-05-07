import nltk
from zipfile import ZipFile
import os

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('omw-1.4')

# import subprocess
#
# url = "https://nlp.stanford.edu/software/stanford-corenlp-4.3.1.zip"
# subprocess.run(["wget", url])
#
#
# path = os.getcwd()+'/stanford-corenlp-4.3.1.zip'
# with ZipFile(path, 'r') as f:
#   #extract in current directory
#   f.extractall()
