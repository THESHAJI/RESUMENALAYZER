"""
===================================================================
MODULE 7: STORAGE MODULE - Data Persistence with Pandas & CSV
===================================================================
Role: Store analysis results, manage history, export reports.
Tech: pandas, csv (Python built-in)
===================================================================
"""

import os
import csv
import json
import hashlib
from datetime import datetime
import pandas as pd
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import RESULTS_DIR


def generate_analysis_id(resume_text):
    """Generate a unique ID for this analysis session."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    text_hash = hashlib.md5(resume_text.encode()).hexdigest()[:8]
    return f"analysis_{timestamp}_{text_hash}"


def save_results(analysis_id, analysis_data, resume_text):
    """
    Save complete analysis results to CSV files using Pandas.
    
    Creates 3 CSV files:
        1. summary.csv - Overall scores and metadata
        2. job_matches.csv - All job match results
        3. skill_gaps.csv - Skill gap analysis details
    
    Args:
        analysis_id: Unique session identifier
        analysis_data: Full analysis dict from Module 6
        resume_text: Original resume text
    Returns:
        dict with file paths of saved files
    """
    print("\n" + "=" * 60)
    print("  MODULE 7: STORAGE - Saving Results to CSV")
    print("=" * 60)

    # Create session directory
    session_dir = os.path.join(RESULTS_DIR, analysis_id)
    os.makedirs(session_dir, exist_ok=True)

    saved_files = {}

    # ─── 1. SUMMARY CSV ───
    summary_data = {
        'analysis_id': [analysis_id],
        'timestamp': [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        'resume_strength': [analysis_data['resume_strength']],
        'total_skills_found': [analysis_data['total_skills']],
        'avg_match_score': [analysis_data['avg_match']],
        'top_match_score': [analysis_data['top_match']],
        'top_match_job': [analysis_data['match_results'][0]['title']],
        'high_matches': [analysis_data['match_distribution']['high']],
        'medium_matches': [analysis_data['match_distribution']['medium']],
        'low_matches': [analysis_data['match_distribution']['low']],
        'categories_covered': [len(analysis_data['resume_skills'])],
        'recommendations_count': [len(analysis_data['recommendations'])]
    }
    summary_df = pd.DataFrame(summary_data)
    summary_path = os.path.join(session_dir, "summary.csv")
    summary_df.to_csv(summary_path, index=False)
    saved_files['summary'] = summary_path
    print(f"  > Saved: summary.csv")

    # ─── 2. JOB MATCHES CSV ───
    matches_data = []
    for job in analysis_data['match_results']:
        matches_data.append({
            'rank': job['rank'],
            'job_title': job['title'],
            'category': job['category'],
            'match_score_pct': job['match_score'],
            'cosine_similarity': job['cosine_raw'],
            'euclidean_distance': job['euclidean_dist'],
            'required_skills': '; '.join(job['required_skills'])
        })
    matches_df = pd.DataFrame(matches_data)
    matches_path = os.path.join(session_dir, "job_matches.csv")
    matches_df.to_csv(matches_path, index=False)
    saved_files['job_matches'] = matches_path
    print(f"  > Saved: job_matches.csv ({len(matches_data)} records)")

    # ─── 3. SKILL GAPS CSV ───
    gaps_data = []
    for gap in analysis_data['skill_gap_analysis']:
        gaps_data.append({
            'job_title': gap['title'],
            'match_score': gap['match_score'],
            'skill_coverage_pct': gap['skill_coverage'],
            'present_skills': '; '.join(gap['present_skills']),
            'missing_skills': '; '.join(gap['missing_skills']),
            'total_required': len(gap['required_skills']),
            'total_present': len(gap['present_skills']),
            'total_missing': len(gap['missing_skills'])
        })
    gaps_df = pd.DataFrame(gaps_data)
    gaps_path = os.path.join(session_dir, "skill_gaps.csv")
    gaps_df.to_csv(gaps_path, index=False)
    saved_files['skill_gaps'] = gaps_path
    print(f"  > Saved: skill_gaps.csv")

    # ─── 4. SKILLS INVENTORY CSV ───
    skills_data = []
    for category, skills in analysis_data['resume_skills'].items():
        for skill in skills:
            skills_data.append({
                'category': category,
                'skill': skill,
                'found_in_resume': 'Yes'
            })
    skills_df = pd.DataFrame(skills_data)
    skills_path = os.path.join(session_dir, "skills_inventory.csv")
    skills_df.to_csv(skills_path, index=False)
    saved_files['skills_inventory'] = skills_path
    print(f"  > Saved: skills_inventory.csv ({len(skills_data)} skills)")

    # ─── 5. RECOMMENDATIONS TXT ───
    rec_path = os.path.join(session_dir, "recommendations.txt")
    with open(rec_path, 'w', encoding='utf-8') as f:
        f.write("=" * 60 + "\n")
        f.write("  CAREER INTELLIGENCE RECOMMENDATIONS\n")
        f.write(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 60 + "\n\n")
        for i, rec in enumerate(analysis_data['recommendations'], 1):
            f.write(f"  {i}. {rec}\n\n")
    saved_files['recommendations'] = rec_path
    print(f"  > Saved: recommendations.txt")

    # ─── 6. MASTER HISTORY (append mode) ───
    history_path = os.path.join(RESULTS_DIR, "analysis_history.csv")
    history_entry = {
        'analysis_id': analysis_id,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'resume_strength': analysis_data['resume_strength'],
        'top_match': analysis_data['match_results'][0]['title'],
        'top_score': analysis_data['top_match'],
        'total_skills': analysis_data['total_skills'],
        'session_path': session_dir
    }
    history_df = pd.DataFrame([history_entry])
    if os.path.exists(history_path):
        history_df.to_csv(history_path, mode='a', header=False, index=False)
    else:
        history_df.to_csv(history_path, index=False)
    print(f"  > Updated: analysis_history.csv (master log)")

    print(f"\n  All files saved to: {session_dir}")
    return saved_files


def load_history():
    """Load analysis history from master CSV."""
    history_path = os.path.join(RESULTS_DIR, "analysis_history.csv")
    if os.path.exists(history_path):
        df = pd.read_csv(history_path)
        return df.to_dict('records')
    return []
