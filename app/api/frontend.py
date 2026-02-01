"""
CloudJobHunt - Frontend HTML Templates avec recherche en temps réel
"""
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.scraper.aggregator import search_jobs_sync
import json

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
            background: linear-gradient(135deg, #0066cc 0%, #004499 100%);
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
        .logo { 
            font-size: 32px; 
            font-weight: bold; 
            color: #0066cc; 
            text-decoration: none;
        }
        nav a {
            margin-left: 30px;
            text-decoration: none;
            color: #333;
            font-weight: 500;
        }
        nav a:hover { color: #0066cc; }
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
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 16px;
        }
        .search-box button {
            width: 100%;
            padding: 15px;
            background: linear-gradient(135deg, #0066cc 0%, #004499 100%);
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
        .feature-card h3 { color: #0066cc; margin-bottom: 15px; }
        footer {
            background: #004499;
            color: white;
            text-align: center;
            padding: 30px;
            margin-top: 60px;
        }
        .loading {
            text-align: center;
            padding: 40px;
            color: white;
            font-size: 18px;
        }
        .spinner {
            width: 40px;
            height: 40px;
            border: 4px solid rgba(255,255,255,0.3);
            border-top: 4px solid white;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        .job-card {
            background: white;
            padding: 25px;
            border-radius: 10px;
            margin: 15px 0;
            box-shadow: 0 3px 10px rgba(0,0,0,0.1);
            border-left: 4px solid #0066cc;
        }
        .job-card h3 { margin-bottom: 10px; color: #333; }
        .job-card .company { color: #0066cc; font-weight: 500; }
        .job-card .location { color: #666; font-size: 14px; margin-bottom: 10px; }
        .job-card .description { color: #333; margin: 15px 0; }
        .job-card .tags { margin-bottom: 15px; }
        .job-card .tag {
            display: inline-block;
            background: #e0e0e0;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 12px;
            margin-right: 5px;
            margin-bottom: 5px;
        }
        .job-card .source-tag {
            display: inline-block;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 12px;
            color: white;
        }
        .source-linkedin { background: #0077b5; }
        .source-indeed { background: #2164f3; }
        .source-junglejobs { background: #00d09c; }
        .btn-apply {
            display: inline-block;
            padding: 12px 25px;
            border-radius: 5px;
            text-decoration: none;
            font-weight: bold;
            color: white;
            background: #0066cc;
        }
        .no-results {
            text-align: center;
            padding: 40px;
            background: white;
            border-radius: 15px;
            margin: 20px 0;
        }
        .no-results h3 { color: #0066cc; margin-bottom: 10px; }
    </style>
</head>
<body>
    <header>
        <div class="container">
            <a href="/" class="logo">🚀 CloudJobHunt</a>
            <nav>
                <a href="#search">Rechercher</a>
                <a href="#features">Fonctionnalités</a>
                <a href="/login">Connexion</a>
            </nav>
        </div>
    </header>

    <section class="hero">
        <div class="container">
            <h1>Trouve ton job idéal en France & Europe</h1>
            <p>Recherche parmi des milliers d'offres LinkedIn, Indeed, Welcome to the Jungle et plus encore</p>
        </div>
    </section>

    <section id="search">
        <div class="container">
            <div class="search-box">
                <h2 style="text-align: center; margin-bottom: 20px; color: #333;">🔍 Recherche en temps réel</h2>
                <form id="jobSearchForm">
                    <input type="text" id="searchQuery" name="q" placeholder="Poste (ex: devops, python, data scientist)..." required>
                    <div class="filters">
                        <select id="searchLocation" name="location">
                            <option value="">📍 Toutes localisations</option>
                            <option value="tunisie">🇹🇳 Tunisie</option>
                            <option value="paris, france">🇫🇷 Paris, France</option>
                            <option value="lyon, france">🇫🇷 Lyon, France</option>
                            <option value="marseille, france">🇫🇷 Marseille, France</option>
                            <option value="berlin, allemagne">🇩🇪 Berlin, Allemagne</option>
                            <option value="bruxelles, belgique">🇧🇪 Bruxelles, Belgique</option>
                            <option value="london, uk">🇬🇧 Londres, UK</option>
                        </select>
                        <select id="searchType" name="type">
                            <option value="">📋 Tous types</option>
                            <option value="cdi">CDI</option>
                            <option value="cdd">CDD</option>
                            <option value="stage">Stage</option>
                            <option value="freelance">Freelance</option>
                        </select>
                    </div>
                    <button type="submit" id="searchBtn">🚀 Rechercher</button>
                </form>
                <div id="loading" class="loading" style="display: none;">
                    <div class="spinner"></div>
                    <p>Recherche en cours sur LinkedIn, Indeed, Welcome to the Jungle...</p>
                </div>
            </div>
        </div>
    </section>

    <section class="container">
        <div id="results"></div>
    </section>

    <section id="features" class="container">
        <div class="features">
            <div class="feature-card">
                <h3>🔍 Recherche en temps réel</h3>
                <p>Notre агент сканиne LinkedIn, Indeed et Welcome to the Jungle pour trouver les dernières offres.</p>
            </div>
            <div class="feature-card">
                <h3>⚡ Récent (moins de 5 jours)</h3>
                <p>Toutes les offres affichées sont publiées il y a moins de 5 jours.</p>
            </div>
            <div class="feature-card">
                <h3>🔗 Lien direct</h3>
                <p>Chaque offre inclut un lien pour postuler directement sur le site original.</p>
            </div>
        </div>
    </section>

    <footer>
        <p>🚀 CloudJobHunt - Trouve ton job idéal en France et en Europe</p>
        <p style="margin-top: 10px; opacity: 0.7;">Propulsé par Azure Kubernetes & FastAPI</p>
    </footer>

    <script>
        document.getElementById('jobSearchForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const query = document.getElementById('searchQuery').value;
            const location = document.getElementById('searchLocation').value;
            const type = document.getElementById('searchType').value;
            const searchBtn = document.getElementById('searchBtn');
            const loading = document.getElementById('loading');
            const results = document.getElementById('results');
            
            // Afficher le loader
            searchBtn.style.display = 'none';
            loading.style.display = 'block';
            results.innerHTML = '';
            
            try {
                const response = await fetch('/api/v1/search?q=' + encodeURIComponent(query) + 
                    '&location=' + encodeURIComponent(location) + 
                    '&job_type=' + encodeURIComponent(type));
                
                if (!response.ok) {
                    throw new Error('Erreur serveur: ' + response.status);
                }
                
                const data = await response.json();
                
                if (data.total_found === 0) {
                    results.innerHTML = `
                        <div class="no-results">
                            <h3 style="color: #0066cc;">🔍 Aucune offre trouvée</h3>
                            <p>Essayez avec d'autres mots-clés ou une autre localisation.</p>
                        </div>
                    `;
                } else {
                    let jobsHtml = `
                        <h2 style="text-align: center; margin: 40px 0 20px; color: white;">
                            💼 ${data.total_found} offres trouvées pour "${data.query}"
                        </h2>
                    `;
                    
                    data.jobs.forEach(job => {
                        jobsHtml += `
                            <div class="job-card">
                                <h3>${job.title}</h3>
                                <p class="company">🏢 ${job.company}</p>
                                <p class="location">📍 ${job.location}</p>
                                <p class="description">${job.description}</p>
                                <div class="tags">
                                    <span class="tag">📅 ${job.days_ago} jour(s)</span>
                                    <span class="tag">${job.job_type}</span>
                                    <span class="tag">💰 ${job.salary}</span>
                                    ${job.skills.map(s => `<span class="tag">${s}</span>`).join('')}
                                </div>
                                <a href="${job.url}" target="_blank" class="btn-apply">
                                    ➡️ Postuler sur ${job.source.charAt(0).toUpperCase() + job.source.slice(1)}
                                </a>
                            </div>
                        `;
                    });
                    
                    results.innerHTML = jobsHtml;
                }
            } catch (error) {
                console.error('Erreur:', error);
                results.innerHTML = `
                    <div class="no-results">
                        <h3 style="color: red;">❌ Erreur</h3>
                        <p>Une erreur s'est produite: ${error.message}</p>
                        <p>Veuillez réessayer dans quelques instants.</p>
                    </div>
                `;
            }
            
            // Masquer le loader
            searchBtn.style.display = 'block';
            loading.style.display = 'none';
        });
    </script>
</body>
</html>
"""

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Page d'accueil"""
    return HOME_TEMPLATE

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Page de connexion"""
    return """
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Connexion - CloudJobHunt</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #0066cc 0%, #004499 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .login-box {
                background: white;
                padding: 40px;
                border-radius: 15px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.2);
                width: 100%;
                max-width: 400px;
            }
            .logo { 
                font-size: 36px; 
                font-weight: bold; 
                color: #0066cc; 
                text-align: center;
                display: block;
                margin-bottom: 30px;
                text-decoration: none;
            }
            h1 { text-align: center; margin-bottom: 30px; color: #333; }
            input {
                width: 100%;
                padding: 15px;
                margin: 10px 0;
                border: 2px solid #ddd;
                border-radius: 8px;
                font-size: 16px;
            }
            button {
                width: 100%;
                padding: 15px;
                background: linear-gradient(135deg, #0066cc 0%, #004499 100%);
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 18px;
                font-weight: bold;
                cursor: pointer;
                margin-top: 20px;
            }
            button:hover { opacity: 0.9; }
            .links { text-align: center; margin-top: 20px; }
            .links a { color: #0066cc; text-decoration: none; }
        </style>
    </head>
    <body>
        <div class="login-box">
            <a href="/" class="logo">🚀 CloudJobHunt</a>
            <h1>Connexion</h1>
            <form id="loginForm">
                <input type="email" id="email" placeholder="Email" required>
                <input type="password" id="password" placeholder="Mot de passe" required>
                <button type="submit">Se connecter</button>
            </form>
            <div class="links">
                <p>Pas de compte? <a href="/register">S'inscrire</a></p>
                <p style="margin-top: 10px;"><a href="/">← Retour à l'accueil</a></p>
            </div>
        </div>
        <script>
            document.getElementById('loginForm').addEventListener('submit', async function(e) {
                e.preventDefault();
                const email = document.getElementById('email').value;
                const password = document.getElementById('password').value;
                
                try {
                    const response = await fetch('/api/v1/auth/login', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({username: email, password: password})
                    });
                    
                    if (response.ok) {
                        const data = await response.json();
                        localStorage.setItem('token', data.access_token);
                        window.location.href = '/';
                    } else {
                        alert('Erreur de connexion. Vérifiez vos identifiants.');
                    }
                } catch (error) {
                    alert('Erreur: ' + error.message);
                }
            });
        </script>
    </body>
    </html>
    """

@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    """Page d'inscription"""
    return """
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Inscription - CloudJobHunt</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #0066cc 0%, #004499 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .register-box {
                background: white;
                padding: 40px;
                border-radius: 15px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.2);
                width: 100%;
                max-width: 400px;
            }
            .logo { 
                font-size: 36px; 
                font-weight: bold; 
                color: #0066cc; 
                text-align: center;
                display: block;
                margin-bottom: 30px;
                text-decoration: none;
            }
            h1 { text-align: center; margin-bottom: 30px; color: #333; }
            input {
                width: 100%;
                padding: 15px;
                margin: 10px 0;
                border: 2px solid #ddd;
                border-radius: 8px;
                font-size: 16px;
            }
            button {
                width: 100%;
                padding: 15px;
                background: linear-gradient(135deg, #0066cc 0%, #004499 100%);
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 18px;
                font-weight: bold;
                cursor: pointer;
                margin-top: 20px;
            }
            button:hover { opacity: 0.9; }
            .links { text-align: center; margin-top: 20px; }
            .links a { color: #0066cc; text-decoration: none; }
        </style>
    </head>
    <body>
        <div class="register-box">
            <a href="/" class="logo">🚀 CloudJobHunt</a>
            <h1>Inscription</h1>
            <form id="registerForm">
                <input type="text" id="name" placeholder="Nom complet" required>
                <input type="email" id="email" placeholder="Email" required>
                <input type="password" id="password" placeholder="Mot de passe" required>
                <button type="submit">S'inscrire</button>
            </form>
            <div class="links">
                <p>Déjà un compte? <a href="/login">Se connecter</a></p>
                <p style="margin-top: 10px;"><a href="/">← Retour à l'accueil</a></p>
            </div>
        </div>
        <script>
            document.getElementById('registerForm').addEventListener('submit', async function(e) {
                e.preventDefault();
                const name = document.getElementById('name').value;
                const email = document.getElementById('email').value;
                const password = document.getElementById('password').value;
                
                try {
                    const response = await fetch('/api/v1/auth/register', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({email: email, password: password, full_name: name})
                    });
                    
                    if (response.ok) {
                        const data = await response.json();
                        localStorage.setItem('token', data.access_token);
                        window.location.href = '/';
                    } else {
                        const error = await response.json();
                        alert('Erreur: ' + (error.detail || 'Inscription échouée'));
                    }
                } catch (error) {
                    alert('Erreur: ' + error.message);
                }
            });
        </script>
    </body>
    </html>
    """
