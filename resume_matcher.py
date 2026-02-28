import re
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

SKILLS = [
    "python", "machine learning", "sql", "data analysis",
    "deep learning", "nlp", "flask", "pandas", "numpy",
    "tensorflow", "power bi", "excel"
]

def clean_text(text):
    text = text.lower()
    text = re.sub(r"\d+", " ", text)
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = re.sub(r"\s+", " ", text).strip()
    return text

def extract_skills(text):
    return [skill for skill in SKILLS if skill in text]

def calculate_match(resume_text, job_desc):
    resume_text = clean_text(resume_text)
    job_desc = clean_text(job_desc)

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([resume_text, job_desc])

    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    score = round(similarity[0][0] * 100, 2)

    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(job_desc)

    matched = list(set(resume_skills) & set(jd_skills))
    missing = list(set(jd_skills) - set(resume_skills))

    return score, matched, missing

def rank_resumes(resume_list, job_desc):
    results = []

    for idx, resume in enumerate(resume_list):
        score, matched, missing = calculate_match(resume, job_desc)

        results.append({
            "resume_id": f"Resume {idx+1}",
            "score": score,
            "matched_skills": matched,
            "missing_skills": missing
        })

    results = sorted(results, key=lambda x: x["score"], reverse=True)
    return results