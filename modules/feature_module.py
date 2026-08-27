"""
===================================================================
MODULE 3: FEATURE ENGINEERING - TF-IDF Vectorization
===================================================================
Role: Convert text into numerical feature vectors using TF-IDF.
Tech: scikit-learn (TfidfVectorizer), numpy, scipy
===================================================================
"""

from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import TFIDF_MAX_FEATURES, TFIDF_NGRAM_RANGE


def create_tfidf_vectors(resume_text, job_texts):
    """
    Convert resume and job description texts into TF-IDF vectors.
    
    Args:
        resume_text (str): Preprocessed resume text
        job_texts (list): List of job description texts
    Returns:
        dict with vectorizer, resume_vector, job_vectors, feature info
    """
    print("\n" + "=" * 60)
    print("  MODULE 3: FEATURE ENGINE - TF-IDF Vectorization")
    print("=" * 60)

    all_documents = [resume_text] + job_texts

    vectorizer = TfidfVectorizer(
        max_features=TFIDF_MAX_FEATURES,
        ngram_range=TFIDF_NGRAM_RANGE,
        stop_words='english',
        sublinear_tf=True,
        smooth_idf=True
    )

    tfidf_matrix = vectorizer.fit_transform(all_documents)
    resume_vector = tfidf_matrix[0:1]
    job_vectors = tfidf_matrix[1:]
    feature_names = vectorizer.get_feature_names_out()

    print(f"  > Vocabulary size: {len(feature_names)} features")
    print(f"  > Resume vector shape: {resume_vector.shape}")
    print(f"  > Job vectors shape: {job_vectors.shape}")

    return {
        'vectorizer': vectorizer,
        'resume_vector': resume_vector,
        'job_vectors': job_vectors,
        'feature_names': list(feature_names),
        'n_features': len(feature_names)
    }


def get_top_keywords(vectorizer, vector, top_n=15):
    """Extract top N important keywords from a TF-IDF vector."""
    feature_names = vectorizer.get_feature_names_out()
    dense = np.array(vector.toarray()).flatten()
    top_indices = dense.argsort()[-top_n:][::-1]
    results = []
    for idx in top_indices:
        if dense[idx] > 0:
            results.append((feature_names[idx], round(float(dense[idx]), 4)))
    return results
