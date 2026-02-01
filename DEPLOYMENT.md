# 🚀 CloudJobHunt - Guide de Déploiement & Configuration

## 📋 Table des matières
1. [Installation locale](#installation-locale)
2. [Configuration nginx](#configuration-nginx)
3. [Lancement du service](#lancement-du-service)
4. [Accès au site](#accès-au-site)

---

## Installation locale

### Prérequis
- Python 3.12+
- PostgreSQL (local ou remote)
- nginx (pour reverse proxy)
- Git

### Étape 1 : Cloner et configurer l'environnement

```bash
cd /home/jihed/CloudJobHunt-Project/cloudjobhunt-infrastructure

# Créer l'environnement virtuel
python3 -m venv .venv

# L'activer
source .venv/bin/activate  # Sur Linux/Mac
# ou
.venv\Scripts\activate  # Sur Windows

# Installer les dépendances
pip install -r requirements.txt
```

### Étape 2 : Configurer la base de données

Deux options :

#### Option A : PostgreSQL local (développement)

```bash
# Installer PostgreSQL (si pas déjà installé)
# Ubuntu/Debian:
sudo apt-get install postgresql postgresql-contrib
# Mac:
brew install postgresql@15

# Démarrer le service PostgreSQL
sudo service postgresql start  # Linux
# ou
brew services start postgresql@15  # Mac

# Se connecter et créer la base
psql -U postgres

# Dans psql:
CREATE DATABASE cloudjobhunt;
CREATE USER cloudjobhunt_user WITH PASSWORD 'secure_password_123';
ALTER ROLE cloudjobhunt_user SET client_encoding TO 'utf8';
ALTER ROLE cloudjobhunt_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE cloudjobhunt_user SET default_transaction_deferrable TO on;
ALTER ROLE cloudjobhunt_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE cloudjobhunt TO cloudjobhunt_user;
\q
```

Puis exporter les variables :

```bash
export DATABASE_HOST=localhost
export DATABASE_PORT=5432
export DATABASE_NAME=cloudjobhunt
export DATABASE_USER=cloudjobhunt_user
export DATABASE_PASSWORD=secure_password_123
export SECRET_KEY=your-secret-key-change-in-production
```

#### Option B : PostgreSQL sur Azure (production)

```bash
export DATABASE_HOST=your-pg-server.postgres.database.azure.com
export DATABASE_PORT=5432
export DATABASE_NAME=cloudjobhunt
export DATABASE_USER=yourusername@yourserver
export DATABASE_PASSWORD=YourSecurePassword123!
export SECRET_KEY=$(openssl rand -hex 32)
```

---

## Configuration nginx

### Étape 1 : Copier la configuration

```bash
# Copier la config nginx fournie
sudo cp nginx.conf /etc/nginx/sites-available/cloudjobhunt
sudo ln -s /etc/nginx/sites-available/cloudjobhunt /etc/nginx/sites-enabled/cloudjobhunt

# Ou remplacer la config par défaut
sudo cp nginx.conf /etc/nginx/conf.d/cloudjobhunt.conf
```

### Étape 2 : Tester la configuration nginx

```bash
sudo nginx -t
# Output: nginx: configuration file /etc/nginx/nginx.conf test is successful
```

### Étape 3 : Redémarrer nginx

```bash
sudo systemctl restart nginx
# ou
sudo service nginx restart
```

### Étape 4 : Vérifier le statut

```bash
sudo systemctl status nginx
sudo netstat -tlnp | grep :80  # Vérifier que port 80 est en écoute
```

---

## Lancement du service

### Option 1 : Développement (mode rechargement auto)

```bash
source .venv/bin/activate
export DATABASE_HOST=localhost
export DATABASE_PORT=5432
export DATABASE_NAME=cloudjobhunt
export DATABASE_USER=cloudjobhunt_user
export DATABASE_PASSWORD=secure_password_123
export SECRET_KEY=dev-secret-key

python -m uvicorn main:app \
    --host 0.0.0.0 \
    --port 8000 \
    --reload
```

Ou utiliser le script :

```bash
./start.sh
```

### Option 2 : Production (avec gunicorn & systemd)

#### Créer un service systemd

Créer `/etc/systemd/system/cloudjobhunt.service` :

```ini
[Unit]
Description=CloudJobHunt FastAPI Backend
After=network.target postgresql.service

[Service]
Type=notify
User=www-data
WorkingDirectory=/home/jihed/CloudJobHunt-Project/cloudjobhunt-infrastructure
ExecStart=/home/jihed/CloudJobHunt-Project/cloudjobhunt-infrastructure/.venv/bin/gunicorn \
    -w 4 \
    -k uvicorn.workers.UvicornWorker \
    -b 127.0.0.1:8000 \
    main:app

Environment="DATABASE_HOST=localhost"
Environment="DATABASE_PORT=5432"
Environment="DATABASE_NAME=cloudjobhunt"
Environment="DATABASE_USER=cloudjobhunt_user"
Environment="DATABASE_PASSWORD=secure_password_123"
Environment="SECRET_KEY=your-secret-key-change-in-production"
Environment="PYTHONUNBUFFERED=1"

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Puis :

```bash
sudo systemctl daemon-reload
sudo systemctl enable cloudjobhunt
sudo systemctl start cloudjobhunt
sudo systemctl status cloudjobhunt
```

---

## Accès au site

Une fois l'API en cours d'exécution et nginx configuré :

- **Accueil** : https://cloudjobhunt.42web.io  
- **Inscription** : https://cloudjobhunt.42web.io/register  
- **Connexion** : https://cloudjobhunt.42web.io/login  
- **API Docs** : https://cloudjobhunt.42web.io/docs  
- **Health** : https://cloudjobhunt.42web.io/health  

### Tester la connexion API

```bash
# Test health
curl http://localhost:8000/health

# Accueil (HTML)
curl http://localhost:8000/

# Test public endpoint
curl http://localhost:8000/api/v1/test-public

# Test recherche
curl "http://localhost:8000/api/v1/search?q=python&location=Paris"
```

### Tester l'inscription

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email":"user@example.com",
    "password":"password123",
    "full_name":"Test User"
  }'
```

---

## 🔧 Dépannage

### nginx : 502 Bad Gateway
- Vérifier que l'API uvicorn écoute sur `127.0.0.1:8000`
- Vérifier la config nginx : `sudo nginx -t`
- Regarder les logs : `sudo tail -f /var/log/nginx/cloudjobhunt_error.log`

### Erreur de connexion à la base de données
```bash
# Vérifier PostgreSQL
sudo systemctl status postgresql
psql -h localhost -U cloudjobhunt_user -d cloudjobhunt

# Vérifier les variables d'env
echo $DATABASE_HOST
echo $DATABASE_USER
```

### Port 8000 déjà utilisé
```bash
lsof -i :8000
kill -9 <PID>
```

### SSL/TLS (HTTPS)

Pour activer HTTPS avec Let's Encrypt :

```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot certonly --nginx -d cloudjobhunt.42web.io

# Mettre à jour la config nginx pour rediriger HTTP → HTTPS
# Décommenter les lignes 'return 301 https' dans nginx.conf
```

---

## 📞 Support & Logs

Logs nginx :
```bash
sudo tail -f /var/log/nginx/cloudjobhunt_access.log
sudo tail -f /var/log/nginx/cloudjobhunt_error.log
```

Logs uvicorn (si en dev) :
```bash
# Visible dans le terminal où vous avez lancé ./start.sh
```

Logs systemd (si en production) :
```bash
sudo journalctl -u cloudjobhunt -f
```

---

**✅ Vous êtes prêt à déployer !**
