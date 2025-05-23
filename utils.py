import pandas as pd
import spacy

# Load the English model
nlp = spacy.load('en_core_web_sm')

def clean_and_tokenize(text):
    doc = nlp(str(text))
    tokens = [token.lemma_.lower() for token in doc 
              if token.is_alpha and not token.is_stop]
    return tokens

def load_dataset(path='data/UpdatedResumeDataSet.csv'):
    df = pd.read_csv(path)
    df['Skills_list'] = df['Resume'].apply(clean_and_tokenize)
    df['Role'] = df['Category']  # For compatibility with prediction
    return df

def predict_job_role(extracted_skills, df):
    extracted_skills = set([s.lower() for s in extracted_skills])
    best_role = None
    max_match = 0
    for _, row in df.iterrows():
        role_skills = set(row['Skills_list'])
        matches = len(extracted_skills.intersection(role_skills))
        if matches > max_match:
            max_match = matches
            best_role = row['Role']
    return best_role if best_role else "No matching role found"

# Example to run once spaCy model is installed:
# python -m spacy download en_core_web_sm
