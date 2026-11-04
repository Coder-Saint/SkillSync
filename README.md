# SkillSync

A skill-based job matching platform built with Flask. SkillSync helps job seekers find roles that fit their skills and shows them what to learn next, while helping recruiters find candidates who match their exact job requirements.

## Features

### For Job Seekers
- Sign up, log in, and complete an onboarding profile
- Add and assess your skills
- Get job and opportunity recommendations based on your skill set
- View a skill analysis, including a SWOT breakdown of your strengths and gaps
- Get suggestions on which skills to upgrade to qualify for better roles
- Explore role pages to see what each job requires

### For Recruiters
- Separate recruiter onboarding and dashboard
- Define job requirements by required skills
- Find candidates whose skills match the job requirements
- Save time by focusing on best-fit candidates

## Tech Stack

- **Backend:** Python, Flask
- **Database:** SQLite
- **Frontend:** HTML (Jinja2 templates), CSS

## Project Structure

```
.
├── app.py                 # Main Flask application and routes
├── database.py            # Database setup and helper functions
├── seed_db.py             # Seeds the database with sample data (roles, skills)
├── requirements.txt       # Python dependencies
├── static/
│   └── style.css          # Stylesheet
└── templates/
    ├── index.html                  # Landing page
    ├── login.html                  # Login / sign up
    ├── onboarding.html             # Job seeker onboarding
    ├── assessment.html             # Skill assessment
    ├── analysis.html               # Skill analysis
    ├── dashboard.html              # Job seeker dashboard
    ├── opportunities.html          # Matched jobs and opportunities
    ├── role.html                   # Role details
    ├── recruiter_onboarding.html   # Recruiter onboarding
    ├── recruiter_dashboard.html    # Recruiter dashboard
    └── test_*.html                 # Test pages (skills, SWOT, recommendations)
```

## Getting Started

### Prerequisites
- Python 3.8 or higher
- pip

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/skillsync.git
   cd skillsync
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # Mac/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the database:
   ```bash
   python database.py
   python seed_db.py
   ```
   This creates `skillsync.db` and fills it with sample data.

5. Run the app:
   ```bash
   python app.py
   ```
   Then open http://127.0.0.1:5000 in your browser.

## How It Works

1. A job seeker creates a profile and lists their skills.
2. A recruiter posts the skills required for a role.
3. SkillSync compares candidate skills against role requirements.
4. Job seekers see matching opportunities plus the skills they should learn to close any gaps.
5. Recruiters see the candidates who best fit their requirements.

## Future Improvements

- Resume upload with automatic skill extraction
- Course recommendations linked to missing skills
- Email notifications for new matching jobs
- In-app chat between recruiters and candidates

## Notes

- The SQLite database (`skillsync.db`) is not included in the repository. Create it with the steps above.
- Never commit secrets. Keep keys and passwords in a `.env` file, which is listed in `.gitignore`.

## License

MIT
