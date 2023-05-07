from prep import *
import pandas as pd
import os
from nltk.corpus import stopwords
from string import punctuation

def preprocessing():
    ##Defines Stopwords
    stop_words = set(stopwords.words('english'))

    ##Defines punctuation
    punct = punctuation + '()●xx%•'

    ##Path to data file
    path = os.getcwd()+'/preprocessing/Data/Resume.csv'

    ##Reading the data to a dataframe for processing
    df = pd.read_csv(path)

    ## Joining hypen terms before POS tagging and removing tabs,spaces
    for i, row in df.iterrows():
      row['Resume']=row['Resume'].replace('-','').replace('â¢',' ').replace('\n' ,' ').replace('\t',' ').replace('\r',' ').strip()

    ##POS tags identifying and removal
    pos_sent = pos_rem(df)
    df['cleaned_resume'] = pos_sent

    ##remove ner
    for i, row in df.iterrows():
      df.at[i, 'cleaned_resume'] = remove_ner(row['cleaned_resume'])

    # Tokenize the text
    tokenized_docs = [doc.split() for doc in df.cleaned_resume]

    ##Removing stopwords and punctuations
    final =[]
    for doc in tokenized_docs:
      output = []
      for word in doc:
        if word not in stop_words and word not in punct and not word.isdigit():
            output.append(word.lower().strip(punctuation))
      final.append(output)

    ##Creating ngrams
    bi_grams = generate_uni_bigram(final)

    ##Including unigrams
    final_gram =[]
    for i,val in enumerate(bi_grams):
      val.extend(final[i])
      final_gram.append(val)

    df['cleaned_resume'] = final_gram 
    for i,val in enumerate(final):
      df.at[i,'cleaned_sent'] = ' '.join(val)

    return df

if __name__ == '__main__':
  output = preprocessing()
  ##Writing the processed data to a pickle file for Guided Topic modeling input
  output.to_pickle("./data.pkl")  

