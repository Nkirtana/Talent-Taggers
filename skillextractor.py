import os
import re
from tqdm.auto import tqdm
from collections import Counter

import spacy
import pandas as pd
from spacy.matcher import Matcher, PhraseMatcher

basedir = os.path.abspath(os.path.dirname(__file__))
skill_path = os.path.join(basedir, 'skilldb', 'all_skills.csv')


class ExtractSkills:

    def __init__(self):
        try:
            # loading spacy english medium core model
            self.nlp = spacy.load("en_core_web_md")
        except OSError:
            os.system('python -m spacy download en_core_web_md')
            self.nlp = spacy.load("en_core_web_md")
        # loading all the skills in the database
        # self.skill_list = pd.read_excel(skill_path).skills.tolist()

        self.skill_list = pd.read_csv(skill_path).skills.tolist()

        # Cleaning the skills database
        self.skill_list = [str(skill) for skill in self.skill_list if self.skill_check(str(skill))]
        self.skill_list = sorted(self.skill_list, key=lambda x: -len(x))

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
        remove_idx = []
        for match_str_id, i, j in self.phrase_matcher(input_text_docs):
            if len(matches) == 0:
                matches.append((self.nlp.vocab.strings[match_str_id], i, j))
            else:
                new_entry = True
                for idx, (match_prev, i_prev, j_prev) in enumerate(matches):
                    if i_prev == i:
                        if j_prev < j:
                            new_entry = False
                            remove_idx.append(idx)
                            matches.append((self.nlp.vocab.strings[match_str_id], i, j))
                if new_entry:
                    matches.append((self.nlp.vocab.strings[match_str_id], i, j))

        matches_skills = []
        for idx, (match_str, i, j) in enumerate(matches):
            if idx not in remove_idx:
                matches_skills.append(match_str)

        skill_counts = Counter(matches_skills)

        return skill_counts

