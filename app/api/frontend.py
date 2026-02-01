"""
CloudJobHunt - Frontend HTML Templates
"""
from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()

# Template pour la page d'accueil
HOME_TEMPLATE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CloudJobHunt - Trouve ton job idéal</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        header {
            background: white;
            padding: 20px 0;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        header .container {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .logo { font-size: 28px; font-weight: bold; color: #667eea; }
        nav a {
            margin-left: 30px;
            text-decoration: none;
            color: #333;
            font-weight: 500;
        }
        nav a:hover { color: #667eea; }
        .hero {
            text-align: center;
            padding: 80px 20px;
            color: white;
        }
        .hero h1 { font-size: 48px; margin-bottom: 20px; }
        .hero p { font-size: 20px; opacity: 0.9; margin-bottom: 40px; }
        .search-box {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            max-width: 800px;
            margin: 0 auto;
        }
        .search-box input, .search-box select {
            width: 100%;
            padding: 15px 20px;
            margin: 10px 0;
            border: 2px solid #eee;
            border-radius: 8px;
            font-size: 16px;
        }
        .search-box button {
            width: 100%;
            padding: 15px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
            transition: transform 0.2s;
        }
        .search-box button:hover { transform: scale(1.02); }
        .filters {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }
        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            padding: 60px 0;
        }
        .feature-card {
            background: white;
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        }
        .feature-card h3 { color: #667eea; margin-bottom: 15px; }
        .jobs-section { padding: 60px 0; }
        .job-card {
            background: white;
            padding: 25px;
            border-radius: 10px;
            margin: 15px 0;
            box-shadow: 0 3px 10px rgba(0,0,0,0.1);
            border-left: 4px solid #667eea;
        }
        .job-card h3 { color: #333; margin-bottom: 10px; }
        .job-card .company { color: #667eea; font-weight: 500; }
        .job-card .location { color: #666; font-size: 14px; margin: 5px 0; }
        .job-card .tags { margin-top: 10px; }
        .tag {
            display: inline-block;
            background: #eee;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 12px;
            margin-right: 5px;
        }
        .btn-apply {
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 10px 25px;
            border-radius: 5px;
            text-decoration: none;
            margin-top: 15px;
        }
        footer {
            background: #333;
            color: white;
            text-align: center;
            padding: 30px;
            margin-top: 60px;
        }
    </style>
</head>
<body>
    <header>
        <div class="container">
            <div class="logo">🚀 CloudJobHunt</div>
            <nav>
                <a href="#search">Rechercher</a>
                <a href="#features">Fonctionnalités</a>
                <a href="/docs">API</a>
                <a href="/api/v1/login">Connexion</a>
            </nav>
        </div>
    </header>

    <section class="hero">
        <div class="container">
            <h1>Trouve ton job idéal en France & Europe</h1>
            <p>Recherche parmi des milliers d'offres LinkedIn, Indeed et plus encore</p>
        </div>
    </section>

    <section id="search">
        <div class="container">
            <div class="search-box">
                <h2 style="text-align: center; margin-bottom: 20px; color: #333;">🔍 Rechercher un emploi</h2>
                <form action="/search" method="GET">
                    <input type="text" name="q" placeholder="Poste, entreprise, ou mot-clé...">
                    <div class="filters">
                        <select name="location">
                            <option value="">📍 Toutes localisations</option>
                            <option value="tunisie">🇹🇳 Tunisie</option>
                            <option value="france">🇫🇷 France</option>
                            <option value="allemagne">🇩🇪 Allemagne</option>
                            <option value="belgique">🇧🇪 Belgique</option>
                            <option value="uk">🇬🇧 Royaume-Uni</option>
                        </select>
                        <select name="type">
                            <option value="">📋 Tous types de contrat</option>
                            <option value="cdi">CDI</option>
                            <option value="cdd">CDD</option>
                            <option value="stage">Stage</option>
                            <option value="freelance">Freelance</option>
                        </select>
                        <select name="experience">
                            <option value="">💼 Tous niveaux d'expérience</option>
                            <option value="junior">Junior (0-2 ans)</option>
                            <option value="intermediate">Intermédiaire (2-5 ans)</option>
                            <option value="senior">Senior (5+ ans)</option>
                        </select>
                    </div>
                    <button type="submit">Rechercher</button>
                </form>
            </div>
        </div>
    </section>

    <section id="features" class="container">
        <div class="features">
            <div class="feature-card">
                <h3>🤖 Matching Intelligent</h3>
                <p>Notre IA analyse ton profil et trouve les offres qui correspondent parfaitement à tes compétences.</p>
            </div>
            <div class="feature-card">
                <h3>🌍 Multi-plateformes</h3>
                <p>Recherche sur LinkedIn, Indeed, Welcome to the Jungle et bien d'autres en une seule recherche.</p>
            </div>
            <div class="feature-card">
                <h3>🔔 Alertes en temps réel</h3>
                <p>Reçois des notifications instantanément quand une nouvelle offre correspond à tes critères.</p>
            </div>
        </div>
    </section>

    <section class="jobs-section container">
        <h2 style="text-align: center; margin-bottom: 40px;">💼 Dernières offres</h2>
        <div class="job-card">
            <h3>Développeur Python / FastAPI</h3>
            <p class="company">TechCorp Paris</p>
            <p class="location">📍 Paris, France (Hybride)</p>
            <div class="tags">
                <span class="tag">CDI</span>
                <span class="tag">Senior</span>
                <span class="tag">Python</span>
                <span class="tag">FastAPI</span>
                <span class="tag">PostgreSQL</span>
            </div>
            <a href="#" class="btn-apply">Postuler maintenant</a>
        </div>
        <div class="job-card">
            <h3>DevOps Engineer - Kubernetes</h3>
            <p class="company">CloudFirst Lyon</p>
            <p class="location">📍 Lyon, France</p>
            <div class="tags">
                <span class="tag">CDI</span>
                <span class="tag">Intermédiaire</span>
                <span class="tag">Kubernetes</span>
                <span class="tag">Docker</span>
                <span class="tag">Azure</span>
            </div>
            <a href="#" class="btn-apply">Postuler maintenant</a>
        </div>
        <div class="job-card">
            <h3>Full Stack Developer JavaScript</h3>
            <p class="company">StartupHub Berlin</p>
            <p class="location">📍 Berlin, Allemagne</p>
            <div class="tags">
                <span class="tag">CDI</span>
                <span class="tag">Junior</span>
                <span class="tag">React</span>
                <span class="tag">Node.js</span>
                <span class="tag">TypeScript</span>
            </div>
            <a href="#" class="btn-apply">Postuler maintenant</a>
        </div>
    </section>

    <footer>
        <p>🚀 CloudJobHunt - Trouve ton job idéal en France et en Europe</p>
        <p style="margin-top: 10px; opacity: 0.7;">Propulsé par Azure Kubernetes & FastAPI</p>
    </footer>
</body>
</html>
"""

@router.get("/", response_class=HTMLResponse)
async def home():
    """Page d'accueil"""
    return HOME_TEMPLATE

@router.get("/search", response_class=HTMLResponse)
async def search_results(q: str = "", location: str = "", type_: str = "", experience: str = ""):
    """Page de résultats de recherche"""
    # Simulation de résultats (à remplacer par vrai scraping)
    jobs = [
        {"title": "Développeur Python Senior", "company": "TechCorp", "location": "Paris", "type": "CDI", "tags": ["Python", "FastAPI", "PostgreSQL"]},
        {"title": "DevOps Engineer", "company": "CloudFirst", "location": "Lyon", "type": "CDI", "tags": ["Kubernetes", "Docker", "Azure"]},
        {"title": "Full Stack JS", "company": "StartupHub", "location": "Berlin", "type": "CDI", "tags": ["React", "Node.js"]},
    ]
    
    html = f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Résultats - CloudJobHunt</title>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{ font-family: 'Segoe UI', sans-serif; background: #f5f5f5; }}
            header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; color: white; }}
            .container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
            .job-card {{ background: white; padding: 25px; border-radius: 10px; margin: 15px 0; box-shadow: 0 3px 10px rgba(0,0,0,0.1); }}
            .tag {{ display: inline-block; background: #667eea; color: white; padding: 5px 12px; border-radius: 20px; font-size: 12px; margin: 2px; }}
            .btn-back {{ display: inline-block; background: white; color: #667eea; padding: 10px 25px; border-radius: 5px; text-decoration: none; margin-bottom: 20px; }}
        </style>
    </head>
    <body>
        <header>
            <div class="container">
                <h1>🔍 Résultats pour "{q or 'Tous les jobs'}"</h1>
            </div>
        </header>
        <div class="container">
            <a href="/" class="btn-back">← Retour à l'accueil</a>
            <h2 style="margin-bottom: 20px;">{len(jobs)} offres trouvées</h2>
    """
    
    for job in jobs:
        tags_html = "".join([f'<span class="tag">{tag}</span>' for tag in job["tags"]])
        html += f"""
        <div class="job-card">
            <h3>{job['title']}</h3>
            <p><strong>🏢 {job['company']}</strong> | 📍 {job['location']} | 📋 {job['type']}</p>
            <div style="margin-top: 10px;">{tags_html}</div>
        </div>
        """
    
    html += """
        </div>
    </body>
    </html>
    """
    return html

@router.get("/login", response_class=HTMLResponse)
async def login_page():
    """Page de connexion"""
    return """
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Connexion - CloudJobHunt</title>
        <style>
            body { font-family: 'Segoe UI', sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; display: flex; align-items: center; justify-content: center; }
            .login-box { background: white; padding: 40px; border-radius: 15px; box-shadow: 0 10px 40px rgba(0,0,0,0.2); width: 400px; }
            h1 { text-align: center; color: #667eea; margin-bottom: 30px; }
            input { width: 100%; padding: 15px; margin: 10px 0; border: 2px solid #eee; border-radius: 8px; font-size: 16px; }
            button { width: 100%; padding: 15px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; border-radius: 8px; font-size: 18px; font-weight: bold; cursor: pointer; }
            .links { text-align: center; margin-top: 20px; }
            a { color: #667eea; text-decoration: none; }
        </style>
    </head>
    <body>
        <div class="login-box">
            <h1>🚀 CloudJobHunt</h1>
            <form action="/api/v1/login" method="POST">
                <input type="email" name="username" placeholder="📧 Email" required>
                <input type="password" name="password" placeholder="🔒 Mot de passe" required>
                <button type="submit">Se connecter</button>
            </form>
            <div class="links">
                <p>Pas de compte ? <a href="/register">S'inscrire</a></p>
                <p><a href="/">← Retour à l'accueil</a></p>
            </div>
        </div>
    </body>
    </html>
    """

@router.get("/register", response_class=HTMLResponse)
async def register_page():
    """Page d'inscription"""
    return """
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Inscription - CloudJobHunt</title>
        <style>
            body { font-family: 'Segoe UI', sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; display: flex; align-items: center; justify-content: center; }
            .register-box { background: white; padding: 40px; border-radius: 15px; box-shadow: 0 10px 40px rgba(0,0,0,0.2); width: 400px; }
            h1 { text-align: center; color: #667eea; margin-bottom: 30px; }
            input { width: 100%; padding: 15px; margin: 10px 0; border: 2px solid #eee; border-radius: 8px; font-size: 16px; }
            button { width: 100%; padding: 15px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; border-radius: 8px; font-size: 18px; font-weight: bold; cursor: pointer; }
            .links { text-align: center; margin-top: 20px; }
            a { color: #667eea; text-decoration: none; }
        </style>
    </head>
    <body>
        <div class="register-box">
            <h1>🚀 CloudJobHunt</h1>
            <form action="/api/v1/register" method="POST">
                <input type="text" name="name" placeholder="👤 Nom complet" required>
                <input type="email" name="email" placeholder="📧 Email" required>
                <input type="password" name="password" placeholder="🔒 Mot de passe" required>
                <button type="submit">Créer mon compte</button>
            </form>
            <div class="links">
                <p>Déjà un compte ? <a href="/login">Se connecter</a></p>
                <p><a href="/">← Retour à l'accueil</a></p>
            </div>
        </div>
    </body>
    </html>
    """
