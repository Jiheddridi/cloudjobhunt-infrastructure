"""
CloudJobHunt Scraper - Générateur d'offres d'emploi réalistes
Simule la recherche sur LinkedIn, Indeed, Welcome to the Jungle sans API payante
"""
import asyncio
import aiohttp
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from urllib.parse import quote_plus
import random
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class Job:
    """Représentation d'une offre d'emploi"""
    title: str
    company: str
    location: str
    description: str
    url: str
    source: str  # linkedin, indeed, junglejobs, etc.
    posted_date: datetime
    job_type: str = ""  # CDI, CDD, Stage, Freelance
    salary: str = ""
    skills: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "company": self.company,
            "location": self.location,
            "description": self.description[:500] + "..." if len(self.description) > 500 else self.description,
            "url": self.url,
            "source": self.source,
            "posted_date": self.posted_date.isoformat(),
            "job_type": self.job_type,
            "salary": self.salary,
            "skills": self.skills,
            "days_ago": (datetime.now() - self.posted_date).days
        }


# Données réalistes pour la génération
COMPANIES = {
    "linkedin": [
        "TechCorp France", "Digital Innovation SAS", "Cloud Solutions", "Data Dynamics",
        "AI Technologies", "Web Agency Pro", "Startup Valley", "Tech Startup Paris"
    ],
    "indeed": [
        "Entreprise Nationale", "Groupement des Entreprises", "Société de Services",
        "Cabinet de Conseil", "ESN Internationale", "EdTech France", "HealthTech SAS"
    ],
    "junglejobs": [
        "Welcome to the Jungle Partners", "Startup accelerators", "Tech incubators",
        "Innovation labs", "Venture capital firms", "Scale-up françaises"
    ],
    "google": [
        "Multi-national corporations", "International tech companies", "Global firms",
        "Fortune 500 subsidiaries", "European tech leaders"
    ]
}

JOB_DESCRIPTIONS = {
    "devops": [
        "Conception et mise en œuvre de pipelines CI/CD",
        "Management des infrastructures cloud (AWS, Azure, GCP)",
        "Automatisation avec Terraform, Ansible, Kubernetes",
        "Monitoring et observabilité (Prometheus, Grafana)",
        "Amélioration continue des performances"
    ],
    "python": [
        "Développement d'applications Python (Django, FastAPI)",
        "Machine Learning et Data Science",
        "API RESTful et microservices",
        "Automatisation et scripting",
        "Base de données et ORM"
    ],
    "data scientist": [
        "Machine Learning et Deep Learning",
        "Analyse de données avec Python, SQL",
        "Visualisation (Matplotlib, Seaborn, Tableau)",
        "Statistiques avancées",
        "Modélisation prédictif"
    ],
    "web": [
        "Développement frontend (React, Vue.js, Angular)",
        "Backend API (Node.js, Python, PHP)",
        "Responsive design et UI/UX",
        "Base de données et API",
        "SEO et performance web"
    ],
    "stage": [
        "Accompagnement sur des projets concrets",
        "Apprentissage des bonnes pratiques",
        "Tutorat par des développeurs expérimentés",
        "Environnement start-up dynamique",
        "Possibilité de CDI à la clé"
    ],
    "chef de projet": [
        "Gestion de projet agile (Scrum, Kanban)",
        "Coordination des équipes techniques",
        "Planification et suivi des jalons",
        "Communication avec les parties prenantes",
        "Gestion des risques et des imprevus"
    ]
}


def generate_jobs_for_query(query: str, location: str = "", job_type: str = "", max_results: int = 20) -> List[Job]:
    """Génère des offres d'emploi réalistes basées sur la requête"""
    jobs = []
    query_lower = query.lower()
    
    # Vérifier si c'est un poste junior
    is_junior = "junior" in query_lower or "jr" in query_lower or "entry" in query_lower
    
    # Déterminer le type de poste
    job_titles = []
    if "devops" in query_lower:
        if is_junior:
            job_titles = ["Junior DevOps Engineer", "DevOps Jr", "Junior Cloud Engineer", "Junior SRE"]
        else:
            job_titles = ["DevOps Engineer", "Senior DevOps", "Cloud Engineer", "SRE Engineer", "Infrastructure Engineer"]
    elif "python" in query_lower:
        if is_junior:
            job_titles = ["Junior Python Developer", "Python Jr", "Junior Backend Developer", "Junior Software Engineer"]
        else:
            job_titles = ["Python Developer", "Backend Developer Python", "Full Stack Developer", "Software Engineer"]
    elif "data" in query_lower or "scientist" in query_lower:
        if is_junior:
            job_titles = ["Junior Data Scientist", "Data Analyst Jr", "Junior ML Engineer"]
        else:
            job_titles = ["Data Scientist", "Data Analyst", "ML Engineer", "Data Engineer"]
    elif "web" in query_lower or "frontend" in query_lower:
        if is_junior:
            job_titles = ["Junior Web Developer", "Frontend Jr", "Junior Frontend Developer"]
        else:
            job_titles = ["Web Developer", "Frontend Developer", "Full Stack Developer", "React Developer"]
    elif "stage" in query_lower:
        job_titles = ["Stagiaire DevOps", "Stagiaire Data Scientist", "Stagiaire Développeur Web", "Stagiaire Python"]
    elif "chef de projet" in query_lower or "project manager" in query_lower:
        if is_junior:
            job_titles = ["Junior Product Owner", "Junior Project Manager", "Assistant Chef de Projet"]
        else:
            job_titles = ["Chef de Projet IT", "Product Owner", "Scrum Master", "Project Manager"]
    else:
        if is_junior:
            job_titles = [f"Junior {query.title()} Developer", f"Junior {query.title()} Engineer", f"{query.title()} Jr"]
        else:
            job_titles = [f"Développeur {query.title()}", f"Ingénieur {query.title()}", f"Tech Lead {query.title()}", 
                         f"{query.title()} Developer", "Software Engineer"]
    
    # Type de contrat
    contract_type = "CDI"
    if job_type == "cdd":
        contract_type = "CDD"
    elif job_type == "stage":
        contract_type = "Stage"
    elif job_type == "freelance":
        contract_type = "Freelance"
    
    # Localisation
    loc = location if location else "France (Remote)"
    
    # Salaires réalistes
    salaries = {
        "CDI": ["35K€ - 45K€", "40K€ - 55K€", "45K€ - 60K€", "50K€ - 70K€", "55K€ - 75K€"],
        "CDD": ["30K€ - 40K€", "35K€ - 45K€", "40K€ - 50K€"],
        "Stage": ["800€ - 1200€ / mois", "1000€ - 1500€ / mois", "1200€ - 1800€ / mois"],
        "Freelance": ["400€ - 600€ / jour", "500€ - 700€ / jour", "600€ - 800€ / jour"]
    }
    
    # Compétences basées sur la requête
    skills = []
    if "devops" in query_lower:
        skills = ["Docker", "Kubernetes", "Terraform", "AWS", "CI/CD", "Linux"]
    elif "python" in query_lower:
        skills = ["Python", "Django", "FastAPI", "PostgreSQL", "REST API"]
    elif "data" in query_lower:
        skills = ["Python", "Machine Learning", "SQL", "TensorFlow", "Pandas"]
    elif "web" in query_lower:
        skills = ["JavaScript", "React", "CSS", "HTML", "Node.js"]
    elif "stage" in query_lower:
        skills = ["Git", "Bases de données", "Programmation", "Travail d'équipe"]
    
    # Sources
    sources = ["linkedin", "indeed", "junglejobs"]
    
    # Générer les offres
    for i in range(min(max_results, 20)):
        source = sources[i % 3]
        company = random.choice(COMPANIES[source])
        title = random.choice(job_titles)
        
        # Description réaliste
        desc_key = "stage" if job_type == "stage" else ("devops" if "devops" in query_lower else 
                      ("python" if "python" in query_lower else 
                       ("data" if "data" in query_lower else 
                        ("web" if "web" in query_lower else 
                         ("chef de projet" if "chef" in query_lower else "general")))))
        
        descriptions = JOB_DESCRIPTIONS.get(desc_key, JOB_DESCRIPTIONS["web"])
        description = f" {random.choice(descriptions)}.".join([
            f"Rejoignez notre équipe en tant que {title}",
            f"Vous serez responsable de {random.choice(descriptions).lower()}",
            f"Profil recherché: {random.randint(2, 5)} ans d'expérience",
            f"Environnement tech moderne avec {random.choice(['Docker', 'Kubernetes', 'AWS', 'GCP'])}"
        ])
        
        # URL de recherche directe
        if source == "linkedin":
            url = f"https://www.linkedin.com/jobs/search/?keywords={quote_plus(query)}&location={quote_plus(loc)}"
            company_logo = "🔵"
        elif source == "indeed":
            url = f"https://www.indeed.fr/jobs?q={quote_plus(query)}&l={quote_plus(loc)}"
            company_logo = "🔶"
        else:
            url = f"https://www.welcometothejungle.com/fr/jobs?query={quote_plus(query)}"
            company_logo = "🟢"
        
        # Date de publication aléatoire (0-4 jours)
        days_ago = random.randint(0, 4)
        
        job = Job(
            title=f"{title}",
            company=company,
            location=loc,
            description=description,
            url=url,
            source=source,
            posted_date=datetime.now() - timedelta(days=days_ago),
            job_type=contract_type,
            salary=random.choice(salaries[contract_type]),
            skills=skills[:random.randint(3, 6)]
        )
        jobs.append(job)
    
    return jobs


async def search_jobs_async(query: str, location: str = "", job_type: str = "", 
                           max_days_old: int = 5, max_results: int = 20) -> List[Dict[str, Any]]:
    """Recherche asynchrone - utilise la génération de données réalistes"""
    logger.info(f"🔍 Recherche: {query} à {location} (type: {job_type})")
    
    # Simuler un délai réseau
    await asyncio.sleep(0.5)
    
    # Générer les offres
    jobs = generate_jobs_for_query(query, location, job_type, max_results)
    
    # Filtrer par date
    cutoff_date = datetime.now() - timedelta(days=max_days_old)
    jobs = [j for j in jobs if j.posted_date >= cutoff_date]
    
    # Convertir en dict
    return [job.to_dict() for job in jobs]


def search_jobs_sync(query: str, location: str = "", job_type: str = "", 
                     max_days_old: int = 5, max_results: int = 20) -> List[Dict[str, Any]]:
    """Recherche synchrone pour FastAPI"""
    return asyncio.run(search_jobs_async(query, location, job_type, max_days_old, max_results))


class JobAggregator:
    """Agrégateur de jobs - point d'entrée principal"""
    
    def __init__(self):
        self.sources = ["linkedin", "indeed", "junglejobs"]
    
    async def search(self, query: str, location: str = "", job_type: str = "",
                     max_days_old: int = 5, max_results: int = 20) -> List[Dict[str, Any]]:
        """Recherche sur toutes les sources"""
        return await search_jobs_async(query, location, job_type, max_days_old, max_results)
    
    def search_sync(self, query: str, location: str = "", job_type: str = "",
                    max_days_old: int = 5, max_results: int = 20) -> List[Dict[str, Any]]:
        """Version synchrone"""
        return search_jobs_sync(query, location, job_type, max_days_old, max_results)
