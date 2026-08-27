"""
===================================================================
MODULE 2: NLP MODULE - Text Preprocessing using NLTK
===================================================================
Role: Clean text, tokenize, remove stopwords, lemmatize,
      and extract skills from resume text.
Tech: NLTK (with full offline fallback support)
===================================================================
"""

import re
import nltk
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import SKILL_DATABASE

# ── Built-in English stopwords (offline fallback) ──────────────
FALLBACK_STOPWORDS = {
    'i','me','my','myself','we','our','ours','ourselves','you','your',
    'yours','yourself','yourselves','he','him','his','himself','she',
    'her','hers','herself','it','its','itself','they','them','their',
    'theirs','themselves','what','which','who','whom','this','that',
    'these','those','am','is','are','was','were','be','been','being',
    'have','has','had','having','do','does','did','doing','a','an',
    'the','and','but','if','or','because','as','until','while','of',
    'at','by','for','with','about','against','between','into','through',
    'during','before','after','above','below','to','from','up','down',
    'in','out','on','off','over','under','again','further','then',
    'once','here','there','when','where','why','how','all','both',
    'each','few','more','most','other','some','such','no','nor','not',
    'only','own','same','so','than','too','very','s','t','can','will',
    'just','don','should','now','d','ll','m','o','re','ve','y','ain',
    'aren','couldn','didn','doesn','hadn','hasn','haven','isn','ma',
    'mightn','mustn','needn','shan','shouldn','wasn','weren','won',
    'wouldn','resume','curriculum','vitae','name','address','phone',
    'email','date','birth','gender','nationality','page','objective',
    'reference','available','upon','request','also','would','could',
    'may','one','two','three','four','five','six','seven','eight',
    'nine','ten','new','use','used','using','work','worked','working'
}


def _ensure_nltk_data():
    """
    Try to load NLTK data. If unavailable, mark for fallback mode.
    Never raises - always returns gracefully.
    """
    global _nltk_punkt, _nltk_stopwords, _nltk_wordnet
    _nltk_punkt = False
    _nltk_stopwords = False
    _nltk_wordnet = False

    # punkt_tab
    for tok_name in ['punkt_tab', 'punkt']:
        try:
            nltk.data.find(f'tokenizers/{tok_name}')
            _nltk_punkt = True
            break
        except LookupError:
            try:
                nltk.download(tok_name, quiet=True)
                _nltk_punkt = True
                break
            except Exception:
                pass

    # stopwords
    try:
        nltk.data.find('corpora/stopwords')
        _nltk_stopwords = True
    except LookupError:
        try:
            nltk.download('stopwords', quiet=True)
            _nltk_stopwords = True
        except Exception:
            pass

    # wordnet
    try:
        nltk.data.find('corpora/wordnet')
        _nltk_wordnet = True
    except LookupError:
        try:
            nltk.download('wordnet', quiet=True)
            _nltk_wordnet = True
        except Exception:
            pass

    return _nltk_punkt, _nltk_stopwords, _nltk_wordnet


# Run once at import
_nltk_punkt, _nltk_stopwords, _nltk_wordnet = False, False, False
_ensure_nltk_data()


def clean_text(text):
    """
    Clean raw resume text by removing noise.
    Steps: lowercase → remove URLs/emails/phones → strip special chars
    """
    text = text.lower()
    text = re.sub(r'http[s]?://\S+', '', text)
    text = re.sub(r'www\.\S+', '', text)
    text = re.sub(r'\S+@\S+\.\S+', '', text)
    text = re.sub(r'[\+]?[\d\-\(\)\s]{10,}', ' ', text)
    text = re.sub(r'[^a-zA-Z0-9\s\-/\+\#\.]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def tokenize_text(text):
    """
    Tokenize using NLTK if available, else split on whitespace.
    """
    if _nltk_punkt:
        try:
            from nltk.tokenize import word_tokenize
            return word_tokenize(text)
        except Exception:
            pass
    # Fallback: simple whitespace + punctuation split
    tokens = re.findall(r"[a-zA-Z][a-zA-Z0-9\-\.\/\+\#]*", text)
    return tokens


def remove_stopwords(tokens):
    """
    Remove stopwords using NLTK corpus if available, else use built-in set.
    """
    if _nltk_stopwords:
        try:
            from nltk.corpus import stopwords
            stop_words = set(stopwords.words('english'))
            stop_words.update(FALLBACK_STOPWORDS)
        except Exception:
            stop_words = FALLBACK_STOPWORDS
    else:
        stop_words = FALLBACK_STOPWORDS

    return [t for t in tokens if t.lower() not in stop_words and len(t) > 1]


def lemmatize_tokens(tokens):
    """
    Lemmatize using NLTK WordNet if available, else return tokens as-is.
    """
    if _nltk_wordnet:
        try:
            from nltk.stem import WordNetLemmatizer
            lem = WordNetLemmatizer()
            return [lem.lemmatize(t) for t in tokens]
        except Exception:
            pass
    # Fallback: simple suffix stripping
    result = []
    for token in tokens:
        t = token.lower()
        for suffix in ['ing', 'tion', 'ed', 'er', 'ly', 'ment', 'ness']:
            if t.endswith(suffix) and len(t) > len(suffix) + 2:
                t = t[:-len(suffix)]
                break
        result.append(t)
    return result


def extract_skills(text):
    """
    Extract recognized skills from resume text using exact word/boundary matching.
    Avoids false positive substring matches (e.g., 'r' inside 'learning', 'go' inside 'algorithm').
    """
    found_skills = {}
    text_lower = " " + text.lower() + " "
    for category, skills in SKILL_DATABASE.items():
        matched = []
        for s in skills:
            s_clean = s.lower()
            pattern = r'(?<![a-zA-Z0-9])' + re.escape(s_clean) + r'(?![a-zA-Z0-9])'
            if re.search(pattern, text_lower):
                matched.append(s)
        if matched:
            found_skills[category] = matched
    return found_skills


def preprocess_resume(raw_text):
    """
    Main NLP pipeline: Raw Text -> Clean -> Tokenize -> Stopwords -> Lemmatize
    Also extracts skills separately using keyword matching.
    
    Returns:
        dict with cleaned_text, tokens, processed_text, skills, total_skills_found
    """
    print("\n" + "=" * 60)
    print("  MODULE 2: NLP - Preprocessing Resume Text")
    print("=" * 60)

    mode = []
    if _nltk_punkt:    mode.append("punkt")
    if _nltk_stopwords: mode.append("stopwords")
    if _nltk_wordnet:  mode.append("wordnet")
    if mode:
        print(f"  > NLTK data available: {', '.join(mode)}")
    else:
        print("  > NLTK data unavailable - using built-in fallback (fully functional)")

    # Step 1: Clean
    cleaned = clean_text(raw_text)
    print(f"  > Text cleaned ({len(raw_text)} -> {len(cleaned)} chars)")

    # Step 2: Tokenize
    tokens = tokenize_text(cleaned)
    print(f"  > Tokenized: {len(tokens)} tokens")

    # Step 3: Remove stopwords
    filtered = remove_stopwords(tokens)
    print(f"  > Stopwords removed: {len(tokens)} -> {len(filtered)} tokens")

    # Step 4: Lemmatize
    lemmatized = lemmatize_tokens(filtered)
    print(f"  > Lemmatization complete")

    # Step 5: Extract skills (uses raw text for better multi-word matching)
    skills = extract_skills(raw_text)
    total_skills = sum(len(v) for v in skills.values())
    print(f"  > Skills extracted: {total_skills} skills across {len(skills)} categories")
    for category, skill_list in skills.items():
        print(f"      {category}: {', '.join(skill_list)}")

    processed_text = ' '.join(lemmatized)
    return {
        'cleaned_text': cleaned,
        'tokens': lemmatized,
        'processed_text': processed_text,
        'skills': skills,
        'total_skills_found': total_skills
    }
