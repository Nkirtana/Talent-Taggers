import os
import re
from tqdm.auto import tqdm
from collections import Counter

import spacy
import pandas as pd
from spacy.matcher import Matcher, PhraseMatcher

basedir = os.path.abspath(os.path.dirname(__file__))
skill_path = os.path.join(basedir, 'skilldb', 'all_skills.xlsx')


class ExtractSkills:

    def __init__(self):
        try:
            # loading spacy english medium core model
            self.nlp = spacy.load("en_core_web_md")
        except OSError:
            os.system('python -m spacy download en_core_web_md')
            self.nlp = spacy.load("en_core_web_md")
        # loading all the skills in the database
        self.skill_list = pd.read_excel(skill_path).skills.tolist()
        # Cleaning the skills database
        self.skill_list = [str(skill) for skill in self.skill_list if self.skill_check(str(skill))]

        # loading spacy document for each skill
        self.skill_list_docs = list()
        for doc in tqdm(self.nlp.pipe(self.skill_list, batch_size=5000), total=len(self.skill_list)):
            self.skill_list_docs.append(doc)

        # initializing phrasematcher for all the skills
        self.phrase_matcher = PhraseMatcher(self.nlp.vocab)
        for skill, skill_doc in tqdm(zip(self.skill_list, self.skill_list_docs), total=len(self.skill_list)):
            self.phrase_matcher.add(skill, [skill_doc])

    @staticmethod
    def skill_check(skill: str):
        if skill.isnumeric():
            return False
        digit_match = "".join(re.findall("\d+", skill))
        if (len(digit_match)/len(skill)) > 0.65:
            return False
        return True

    def return_skills(self, input_text):
        input_text_docs = self.nlp(input_text)
        matches = []
        for match_str_id, i, j in self.phrase_matcher(input_text_docs):
            matches.append(self.nlp.vocab.strings[match_str_id])
        skill_counts = Counter(matches)

        return skill_counts

