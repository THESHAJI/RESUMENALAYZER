"""
Configuration constants for the Resume Analyzer system.
"""

import os

# ──────────────────────────────────────────────
# PATHS
# ──────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
RESULTS_DIR = os.path.join(DATA_DIR, "results")
UPLOADS_DIR = os.path.join(BASE_DIR, "uploads")
SAMPLE_DIR = os.path.join(DATA_DIR, "sample_resumes")

# Create directories if they don't exist
for directory in [DATA_DIR, RESULTS_DIR, UPLOADS_DIR, SAMPLE_DIR]:
    os.makedirs(directory, exist_ok=True)

# ──────────────────────────────────────────────
# SKILL CATEGORIES (used for extraction & analysis)
# ──────────────────────────────────────────────
SKILL_DATABASE = {
    "Programming Languages": [
        "python", "java", "javascript", "c++", "c#", "ruby", "go", "rust",
        "php", "swift", "kotlin", "typescript", "scala", "r", "matlab",
        "perl", "shell", "bash", "sql", "html", "css"
    ],
    "Data Science & ML": [
        "machine learning", "deep learning", "neural network", "tensorflow",
        "pytorch", "keras", "scikit-learn", "pandas", "numpy", "scipy",
        "data analysis", "data visualization", "statistics", "nlp",
        "natural language processing", "computer vision", "regression",
        "classification", "clustering", "random forest", "xgboost",
        "data mining", "feature engineering", "model training",
        "artificial intelligence", "reinforcement learning"
    ],
    "Web Development": [
        "react", "angular", "vue", "node.js", "express", "django", "flask",
        "spring boot", "rest api", "graphql", "html5", "css3", "bootstrap",
        "tailwind", "webpack", "next.js", "fastapi", "asp.net"
    ],
    "Cloud & DevOps": [
        "aws", "azure", "gcp", "google cloud", "docker", "kubernetes",
        "jenkins", "ci/cd", "terraform", "ansible", "linux", "nginx",
        "microservices", "serverless", "cloud computing", "devops"
    ],
    "Databases": [
        "mysql", "postgresql", "mongodb", "redis", "elasticsearch",
        "oracle", "sql server", "sqlite", "cassandra", "dynamodb",
        "firebase", "neo4j"
    ],
    "Tools & Platforms": [
        "git", "github", "gitlab", "jira", "confluence", "slack",
        "vs code", "intellij", "jupyter", "postman", "figma",
        "tableau", "power bi", "excel"
    ],
    "Soft Skills": [
        "leadership", "communication", "teamwork", "problem solving",
        "critical thinking", "project management", "agile", "scrum",
        "time management", "collaboration", "mentoring", "presentation"
    ]
}

# ──────────────────────────────────────────────
# TF-IDF CONFIGURATION
# ──────────────────────────────────────────────
TFIDF_MAX_FEATURES = 5000
TFIDF_NGRAM_RANGE = (1, 2)

# ──────────────────────────────────────────────
# MATCHING THRESHOLDS
# ──────────────────────────────────────────────
HIGH_MATCH_THRESHOLD = 70    # % — Excellent match
MEDIUM_MATCH_THRESHOLD = 45  # % — Good match
LOW_MATCH_THRESHOLD = 25     # % — Weak match
