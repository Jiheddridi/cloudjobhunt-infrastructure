from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import requests
import http.client
import json
import os
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Config APIs - Récupérer depuis variables d'environnement
ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID", "")
ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY", "")
JSEARCH_API_KEY = os.getenv("JSEARCH_API_KEY", "")


def init_db():
    conn = sqlite3.connect('jobs.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS jobs
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  title TEXT,
                  company TEXT,
                  location TEXT,
                  description TEXT,
                  url TEXT,
                  country TEXT,
                  source TEXT,
                  created_at TEXT)''')
    conn.commit()
    conn.close()

init_db()

@app.get("/")
def read_root():
    return {"status": "JobHunt API Running - Multi-Source", "sources": ["Adzuna", "JSearch"]}

def fetch_adzuna(country: str, keyword: str):
    """Fetch jobs from Adzuna API"""
    jobs = []
    try:
        url = f"https://api.adzuna.com/v1/api/jobs/{country}/search/1?app_id={ADZUNA_APP_ID}&app_key={ADZUNA_APP_KEY}&results_per_page=15&what={keyword}"
        response = requests.get(url, timeout=5)
        data = response.json()
        
        for job in data.get('results', []):
            jobs.append({
                "title": job.get('title', 'N/A'),
                "company": job.get('company', {}).get('display_name', 'N/A'),
                "location": job.get('location', {}).get('display_name', 'N/A'),
                "description": job.get('description', 'No description')[:500],
                "url": job.get('redirect_url', ''),
                "country": country.upper(),
                "source": "Adzuna"
            })
    except Exception as e:
        print(f"Adzuna error: {e}")
    
    return jobs

def fetch_jsearch(country: str, keyword: str):
    """Fetch jobs from JSearch API (LinkedIn, Indeed, etc.)"""
    jobs = []
    try:
        conn = http.client.HTTPSConnection("jsearch.p.rapidapi.com")
        headers = {
            'x-rapidapi-key': JSEARCH_API_KEY,
            'x-rapidapi-host': "jsearch.p.rapidapi.com"
        }
        
        # Mapping pays complet pour JSearch
        country_map = {
            'tn': ('tunisia', 'tn'),
            'fr': ('france', 'fr'),
            'gb': ('united kingdom', 'gb'),
            'us': ('united states', 'us'),
            'de': ('germany', 'de'),
            'ca': ('canada', 'ca'),
            'au': ('australia', 'au'),
            'nl': ('netherlands', 'nl'),
            'ch': ('switzerland', 'ch')
        }
        
        country_name, country_code = country_map.get(country.lower(), (country, country.lower()))
        
        # Construction de l'URL avec country code
        query = f"{keyword}%20jobs%20in%20{country_name.replace(' ', '%20')}"
        endpoint = f"/search?query={query}&page=1&num_pages=1&country={country_code}"
        
        conn.request("GET", endpoint, headers=headers)
        res = conn.getresponse()
        data = json.loads(res.read().decode("utf-8"))
        
        print(f"JSearch response for {country}: {len(data.get('data', []))} jobs")
        
        for job in data.get('data', [])[:15]:
            jobs.append({
                "title": job.get('job_title', 'N/A'),
                "company": job.get('employer_name', 'N/A'),
                "location": (job.get('job_city', '') + ', ' + job.get('job_country', '')).strip(', '),
                "description": job.get('job_description', 'No description')[:500],
                "url": job.get('job_apply_link', job.get('job_google_link', '')),
                "country": country.upper(),
                "source": "JSearch (LinkedIn/Indeed)"
            })
    except Exception as e:
        print(f"JSearch error: {e}")
    
    return jobs

@app.get("/search")
def search_jobs(country: str, keyword: str, source: str = "all"):
    """
    Search jobs from multiple sources
    source: 'all', 'adzuna', or 'jsearch'
    """
    try:
        all_jobs = []
        
        # Filter by source
        if source in ["all", "adzuna"]:
            all_jobs.extend(fetch_adzuna(country, keyword))
        
        if source in ["all", "jsearch"]:
            all_jobs.extend(fetch_jsearch(country, keyword))
        
        # Save to database
        conn = sqlite3.connect('jobs.db')
        c = conn.cursor()
        
        for job in all_jobs:
            c.execute("INSERT INTO jobs (title, company, location, description, url, country, source, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                      (job['title'], job['company'], job['location'], 
                       job['description'], job['url'], job['country'], job['source'], datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
        
        return {
            "jobs": all_jobs,
            "count": len(all_jobs),
            "country": country.upper(),
            "keyword": keyword,
            "source_filter": source
        }
    
    except Exception as e:
        return {"error": str(e), "jobs": [], "count": 0}

@app.get("/jobs")
def get_all_jobs():
    conn = sqlite3.connect('jobs.db')
    c = conn.cursor()
    c.execute("SELECT * FROM jobs ORDER BY created_at DESC LIMIT 100")
    jobs = [{"id": row[0], "title": row[1], "company": row[2], 
             "location": row[3], "description": row[4], "url": row[5], 
             "country": row[6], "source": row[7]} 
            for row in c.fetchall()]
    conn.close()
    return {"jobs": jobs, "count": len(jobs)}
