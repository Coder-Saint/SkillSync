import sys
import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
import database as db
import PyPDF2
from google import genai

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join('static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialize the database
db.init_db()


try:
   
    client = genai.Client(api_key="API KEY")
except Exception as e:
    client = None

# --- GLOBAL STATE MVP ---
CURRENT_USER_EMAIL = "guest@example.com"

def get_default_state():
    return {
        "name": "",
        "scores": [0, 0, 0, 0, 0],
        "overall_match": 0,
        "strength": "Pending Assessment...",
        "weakness": "Pending Assessment...",
        "ai_insight": "Take the Career Assessment Test to generate your AI Action Plan.",
        "parsed_skills": "Not provided",
        "education": "Not provided",
        "experience": "Not provided",
        "resume_path": "", 
        "pfp_path": "" 
    }

USER_STATE = get_default_state()

# --- ROUTES ---

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('login.html')

@app.route('/login_action', methods=['POST'])
def login_action():
    global CURRENT_USER_EMAIL, USER_STATE
    email = request.form.get('email')
    password = request.form.get('password')
    role_choice = request.form.get('role', 'seeker')
    
    user = db.get_user(email)
    
    if user:
        CURRENT_USER_EMAIL = email
        if user[3] == 'recruiter':
            return redirect(url_for('recruiter_dashboard'))
        else:
            return redirect(url_for('onboarding'))
    else:
        display_name = email.split('@')[0].capitalize()
        db.add_user(email, password, role_choice, display_name)
        CURRENT_USER_EMAIL = email
        
        if role_choice == 'recruiter':
            return redirect(url_for('recruiter_dashboard'))
        else:
            return redirect(url_for('onboarding'))

@app.route('/logout')
def logout():
    global CURRENT_USER_EMAIL, USER_STATE
    CURRENT_USER_EMAIL = "guest@example.com"
    USER_STATE = get_default_state() 
    return redirect(url_for('index'))

@app.route('/onboarding')
def onboarding():
    return render_template('onboarding.html')

@app.route('/seeker_dashboard', methods=['GET', 'POST'])
def seeker_dashboard():
    global USER_STATE
    if request.method == 'POST':
        USER_STATE['parsed_skills'] = request.form.get('skills', 'Not provided')
        USER_STATE['education'] = request.form.get('education', 'Not provided')
        USER_STATE['experience'] = request.form.get('experience', 'Not provided')
        USER_STATE['name'] = request.form.get('name', '')
        
    user = db.get_user(CURRENT_USER_EMAIL)
    display_name = USER_STATE.get('name') or (user[4] if user else "Seeker")
    initial = display_name[0].upper() if display_name else "S"
    
    return render_template('dashboard.html', user_name=display_name, state=USER_STATE, initial=initial)

@app.route('/parse_resume', methods=['POST'])
def parse_resume():
    global USER_STATE
    if 'resume' not in request.files:
        return jsonify({"error": "No file uploaded"})
        
    file = request.files['resume']
    if file.filename == '':
        return jsonify({"error": "No file selected"})

    try:
        filename = secure_filename("resume_" + CURRENT_USER_EMAIL.split('@')[0] + ".pdf")
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        USER_STATE['resume_path'] = filepath

        reader = PyPDF2.PdfReader(filepath)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + " "
        
        text = text.lower()
        tech_keywords = [
            'python', 'java', 'c++', 'sql', 'react', 'aws', 'docker', 
            'firebase', 'javascript', 'html', 'css', 'node.js', 'git'
        ]
        found_skills = [skill.title() for skill in tech_keywords if skill in text]
        
        extracted_data = {
            "name": CURRENT_USER_EMAIL.split('@')[0].capitalize(),
            "skills": ", ".join(found_skills),
            "education": "B.Tech" if "b.tech" in text or "bachelor" in text else "",
            "experience": "Fresher" if "2026" in text or "2025" in text else "1-2 Years"
        }
        return jsonify(extracted_data)
    except Exception as e:
        return jsonify({"error": str(e)})

# 🔧 THE FIX: Dynamically redirect back to the correct dashboard based on role
@app.route('/upload_pfp', methods=['POST'])
def upload_pfp():
    global USER_STATE
    if 'pfp' in request.files:
        file = request.files['pfp']
        if file.filename != '':
            filename = secure_filename("pfp_" + CURRENT_USER_EMAIL.split('@')[0] + "_" + file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            USER_STATE['pfp_path'] = filepath
            
    user = db.get_user(CURRENT_USER_EMAIL)
    if user and user[3] == 'recruiter':
        return redirect(url_for('recruiter_dashboard'))
    return redirect(url_for('seeker_dashboard'))

@app.route('/analysis', methods=['GET', 'POST'])
def analysis():
    global USER_STATE
    if request.method == 'POST':
        test_type = request.form.get('test_type')
        if test_type == 'technical':
            prog = (int(request.form.get('skill_1', 1)) / 4) * 100
            db_score = (int(request.form.get('skill_2', 1)) / 4) * 100
            vc_test = ((int(request.form.get('skill_3', 1)) + int(request.form.get('skill_6', 1))) / 8) * 100
            cloud_api = ((int(request.form.get('skill_4', 1)) + int(request.form.get('skill_5', 1))) / 8) * 100
            arch_algo = ((int(request.form.get('skill_7', 1)) + int(request.form.get('skill_8', 1))) / 8) * 100
            
            USER_STATE['scores'] = [int(prog), int(db_score), int(vc_test), int(cloud_api), int(arch_algo)]
            total_points = sum(int(request.form.get(f'skill_{i}', 1)) for i in range(1, 9))
            USER_STATE['overall_match'] = int((total_points / 32) * 100)
            
            swot_answers = [request.form.get(f'swot_{i}', 'S') for i in range(1, 9)]
            s_count = swot_answers.count('S')
            w_count = swot_answers.count('W')
            
            USER_STATE['strength'] = "Methodical Planning & Execution" if s_count >= 4 else "Adaptability Under Pressure"
            USER_STATE['weakness'] = "Overthinking & Hesitation" if w_count >= 3 else "Imposter Syndrome / Self-Doubt"
                
            if client:
                try:
                    role = "Backend Developer" 
                    style = request.form.get('learn_1', 'Kinesthetic')
                    prompt = f"""You are an expert career coach. Target role: {role}. Preferred learning style: {style}.
                    My top strength is {USER_STATE['strength']} and my weakness is {USER_STATE['weakness']}. Write a highly personalized, encouraging 2-sentence career action plan."""
                    response = client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
                    USER_STATE["ai_insight"] = response.text.replace('*', '')
                except:
                    USER_STATE["ai_insight"] = "Keep refining your technical foundation and updating your portfolio."
            return redirect(url_for('seeker_dashboard'))
    return render_template('analysis.html')

@app.route('/opportunities')
def opportunities():
    raw_jobs = db.get_all_jobs()
    display_jobs = [{'id': j[0], 'company': j[1], 'title': j[2], 'salary': j[3], 'skills': j[4]} for j in raw_jobs]
    return render_template('opportunities.html', jobs=display_jobs)

@app.route('/apply/<int:job_id>')
def apply_job(job_id):
    db.apply_for_job(job_id, CURRENT_USER_EMAIL)
    return redirect(url_for('opportunities'))

# 🔧 THE FIX: Pass `state` and `initial` to the recruiter dashboard
@app.route('/recruiter_dashboard', methods=['GET', 'POST'])
def recruiter_dashboard():
    global USER_STATE
    if request.method == 'POST':
        db.add_job(request.form.get('company'), request.form.get('job_title'), request.form.get('salary'), request.form.get('skills'))
        return redirect(url_for('recruiter_dashboard'))
        
    raw_jobs = db.get_all_jobs()
    all_seekers = db.get_all_seekers()
    dashboard_data = []
    
    for j in raw_jobs:
        job_id = j[0]
        job_dict = {'id': job_id, 'title': j[2], 'company': j[1], 'skills': j[4], 'applicants': [], 'matches': []}
        applicants = db.get_applicants_for_job(job_id)
        job_dict['applicants'] = [{"name": a[0], "email": a[1]} for a in applicants]
        
        job_skills_set = set(x.strip().lower() for x in str(j[4]).replace('\n', ',').split(',') if x.strip())
        
        for seeker in all_seekers:
            seeker_name = seeker[4]
            seeker_skills_set = set(x.strip().lower() for x in (seeker[5] if seeker[5] else "").replace('\n', ',').split(',') if x.strip())
            
            if job_skills_set and seeker_skills_set:
                matched = seeker_skills_set.intersection(job_skills_set)
                match_score = int((len(matched) / len(job_skills_set)) * 100)
                if match_score >= 30:
                    job_dict['matches'].append({"name": seeker_name, "score": match_score})
                    
        job_dict['matches'] = sorted(job_dict['matches'], key=lambda x: x['score'], reverse=True)
        dashboard_data.append(job_dict)

    user = db.get_user(CURRENT_USER_EMAIL)
    display_name = user[4] if user else "Recruiter"
    initial = display_name[0].upper() if display_name else "R"
    
    return render_template('recruiter_dashboard.html', user_name=display_name, jobs=dashboard_data, state=USER_STATE, initial=initial)

if __name__ == '__main__':
    app.run(debug=True)