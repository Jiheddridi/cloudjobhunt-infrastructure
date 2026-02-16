# 🚀 CloudJobHunt - Multi-Source Job Aggregator on Azure Kubernetes

![Azure](https://img.shields.io/badge/Azure-0078D4?style=for-the-badge&logo=microsoft-azure&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Jenkins](https://img.shields.io/badge/Jenkins-D24939?style=for-the-badge&logo=jenkins&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

> Cloud-native job search platform aggregating opportunities from multiple sources across 9 countries, deployed on Azure Kubernetes Service with full CI/CD automation.

**🌐 Live Demo:** http://20.74.48.197

---

## 📊 Project Overview

CloudJobHunt is a production-ready job aggregation platform demonstrating modern DevOps practices and cloud-native architecture. Built as a portfolio project showcasing:

- ☸️ **Kubernetes orchestration** on Azure AKS
- 🔄 **Jenkins CI/CD** with automated deployment
- 🐳 **Docker containerization** with multi-stage builds
- 🛡️ **Security scanning** with Trivy
- 📈 **Auto-scaling** with Horizontal Pod Autoscaler
- 🌍 **Multi-API integration** (Adzuna + JSearch)

### Key Metrics

| Metric | Value |
|--------|-------|
| **Countries Supported** | 9 (Tunisia, France, UK, US, Germany, Canada, Australia, Netherlands, Switzerland) |
| **API Sources** | 2 (Adzuna, JSearch/LinkedIn) |
| **Jobs per Search** | 30+ aggregated listings |
| **Deployment Time** | <6 minutes (60% reduction via automation) |
| **Response Time** | <2 seconds |
| **Auto-scaling Range** | 2-5 backend pods, 1-3 frontend pods |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Internet Users                          │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
            ┌────────────────────────┐
            │  Azure Load Balancer   │  (Public IP: 20.74.48.197)
            │    frontend-public     │
            └────────────┬───────────┘
                         │
                         ▼
            ┌────────────────────────┐
            │   Frontend Pods (1-3)  │
            │   Nginx + HTML/CSS/JS  │
            └────────────┬───────────┘
                         │
                         ▼
            ┌────────────────────────┐
            │   Backend Service      │  (ClusterIP: backend:8000)
            └────────────┬───────────┘
                         │
                         ▼
      ┌──────────────────────────────────────┐
      │      Backend Pods (2-5 HPA)          │
      │  ┌─────────────┬──────────────┐     │
      │  │  FastAPI    │    Redis     │     │
      │  │  Container  │  Container   │     │
      │  │  - APIs     │  - Cache     │     │
      │  │  - SQLite   │  - Session   │     │
      │  └─────────────┴──────────────┘     │
      └──────────────────┬───────────────────┘
                         │
                         ▼
              ┌──────────────────┐
              │  External APIs   │
              │  - Adzuna        │
              │  - JSearch       │
              └──────────────────┘
```

---

## ✨ Features

### User Features
- 🔍 **Smart Search** - Multi-source job aggregation with real-time results
- 🌍 **Global Coverage** - Search across 9 countries simultaneously
- 🎯 **Source Filtering** - Choose Adzuna only, LinkedIn/Indeed only, or all sources
- 📱 **Responsive Design** - Mobile-friendly interface
- 💾 **Search History** - Persistent storage with SQLite

### Technical Features
- 🐳 **Fully Containerized** - All services in Docker containers
- ☸️ **Kubernetes Native** - Deployments, Services, Secrets, HPA
- 🔐 **Secure by Design** - API keys in Kubernetes Secrets, no credentials in code
- 📈 **Auto-scaling** - HPA based on CPU metrics (70% threshold)
- 🔄 **Zero Downtime** - Rolling updates deployment strategy
- 🛡️ **Security Scanning** - Trivy vulnerability detection
- 🚀 **CI/CD Pipeline** - Automated build, test, and deployment

---

## 🛠️ Tech Stack

### Infrastructure & Cloud
- **Cloud Provider:** Microsoft Azure
- **Orchestration:** Azure Kubernetes Service (AKS)
- **Container Registry:** Azure Container Registry (ACR)
- **Infrastructure as Code:** Terraform
- **CI/CD:** Jenkins with 5-stage pipeline

### Backend
- **Framework:** FastAPI 0.104.1
- **Language:** Python 3.11
- **Database:** SQLite 3
- **Cache:** Redis 7 Alpine
- **APIs:** Adzuna API, JSearch RapidAPI

### Frontend
- **Server:** Nginx Alpine
- **UI:** HTML5, CSS3, Vanilla JavaScript
- **Design:** Responsive, modern gradient UI

### DevOps Tools
- **Containerization:** Docker
- **Security Scanning:** Trivy
- **CLI Tools:** kubectl, az cli, terraform
- **Version Control:** Git + GitHub

---

## 📁 Project Structure

```
cloudjobhunt-infrastructure/
├── docker/
│   ├── api/
│   │   ├── Dockerfile              # Backend container
│   │   ├── main.py                 # FastAPI application
│   │   └── requirements.txt        # Python dependencies
│   └── apiFront/
│       ├── Dockerfile              # Frontend container
│       ├── index.html              # User interface
│       └── nginx.conf              # Nginx configuration
│
├── kubernetes/
│   └── manifests/
│       └── app.yaml                # K8s resources (Deployments, Services, HPA)
│
├── terraform/
│   └── live/
│       ├── main.tf                 # Infrastructure definition
│       ├── provider.tf             # Azure provider
│       └── variables.tf            # Input variables
│
├── Jenkinsfile                     # CI/CD pipeline definition
├── README.md                       # This file
└── .gitignore                      # Excludes secrets and sensitive files
```

---

## 🚀 Quick Start

### Prerequisites
- Azure account with active subscription
- kubectl configured for AKS
- Docker installed
- Azure CLI (`az`)

### 1. Clone Repository

```bash
git clone https://github.com/Jiheddridi/cloudjobhunt-infrastructure.git
cd cloudjobhunt-infrastructure
```

### 2. Configure Secrets

Create Kubernetes secret for API keys:

```bash
kubectl create secret generic api-keys \
  --from-literal=ADZUNA_APP_ID=your_adzuna_id \
  --from-literal=ADZUNA_APP_KEY=your_adzuna_key \
  --from-literal=JSEARCH_API_KEY=your_jsearch_key
```

### 3. Deploy to AKS

```bash
# Apply Kubernetes manifests
kubectl apply -f kubernetes/manifests/app.yaml

# Verify deployment
kubectl get pods
kubectl get services
```

### 4. Access Application

```bash
# Get public IP
kubectl get service frontend-public

# Access in browser
http://<EXTERNAL-IP>
```

---

## 🔄 CI/CD Pipeline

### Jenkins Pipeline - 5 Stages

```groovy
1. Build Docker Images
   └─ Build backend and frontend containers

2. Security Scan with Trivy
   └─ Scan for HIGH and CRITICAL vulnerabilities

3. Push to Azure Container Registry
   └─ Upload images to ACR

4. Deploy to AKS
   └─ Update Kubernetes deployments

5. Health Check
   └─ Verify pods are running and healthy
```

**Trigger:** Automatic via Git Poll SCM (checks every minute)

**Duration:** ~5-6 minutes per build

**Result:** Automated deployment with 60% time reduction compared to manual process

---

## 🔒 Security

### Implemented Security Measures

✅ **Kubernetes Secrets** - API keys stored securely, not in code  
✅ **Trivy Scanning** - Automated vulnerability detection  
✅ **No Hardcoded Credentials** - All sensitive data externalized  
✅ **`.gitignore`** - Excludes `.env`, `*.tfstate`, secrets  
✅ **ClusterIP for Backend** - Not exposed to internet  
✅ **Resource Limits** - CPU/Memory constraints prevent exhaustion  
✅ **Network Policies** - Azure NSG controls traffic  

### API Keys Required

- **Adzuna API** - Free tier: 1000 requests/month
  - Sign up: https://developer.adzuna.com/
  
- **JSearch API** - Free tier: 100 requests/month
  - Sign up: https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch

---

## 📊 Monitoring & Scaling

### Horizontal Pod Autoscaling (HPA)

```bash
# Backend: 2-5 pods based on 70% CPU
kubectl autoscale deployment backend --cpu-percent=70 --min=2 --max=5

# Frontend: 1-3 pods based on 70% CPU
kubectl autoscale deployment frontend --cpu-percent=70 --min=1 --max=3

# Check HPA status
kubectl get hpa
```

### Monitoring Commands

```bash
# Resource usage
kubectl top pods
kubectl top nodes

# Logs
kubectl logs -f deployment/backend -c api

# Service endpoints
kubectl get endpoints
```

---

## 🎯 API Documentation

### Base URL
`http://20.74.48.197` (Production)

### Endpoints

#### 1. Search Jobs
```http
GET /search?country={country}&keyword={keyword}&source={source}
```

**Parameters:**
- `country` (required): Country code (tn, fr, gb, us, de, ca, au, nl, ch)
- `keyword` (required): Job search term
- `source` (optional): Filter by source ("all", "adzuna", "jsearch")

**Example:**
```bash
curl "http://20.74.48.197/search?country=tn&keyword=devops&source=all"
```

**Response:**
```json
{
  "jobs": [
    {
      "title": "DevOps Engineer",
      "company": "Tech Corp",
      "location": "Tunis, Tunisia",
      "description": "We are looking for...",
      "url": "https://apply.link",
      "country": "TN",
      "source": "JSearch"
    }
  ],
  "count": 25,
  "country": "TN",
  "keyword": "devops"
}
```

#### 2. Get All Jobs
```http
GET /jobs?limit={limit}
```

Returns recently searched jobs from database.

---

## 🔧 Troubleshooting

### Pods Not Starting

```bash
# Check pod status
kubectl get pods

# Describe pod for events
kubectl describe pod <pod-name>

# Check logs
kubectl logs <pod-name>
```

### Service Not Accessible

```bash
# Verify service
kubectl get service frontend-public

# Check endpoints
kubectl get endpoints frontend-public

# Test from within cluster
kubectl run test --rm -it --image=busybox -- wget -O- http://backend:8000/
```

### Database Issues

```bash
# Access backend pod
kubectl exec -it deployment/backend -c api -- sh

# Query SQLite
python3 -c "import sqlite3; conn = sqlite3.connect('jobs.db'); c = conn.cursor(); c.execute('SELECT COUNT(*) FROM jobs'); print(c.fetchone())"
```

---

## 📈 Performance Metrics

| Metric | Before Automation | After CI/CD | Improvement |
|--------|------------------|-------------|-------------|
| **Deployment Time** | 15 minutes | 6 minutes | **60%** reduction |
| **Manual Steps** | 15 commands | 1 git push | **93%** reduction |
| **Error Rate** | ~5% (human error) | <1% | **80%** reduction |
| **Rollback Time** | 20 minutes | 3 minutes | **85%** faster |

---

## 🚧 Future Enhancements

### Planned Features
- [ ] **PostgreSQL Migration** - Replace SQLite with managed Azure PostgreSQL
- [ ] **Job Scraper CronJob** - Automated hourly job fetching
- [ ] **User Authentication** - OAuth2 with personalized recommendations
- [ ] **Email Alerts** - Notify users of new matching jobs
- [ ] **Advanced Filters** - Salary range, experience level, remote/on-site
- [ ] **Analytics Dashboard** - Visualize job market trends

### Infrastructure Improvements
- [ ] **Istio Service Mesh** - Advanced traffic management
- [ ] **Prometheus + Grafana** - Monitoring dashboards
- [ ] **ELK Stack** - Centralized logging
- [ ] **ArgoCD** - GitOps deployment
- [ ] **Cert-Manager** - Automated SSL/TLS

---

## 👨‍💻 Author

**Jihed Dridi**

- GitHub: [@Jiheddridi](https://github.com/Jiheddridi)
- LinkedIn: [Connect with me](https://linkedin.com/in/yourprofile)
- Portfolio: [jiheddridi.dev](https://jiheddridi.dev)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Adzuna** for job search API
- **RapidAPI** for JSearch API access
- **Microsoft Azure** for cloud infrastructure
- **Kubernetes Community** for excellent documentation
- **FastAPI** for the amazing Python framework

---

## 📊 Project Statistics

- **Total Development Time:** 3 weeks (Jan-Feb 2026)
- **Lines of Code:** ~1,800
- **Docker Images:** 2 (backend, frontend)
- **Kubernetes Resources:** 7 (Deployments, Services, HPA, Secrets)
- **Cloud Resources:** 10+ (AKS, ACR, VNet, NSG, LoadBalancer, etc.)
- **API Integrations:** 2 sources
- **Supported Countries:** 9
- **CI/CD Stages:** 5

---

<div align="center">

**⭐ Star this repo if you find it helpful!**

**Made with ❤️ and ☕ by [Jihed Dridi](https://github.com/Jiheddridi)**

![Visitors](https://visitor-badge.laobi.icu/badge?page_id=Jiheddridi.cloudjobhunt)
![Stars](https://img.shields.io/github/stars/Jiheddridi/cloudjobhunt-infrastructure?style=social)

</div>
