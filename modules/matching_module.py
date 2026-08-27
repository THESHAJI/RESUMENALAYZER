"""
===================================================================
MODULE 5: MATCHING ENGINE - Cosine Similarity
===================================================================
Role: Compare resume vs job descriptions using cosine similarity.
Tech: scikit-learn (cosine_similarity), numpy, scipy
===================================================================
"""

from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from scipy.spatial.distance import cdist


def calculate_similarity(resume_vector, job_vectors, job_data, resume_skills=None):
    """
    Calculate similarity between resume and all job descriptions using a hybrid
    engine that combines skill requirement coverage (70%) with TF-IDF cosine similarity (30%).
    
    Args:
        resume_vector: TF-IDF sparse vector for resume
        job_vectors: TF-IDF sparse matrix for jobs
        job_data: list of job dicts from Module 4
        resume_skills: dict {category: [skills]} from Module 2 (optional)
    Returns:
        list of dicts sorted by match_score descending
    """
    print("\n" + "=" * 60)
    print("  MODULE 5: MATCHING ENGINE - Cosine Similarity & Skill Match")
    print("=" * 60)

    # Flatten resume skills into a set for fast lookup
    all_candidate_skills = set()
    if resume_skills:
        for skills in resume_skills.values():
            for s in skills:
                all_candidate_skills.add(s.lower())

    # Calculate cosine similarity (returns array of shape (1, n_jobs))
    similarity_scores = cosine_similarity(resume_vector, job_vectors)
    scores_array = np.array(similarity_scores).flatten()

    # Also compute euclidean distance for additional insight
    resume_dense = np.array(resume_vector.toarray())
    jobs_dense = np.array(job_vectors.toarray())
    euclidean_dists = cdist(resume_dense, jobs_dense, metric='euclidean').flatten()

    # Build ranked results
    results = []
    for i, job in enumerate(job_data):
        raw_cos = float(scores_array[i])
        
        # 1. Skill coverage calculation
        req_skills = set(s.lower() for s in job.get('required_skills', []))
        if req_skills and all_candidate_skills:
            matched_skills = req_skills.intersection(all_candidate_skills)
            skill_coverage = len(matched_skills) / len(req_skills) * 100.0
        else:
            skill_coverage = raw_cos * 100.0

        # 2. Semantic TF-IDF score (normalized against typical max range in resume texts)
        semantic_score = min((raw_cos / 0.25) * 100.0, 100.0)

        # 3. Hybrid AI Match Score (70% skill coverage + 30% semantic context)
        if all_candidate_skills:
            final_match = round(0.70 * skill_coverage + 0.30 * semantic_score, 1)
        else:
            final_match = round(raw_cos * 100, 1)

        results.append({
            'rank': 0,
            'title': job['title'],
            'category': job['category'],
            'match_score': final_match,
            'skill_coverage': round(skill_coverage, 1),
            'cosine_raw': round(raw_cos, 4),
            'euclidean_dist': round(float(euclidean_dists[i]), 4),
            'required_skills': job['required_skills']
        })

    # Sort by match score descending
    results.sort(key=lambda x: x['match_score'], reverse=True)
    for idx, r in enumerate(results):
        r['rank'] = idx + 1

    print(f"  > Compared resume against {len(job_data)} jobs")
    print(f"  > Top match: {results[0]['title']} ({results[0]['match_score']}%)")
    print(f"  > Lowest match: {results[-1]['title']} ({results[-1]['match_score']}%)")
    print(f"\n  {'Rank':<5} {'Job Title':<30} {'Match %':<10}")
    print("  " + "-" * 50)
    for r in results[:5]:
        print(f"  {r['rank']:<5} {r['title']:<30} {r['match_score']:<10}%")

    return results
