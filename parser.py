import re
import spacy

# Load the English spaCy model
nlp = spacy.load('en_core_web_sm')

def extract_email(text):
    email_pattern = r'[\w\.-]+@[\w\.-]+\.\w+'
    matches = re.findall(email_pattern, text)
    return matches[0] if matches else None

def extract_phone(text):
    phone_pattern = r'(\+?\d{1,3}[\s\-]?)?(\(?\d{3}\)?[\s\-]?)?\d{3}[\s\-]?\d{4}'
    matches = re.findall(phone_pattern, text)
    if matches:
        number = ''.join(matches[0])
        return number.strip()
    return None

def extract_skills(text, skill_set):
    """
    Extracts skills by comparing lemmatized tokens in resume text to the skill set.
    Supports single-word matching; consider using PhraseMatcher for multi-word support.
    """
    doc = nlp(text.lower())
    tokens = set([token.lemma_ for token in doc if token.is_alpha and not token.is_stop])
    matched_skills = list(skill_set.intersection(tokens))
    return matched_skills
