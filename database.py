import sqlite3

DB_NAME = "skillsync.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Create users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            display_name TEXT,
            skills TEXT DEFAULT ''
        )
    ''')
    
    # Create jobs table
    c.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT NOT NULL,
            title TEXT NOT NULL,
            salary TEXT NOT NULL,
            skills TEXT NOT NULL
        )
    ''')

    # Create applications table
    c.execute('''
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id INTEGER NOT NULL,
            user_email TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()

def get_user(email):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email=?", (email,))
    user = c.fetchone()
    conn.close()
    return user

def add_user(email, password, role, display_name):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (email, password, role, display_name, skills) VALUES (?, ?, ?, ?, ?)",
                  (email, password, role, display_name, ""))
        conn.commit()
    except sqlite3.IntegrityError:
        pass # User already exists
    conn.close()

def get_all_jobs():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM jobs")
    jobs = c.fetchall()
    conn.close()
    return jobs

def add_job(company, title, salary, skills):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO jobs (company, title, salary, skills) VALUES (?, ?, ?, ?)",
              (company, title, salary, skills))
    conn.commit()
    conn.close()

def apply_for_job(job_id, email):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO applications (job_id, user_email) VALUES (?, ?)", (job_id, email))
    conn.commit()
    conn.close()

# --- 🔧 NEW FUNCTIONS FOR RECRUITER MATCHING 🔧 ---

def get_applicants_for_job(job_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Join the applications and users tables to get the applicant's name and email
    c.execute('''
        SELECT u.display_name, u.email 
        FROM applications a
        JOIN users u ON a.user_email = u.email
        WHERE a.job_id = ?
    ''', (job_id,))
    applicants = c.fetchall()
    conn.close()
    return applicants

def get_all_seekers():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Fetch all users who are job seekers for the Set-Theory matchmaking pipeline
    c.execute("SELECT * FROM users WHERE role='seeker'")
    seekers = c.fetchall()
    conn.close()
    return seekers