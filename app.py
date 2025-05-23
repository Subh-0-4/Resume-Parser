from flask import Flask, request, render_template, jsonify
from parser import extract_email, extract_phone, extract_skills
from utils import load_dataset, predict_job_role
import webbrowser
import threading

app = Flask(__name__)
df = load_dataset()

# Prepare skill set from dataset
skill_set = set()
for skills in df['Skills_list']:
    skill_set.update(skills)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/parse_resume', methods=['POST'])
def parse_resume():
    data = request.json
    resume_text = data.get('resume_text', '')

    email = extract_email(resume_text)
    phone = extract_phone(resume_text)
    skills = extract_skills(resume_text, skill_set)
    job_role = predict_job_role(skills, df)

    response = {
        'email': email,
        'phone': phone,
        'skills': skills,
        'predicted_job_role': job_role
    }
    return jsonify(response)

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000")

if __name__ == '__main__':
    threading.Timer(1.25, open_browser).start()  # Delay to allow server startup
    app.run(debug=True)

