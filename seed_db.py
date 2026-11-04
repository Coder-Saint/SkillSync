import sqlite3
import random

DB_NAME = "skillsync.db"

# --- DATA POOLS FOR RANDOM GENERATION ---
FIRST_NAMES = ["Rahul", "Priya", "Amit", "Neha", "Rohan", "Anjali", "Karan", "Sneha", "Vikram", "Pooja", "John", "Jane", "Alex", "Emily", "David", "Sarah", "Michael", "Emma", "Chris", "Olivia"]
LAST_NAMES = ["Sharma", "Singh", "Patel", "Gupta", "Kumar", "Verma", "Reddy", "Rao", "Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", "Davis", "Garcia"]
TECH_SKILLS = ["Python", "Java", "C++", "SQL", "React", "AWS", "Docker", "Firebase", "JavaScript", "HTML", "CSS", "Node.js", "Git", "Kubernetes", "Go", "MongoDB", "PostgreSQL", "Redis", "TypeScript", "Azure"]
COMPANIES = ["InnovateTech", "DataSphere", "CloudNative Labs", "Quantum Systems", "Nexus AI", "TCS", "Infosys", "Wipro", "Google", "Microsoft", "Amazon", "TechMahindra", "Flipkart", "Zomato", "Paytm"]
JOB_TITLES = ["Backend Engineer", "Frontend Developer", "Full Stack SDE", "DevOps Engineer", "Data Engineer", "Cloud Architect", "Software Engineer I", "Software Engineer II", "Senior Developer"]

def seed_database():
    print("🌱 Connecting to database...")
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # --- 1. GENERATE 5,000 SEEKERS ---
    print("⏳ Generating 5,000 Job Seekers...")
    seekers_data = []
    for i in range(5000):
        first = random.choice(FIRST_NAMES)
        last = random.choice(LAST_NAMES)
        display_name = f"{first} {last}"
        email = f"{first.lower()}.{last.lower()}.{random.randint(1000, 99999)}@example.com"
        password = "password123"
        role = "seeker"
        
        # Pick 3 to 6 random skills for this user
        num_skills = random.randint(3, 6)
        user_skills = ", ".join(random.sample(TECH_SKILLS, num_skills))
        
        seekers_data.append((email, password, role, display_name, user_skills))

    # Batch insert seekers for extreme speed
    c.executemany("INSERT INTO users (email, password, role, display_name, skills) VALUES (?, ?, ?, ?, ?)", seekers_data)
    print("✅ 5,000 Seekers inserted successfully!")

    # --- 2. GENERATE 1,000 JOB OPPORTUNITIES ---
    print("⏳ Generating 1,000 Job Opportunities...")
    jobs_data = []
    for i in range(1000):
        company = random.choice(COMPANIES)
        title = random.choice(JOB_TITLES)
        
        # Random salary formatting (mixing USD and INR styles)
        if random.choice([True, False]):
            salary = f"${random.randint(80, 160)},000 / yr"
        else:
            salary = f"₹{random.randint(8, 30)} LPA"
            
        # Pick 3 to 5 random skills required for the job
        num_req_skills = random.randint(3, 5)
        job_req_skills = ", ".join(random.sample(TECH_SKILLS, num_req_skills))
        
        jobs_data.append((company, title, salary, job_req_skills))

    # Batch insert jobs
    c.executemany("INSERT INTO jobs (company, title, salary, skills) VALUES (?, ?, ?, ?)", jobs_data)
    print("✅ 1,000 Jobs inserted successfully!")

    conn.commit()
    conn.close()
    print("🎉 Database seeding complete! You are ready to launch.")

if __name__ == "__main__":
    seed_database()