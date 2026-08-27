"""
===================================================================
AI-POWERED SMART RESUME & CAREER INTELLIGENCE SYSTEM
===================================================================
Main Pipeline - Runs all 8 modules in sequence.
Usage: python main.py
===================================================================
"""

import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.input_module import load_resume
from modules.nlp_module import preprocess_resume
from modules.feature_module import create_tfidf_vectors, get_top_keywords
from modules.job_data_module import get_job_database
from modules.matching_module import calculate_similarity
from modules.analysis_module import analyze_results
from modules.storage_module import save_results, generate_analysis_id
from modules.visualization_module import generate_all_charts
from config import SAMPLE_DIR


def run_pipeline(resume_source):
    """
    Execute the complete 8-module pipeline.
    
    Args:
        resume_source: File path or raw text
    Returns:
        dict with all results
    """
    print("\n" + "#" * 60)
    print("#  AI-POWERED SMART RESUME & CAREER INTELLIGENCE SYSTEM  #")
    print("#" * 60)

    # Module 1: Input
    raw_text = load_resume(resume_source)

    # Module 2: NLP Preprocessing
    nlp_result = preprocess_resume(raw_text)

    # Module 3: Feature Engineering (TF-IDF)
    # Module 4: Job Data
    jobs = get_job_database()
    job_texts = [job['description'] for job in jobs]
    tfidf_result = create_tfidf_vectors(nlp_result['processed_text'], job_texts)

    # Show top resume keywords
    top_kw = get_top_keywords(tfidf_result['vectorizer'],
                              tfidf_result['resume_vector'], top_n=10)
    print(f"\n  Top Resume Keywords (TF-IDF):")
    for kw, score in top_kw:
        print(f"    {kw:<25} {score:.4f}")

    # Module 5: Matching Engine
    match_results = calculate_similarity(
        tfidf_result['resume_vector'],
        tfidf_result['job_vectors'],
        jobs,
        nlp_result['skills']
    )

    # Module 6: Analysis
    analysis = analyze_results(match_results, nlp_result['skills'])

    # Module 7: Storage
    analysis_id = generate_analysis_id(raw_text)
    saved_files = save_results(analysis_id, analysis, raw_text)

    # Module 8: Visualization
    charts = generate_all_charts(analysis, analysis_id)

    # Final Summary
    print("\n" + "=" * 60)
    print("  PIPELINE COMPLETE")
    print("=" * 60)
    print(f"  Analysis ID: {analysis_id}")
    print(f"  Resume Strength: {analysis['resume_strength']}/100")
    print(f"  Best Match: {analysis['match_results'][0]['title']} "
          f"({analysis['top_match']}%)")
    print(f"  Charts Generated: {len(charts)}")
    print(f"  Files Saved: {len(saved_files)}")
    print("=" * 60)

    return {
        'analysis_id': analysis_id,
        'analysis': analysis,
        'charts': charts,
        'saved_files': saved_files,
        'nlp_result': nlp_result,
        'tfidf_result': tfidf_result
    }


def main():
    """Entry point - Interactive CLI mode."""
    print("\n" + "=" * 60)
    print("  SMART RESUME & CAREER INTELLIGENCE SYSTEM")
    print("  Select input method:")
    print("  1. Use sample resume (demo)")
    print("  2. Enter file path (.txt)")
    print("  3. Paste resume text")
    print("  4. Launch GUI (PyQt5)")
    print("=" * 60)

    choice = input("\n  Enter choice (1/2/3/4): ").strip()

    if choice == '1':
        sample = os.path.join(SAMPLE_DIR, "sample_resume.txt")
        if os.path.exists(sample):
            run_pipeline(sample)
        else:
            print("  ERROR: Sample resume not found!")
    elif choice == '2':
        path = input("  Enter file path: ").strip().strip('"')
        if os.path.exists(path):
            run_pipeline(path)
        else:
            print(f"  ERROR: File not found: {path}")
    elif choice == '3':
        print("  Paste your resume text (type END on a new line to finish):")
        lines = []
        while True:
            line = input()
            if line.strip().upper() == 'END':
                break
            lines.append(line)
        text = '\n'.join(lines)
        if text.strip():
            run_pipeline(text)
        else:
            print("  ERROR: No text entered!")
    elif choice == '4':
        print("  Launching GUI...")
        from gui import launch_gui
        launch_gui()
    else:
        print("  Invalid choice. Using sample resume...")
        sample = os.path.join(SAMPLE_DIR, "sample_resume.txt")
        run_pipeline(sample)


if __name__ == "__main__":
    main()
