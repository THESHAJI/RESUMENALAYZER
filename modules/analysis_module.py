"""
===================================================================
MODULE 6: ANALYSIS MODULE - Skill Gap & Scoring
===================================================================
Role: Calculate match scores, find missing skills, give suggestions.
Tech: numpy for numerical scoring
===================================================================
"""

import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import HIGH_MATCH_THRESHOLD, MEDIUM_MATCH_THRESHOLD, LOW_MATCH_THRESHOLD


def analyze_results(match_results, resume_skills):
    """
    Perform deep analysis: skill gaps, resume strength, suggestions.
    
    Args:
        match_results: list of dicts from Module 5
        resume_skills: dict {category: [skills]} from Module 2
    Returns:
        dict with full analysis data
    """
    print("\n" + "=" * 60)
    print("  MODULE 6: ANALYSIS - Skill Gap & Career Intelligence")
    print("=" * 60)

    # Flatten all resume skills into a set
    all_resume_skills = set()
    for skills in resume_skills.values():
        for s in skills:
            all_resume_skills.add(s.lower())

    # --- Skill Gap Analysis for top 5 jobs ---
    skill_gap_analysis = []
    for job in match_results[:5]:
        required = set(s.lower() for s in job['required_skills'])
        present = required.intersection(all_resume_skills)
        missing = required - all_resume_skills
        coverage = (len(present) / len(required) * 100) if required else 0

        skill_gap_analysis.append({
            'title': job['title'],
            'match_score': job['match_score'],
            'required_skills': list(required),
            'present_skills': list(present),
            'missing_skills': list(missing),
            'skill_coverage': round(coverage, 1)
        })

    # --- Resume Strength Score (weighted) ---
    scores_arr = np.array([j['match_score'] for j in match_results])
    total_skills = sum(len(v) for v in resume_skills.values())
    num_categories = len(resume_skills)

    skill_breadth_score = min(num_categories / 7 * 100, 100)
    skill_depth_score = min(total_skills / 20 * 100, 100)
    avg_match = float(np.mean(scores_arr))
    top_match = float(np.max(scores_arr))
    match_consistency = float(np.std(scores_arr))

    resume_strength = round(
        skill_breadth_score * 0.20 +
        skill_depth_score * 0.25 +
        avg_match * 0.25 +
        top_match * 0.30, 1
    )

    # --- Career Recommendations ---
    recommendations = []
    if top_match >= HIGH_MATCH_THRESHOLD:
        recommendations.append(
            f"EXCELLENT: Strong match for '{match_results[0]['title']}' "
            f"({match_results[0]['match_score']}%). You are well-suited for this role."
        )
    elif top_match >= MEDIUM_MATCH_THRESHOLD:
        recommendations.append(
            f"GOOD: Moderate match for '{match_results[0]['title']}'. "
            f"Focus on filling skill gaps to strengthen your profile."
        )
    else:
        recommendations.append(
            "NEEDS IMPROVEMENT: Your resume has low similarity to available roles. "
            "Consider adding more relevant technical skills."
        )

    # Suggest skills to learn
    all_missing = set()
    for gap in skill_gap_analysis[:3]:
        all_missing.update(gap['missing_skills'])
    if all_missing:
        top_missing = list(all_missing)[:8]
        recommendations.append(
            f"SKILLS TO LEARN: {', '.join(top_missing)}"
        )

    # Category-specific advice
    if "Programming Languages" not in resume_skills:
        recommendations.append(
            "TIP: Add programming languages to your resume (Python, Java, JavaScript)."
        )
    if "Cloud & DevOps" not in resume_skills:
        recommendations.append(
            "TIP: Cloud skills (AWS, Docker, Kubernetes) are highly in-demand."
        )
    if "Soft Skills" not in resume_skills:
        recommendations.append(
            "TIP: Include soft skills like leadership, communication, and teamwork."
        )

    # --- Match Distribution ---
    high_matches = int(np.sum(scores_arr >= HIGH_MATCH_THRESHOLD))
    medium_matches = int(np.sum((scores_arr >= MEDIUM_MATCH_THRESHOLD) & (scores_arr < HIGH_MATCH_THRESHOLD)))
    low_matches = int(np.sum((scores_arr >= LOW_MATCH_THRESHOLD) & (scores_arr < MEDIUM_MATCH_THRESHOLD)))
    poor_matches = int(np.sum(scores_arr < LOW_MATCH_THRESHOLD))

    # Print analysis summary
    print(f"\n  RESUME STRENGTH SCORE: {resume_strength}/100")
    print(f"  Skills Found: {total_skills} across {num_categories} categories")
    print(f"  Avg Match: {avg_match:.1f}% | Top Match: {top_match:.1f}%")
    print(f"  Match Distribution: {high_matches} high, {medium_matches} medium, "
          f"{low_matches} low, {poor_matches} poor")

    print(f"\n  SKILL GAP ANALYSIS (Top 3 Roles):")
    for gap in skill_gap_analysis[:3]:
        print(f"    {gap['title']}:")
        print(f"      Coverage: {gap['skill_coverage']}%")
        if gap['present_skills']:
            print(f"      Present: {', '.join(gap['present_skills'])}")
        if gap['missing_skills']:
            print(f"      Missing: {', '.join(gap['missing_skills'])}")

    print(f"\n  RECOMMENDATIONS:")
    for rec in recommendations:
        print(f"    > {rec}")

    return {
        'match_results': match_results,
        'skill_gap_analysis': skill_gap_analysis,
        'resume_strength': resume_strength,
        'resume_skills': resume_skills,
        'total_skills': total_skills,
        'avg_match': round(avg_match, 1),
        'top_match': round(top_match, 1),
        'match_consistency': round(match_consistency, 2),
        'match_distribution': {
            'high': high_matches,
            'medium': medium_matches,
            'low': low_matches,
            'poor': poor_matches
        },
        'recommendations': recommendations
    }
