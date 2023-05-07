#NLP
import nltkmodules
import pandas as pd
import os
import nltk

from pandas.io.sql import pandasSQL_builder
from stanfordcorenlp import StanfordCoreNLP
from nltk.util import ngrams
import spacy

NER = spacy.load("en_core_web_sm")

path_to_corenlp = os.getcwd()+'/stanford-corenlp-4.3.1'

def generate_uni_bigram(final):
  bi_gram = []
  tri_gram = []
  
  for sent in final:
    n_grammed = []
    tri_grammed = []
    n_grams = ngrams(sent,2)
    tri_grams = ngrams(sent,3)

    for grams in n_grams:
                  n_grammed.append(' '.join(grams))
                
    bi_gram.append(n_grammed) 

  return bi_gram

##NER
def remove_ner(sents):

    ##Removing place, person from resume
    ner_labels = ['GPE','ORDINAL','PERSON']
    rem_ner = []

    ner = NER(sents)
    # for tags in ner.ents:
    rem = [tags for tags in ner.ents if tags.label_ in ner_labels]

    s=''
    for i,j in enumerate(rem):
        if i==0:
          s=sents.replace(str(j),'').lstrip()
        else:
          s=s.replace(str(j),'').lstrip()
    rem_ner.append(s)
    return rem_ner[0]

##POS tagging
##get pos tags and remove unwanted ones.
def pos_rem(df):
  # try:
    nlp = StanfordCoreNLP(path_to_corenlp)
    pos_sent = []
    for i, row in df.iterrows():
      try:
        temp =[]
        pos_tags = nlp.pos_tag(row['Resume'].lower())
      
        for tag in pos_tags:
          if tag[1] in ['NNS','NNP','NN','JJ']:
            temp.append(tag[0])
      
      except Exception as e:
        # print(str(e))   
        pass 
    

      pos_sent.append(' '.join(temp))
      
    nlp.close()
    return pos_sent




