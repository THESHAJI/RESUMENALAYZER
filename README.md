# AI-Powered Smart Resume & Career Intelligence System

An award-winning, modular AI system that analyzes resumes, extracts skills using NLP,
matches against job roles using machine learning, identifies skill gaps, and delivers
actionable career insights through stunning visualizations.

---

## Features

- **8-Module Pipeline Architecture** — fully modular, extensible design
- **NLP Text Processing** — NLTK tokenization, stopword removal, lemmatization (with offline fallback)
- **TF-IDF Vectorization** — sklearn with bigram support for precise matching
- **Cosine Similarity Matching** — ranked comparison against 15 real-world job roles
- **Skill Gap Analysis** — numpy-powered scoring showing exactly what you're missing
- **Career Recommendations** — actionable suggestions for each candidate
- **Pandas CSV Storage** — 6 output files per analysis + master history log
- **5 Premium Charts** — bar, donut, radar, grouped bar, pie with dark theme
- **PyQt5 Desktop GUI** — premium dark-themed app with tabbed dashboard
- **CLI Mode** — also runs fully from the command line

---

## Libraries Used

| Library | Version | Purpose |
|---------|---------|---------|
| `nltk` | latest | NLP: tokenization, stopwords, lemmatization |
| `scikit-learn` | latest | TF-IDF vectorization, cosine similarity |
| `matplotlib` | latest | 5 chart types for visualization |
| `numpy` | latest | Numerical scoring, statistical analysis |
| `pandas` | latest | CSV storage, DataFrames, history tracking |
| `scipy` | latest | Euclidean distance for matching depth |
| `PyQt5` | latest | Premium desktop GUI with dark theme |

---

## Project Structure

```
Resumeanalyzer/
├── main.py                        # CLI entry point (all 8 modules)
├── gui.py                         # PyQt5 desktop GUI
├── gui_styles.py                  # Dark theme stylesheet
├── config.py                      # Skill database, paths, thresholds
├── requirements.txt               # All dependencies
│
├── modules/
│   ├── input_module.py            # Module 1: TXT/PDF/raw text input
│   ├── nlp_module.py              # Module 2: NLTK NLP preprocessing
│   ├── feature_module.py          # Module 3: TF-IDF vectorization
│   ├── job_data_module.py         # Module 4: 15 curated job roles
│   ├── matching_module.py         # Module 5: cosine + euclidean similarity
│   ├── analysis_module.py         # Module 6: skill gap + career scoring
│   ├── storage_module.py          # Module 7: pandas CSV storage
│   └── visualization_module.py   # Module 8: 5 matplotlib charts
│
├── data/
│   ├── sample_resumes/
│   │   └── sample_resume.txt      # Demo resume for testing
│   └── results/                   # Analysis output (auto-created)
│
└── uploads/                       # Temp upload directory
```

---

## How to Run

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Launch GUI (Recommended)
```bash
python gui.py
```

### 3. CLI Mode
```bash
python main.py
```
Then select:
- `1` — Run with sample resume (instant demo)
- `2` — Browse to your own `.txt` resume file
- `3` — Paste raw resume text
- `4` — Launch the GUI

---

## Data Flow

```
Resume (TXT/PDF/Text)
    |
    v
Module 1: Input      -> extracts raw text
    |
    v
Module 2: NLP        -> cleans, tokenizes, lemmatizes, extracts skills
    |
    v
Module 3: TF-IDF     -> converts text to numerical vectors (sklearn)
    |
    v
Module 4: Job Data   -> loads 15 curated job descriptions
    |
    v
Module 5: Matching   -> cosine_similarity + euclidean distance (scipy)
    |
    v
Module 6: Analysis   -> match scores, skill gaps, recommendations (numpy)
    |
    v
Module 7: Storage    -> saves 6 CSV files + master history (pandas)
    |
    v
Module 8: Charts     -> 5 dark-themed Matplotlib visualizations
    |
    v
PyQt5 Dashboard      -> tabbed GUI with score cards + embedded charts
```

---

## Output Files (per analysis)

| File | Contents |
|------|----------|
| `summary.csv` | Overall scores and metadata |
| `job_matches.csv` | All 15 job match scores |
| `skill_gaps.csv` | Present/missing skills per role |
| `skills_inventory.csv` | All skills found in resume |
| `recommendations.txt` | Career improvement advice |
| `chart_*.png` | 5 visualization charts |

---

## Architecture Design Patterns

- **Modular Pipeline** — each module is independent and reusable
- **Offline Resilient** — NLP module has full fallback if NLTK data unavailable
- **Data-Driven** — all decisions based on numerical scores
- **Extensible** — add new job roles to `job_data_module.py` easily
