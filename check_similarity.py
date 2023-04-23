from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sentence_transformers import SentenceTransformer
from datacleaning import CleanData

sbert_model = SentenceTransformer('bert-base-nli-mean-tokens')


class CheckSimilarity:
    def __init__(self, resume_skills, jd_skills, resume_text, jd_text):

        self.resume_skills = resume_skills
        self.jd_skills = jd_skills
        self.resume_text = resume_text

        cd = CleanData(keep_stopwords=False, keep_punctuation=False)
        cd.initialize_text(resume_text)
        cd.clean_text()
        self.resume_text = cd.output['output_text']

        cd.initialize_text(jd_text)
        cd.clean_text()
        self.jd_text = cd.output['output_text']

    def matching_skills(self):

        skills_intersection = set(self.jd_skills).intersection(set(self.resume_skills))
        skills_missing = set(self.jd_skills).difference(set(self.resume_skills))

        return {"resume": sorted(self.resume_skills), "jd": sorted(self.jd_skills),
                "Matching skills": sorted(list(skills_intersection)),
                "missing skills": sorted(list(skills_missing)),
                "Score": (len(skills_intersection)*100)/len(self.jd_skills)}

    def bert_embeddings(self):
        corpus = [self.jd_text, self.resume_text]
        document_embeddings = sbert_model.encode(corpus)
        cosine_similarity_score = cosine_similarity(document_embeddings)

        return round(cosine_similarity_score[0][1], 2)*100

    def tfidf_embeddings(self):
        corpus = [self.jd_text, self.resume_text]
        vectorizer = TfidfVectorizer()
        corpus_embedded = vectorizer.fit_transform(corpus)
        cosine_similarity_score = cosine_similarity(corpus_embedded[0], corpus_embedded[1])
        return round(cosine_similarity_score[0][0], 2)*100

    def all_scores(self):
        output = {"skill_match": [self.matching_skills()],
                  "bert_Score": self.bert_embeddings(),
                  "tfidf_score": self.tfidf_embeddings()}

        return output


