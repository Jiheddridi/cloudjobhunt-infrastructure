# 🚀 CloudJobHunt - Infrastructure DevOps Full-Stack

Projet DevOps complet avec pipeline CI/CD automatisé et système de monitoring.

## 📋 Table des matières

- [Architecture](#architecture)
- [Technologies](#technologies)
- [Structure du projet](#structure-du-projet)
- [Installation](#installation)
- [Monitoring](#monitoring)
- [CI/CD Pipeline](#cicd-pipeline)
- [Configuration](#configuration)

---

## 🏗️ Architecture
```

╔══════════════════════════════════════════════════════════════════════╗
║                          PIPELINE DEVOPS                             ║
╚══════════════════════════════════════════════════════════════════════╝

        ┌──────────────┐
        │  Développeur │
        └──────┬───────┘
               │
               ▼
        ┌──────────────┐
        │   Git Commit │
        └──────┬───────┘
               │
               ▼
┌──────────────────────────────────────────────────────────────────────┐
│                         Jenkins Pipeline                              │
│                  Build  →  Test  →  Deploy                            │
└──────────────┬──────────────────────────────────────────────┬────────┘
               │                                              │
               ▼                                              ▼
        ┌──────────────┐                              ┌──────────────┐
        │ Docker Build │                              │ Docker Push  │
        └──────┬───────┘                              └──────┬───────┘
               │                                              │
               └──────────────────────┬───────────────────────┘
                                      ▼
                             ┌────────────────┐
                             │   Docker Hub   │
                             └────────┬───────┘
                                      │
                                      ▼
╔══════════════════════════════════════════════════════════════════════╗
║                       Kubernetes Cluster                              ║
║                                                                      ║
║   ┌────────────┐    ┌────────────┐    ┌────────────┐                ║
║   │  Frontend  │    │  Backend   │    │   MySQL    │                ║
║   │   React    │    │  Spring    │    │  Database  │                ║
║   └─────┬──────┘    └─────┬──────┘    └─────┬──────┘                ║
║         │                 │                 │                       ║
║         └───────────┬─────┴─────┬───────────┘                       ║
║                     ▼           ▼                                   ║
║                ┌────────────────────┐                               ║
║                │   Services / Ingress│                               ║
║                └──────────┬─────────┘                               ║
╚═══════════════════════════┼══════════════════════════════════════════╝
                            │
                            ▼
┌──────────────────────────────────────────────────────────────────────┐
│               Prometheus – Collecte des métriques                     │
│          CPU • RAM • Pods • Nodes • Services                          │
└───────────────────────────┬──────────────────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────────────────┐
│                  Grafana – Visualisation                              │
│          Dashboards • Charts • Health Status                          │
└───────────────────────────┬──────────────────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────────────────┐
│                Alertmanager – Notifications                           │
│          Email • Slack • Webhook • SMS                                │
└──────────────────────────────────────────────────────────────────────┘




```

---

## 🛠️ Technologies

### Application
- **Frontend** : React.js
- **Backend** : Spring Boot (Java)
- **Database** : MySQL

### DevOps
- **Containerisation** : Docker, Docker Hub
- **Orchestration** : Kubernetes
- **CI/CD** : Jenkins, Jenkinsfile
- **Monitoring** : Prometheus, Grafana
- **Alerting** : Alertmanager
- **IaC** : YAML, Helm

### Infrastructure
- **OS** : Linux Ubuntu
- **Container Runtime** : Docker
- **Orchestrateur** : Kubernetes

---

## 📁 Structure du projet
```
cloudjobhunt-infrastructure/
├── k8s/                          # Manifestes Kubernetes
│   ├── backend/
│   │   ├── deployment.yaml
│   │   └── service.yaml
│   ├── frontend/
│   │   ├── deployment.yaml
│   │   └── service.yaml
│   └── mysql/
│       ├── deployment.yaml
│       ├── service.yaml
│       └── pvc.yaml
├── monitoring/                   # Configuration Monitoring
│   ├── custom-alerts.yaml
│   ├── alertmanager-config.example.yaml
│   ├── grafana-ingress.yaml
│   └── stress-test.yaml
├── jenkins/                      # Pipeline CI/CD
│   └── Jenkinsfile
├── docker/                       # Dockerfiles
│   ├── frontend/
│   ├── backend/
│   └── mysql/
└── README.md
```

---

## 🚀 Installation

### Prérequis

- Docker installé
- Kubernetes cluster configuré (minikube, kind, ou cloud)
- kubectl configuré
- Helm 3.x
- Jenkins avec plugins nécessaires

### 1. Déployer l'application sur Kubernetes
```bash
# Créer les namespaces
kubectl create namespace default
kubectl create namespace monitoring

# Déployer MySQL
kubectl apply -f k8s/mysql/

# Déployer Backend
kubectl apply -f k8s/backend/

# Déployer Frontend
kubectl apply -f k8s/frontend/

# Vérifier les pods
kubectl get pods
```

### 2. Installer le stack Monitoring
```bash
# Ajouter le repo Helm Prometheus
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# Installer Prometheus + Grafana + Alertmanager
helm install prometheus prometheus-community/kube-prometheus-stack -n monitoring

# Vérifier l'installation
kubectl get pods -n monitoring
```

### 3. Configurer les alertes
```bash
# Appliquer les règles d'alerte
kubectl apply -f monitoring/custom-alerts.yaml

# Configurer Alertmanager (après avoir modifié avec vos credentials)
cp monitoring/alertmanager-config.example.yaml monitoring/alertmanager-config.yaml
nano monitoring/alertmanager-config.yaml  # Ajouter vos emails
kubectl apply -f monitoring/alertmanager-config.yaml
kubectl delete pod -n monitoring -l app.kubernetes.io/name=alertmanager
```

---

## 📊 Monitoring

### Accéder à Grafana
```bash
# Port-forward
kubectl port-forward -n monitoring svc/prometheus-grafana 3000:80

# Récupérer le mot de passe
kubectl get secret -n monitoring prometheus-grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo
```

Ouvrir : http://localhost:3000
- Username: `admin`
- Password: (celui récupéré ci-dessus)

### Dashboards disponibles

- **Kubernetes / Compute Resources / Cluster** : Vue globale
- **Kubernetes / Compute Resources / Namespace (Pods)** : CPU/RAM par pod
- **Kubernetes / Compute Resources / Pod** : Détails d'un pod

### Accéder à Prometheus
```bash
kubectl port-forward -n monitoring svc/prometheus-kube-prometheus-prometheus 9090:9090
```

Ouvrir : http://localhost:9090

### Accéder à Alertmanager
```bash
kubectl port-forward -n monitoring svc/alertmanager-operated 9093:9093
```

Ouvrir : http://localhost:9093

---

## 🔔 Alertes configurées

| Alerte | Condition | Sévérité | Durée |
|--------|-----------|----------|-------|
| PodCPUUsageHigh | CPU > 50% | Warning | 2 min |
| PodMemoryUsageHigh | RAM > 90% | Warning | 2 min |
| PodRestartingFrequently | Restarts > 0 | Critical | 2 min |
| PodNotReady | Pod not Running | Critical | 5 min |
| DeploymentReplicasMismatch | Replicas ≠ Available | Warning | 5 min |

---

## ⚙️ CI/CD Pipeline

### Étapes du pipeline Jenkins

1. **Checkout** : Clone du code depuis Git
2. **Build** : Maven/npm build avec tests
3. **Docker Build** : Construction des images
4. **Docker Push** : Push vers Docker Hub
5. **Deploy** : Déploiement sur Kubernetes
6. **Verify** : Vérification du déploiement

### Jenkinsfile

Le pipeline est défini dans `jenkins/Jenkinsfile` (déclaratif)

### Déclenchement

- Manuel : Clic sur "Build Now" dans Jenkins
- Automatique : Webhook Git (push sur main)

---

## 🔧 Configuration

### Variables d'environnement

À configurer dans `alertmanager-config.yaml` :
```yaml
YOUR_ADMIN_EMAIL@example.com      → Votre email admin
YOUR_TEAM_EMAIL@example.com       → Email de l'équipe
YOUR_GMAIL_ADDRESS@gmail.com      → Votre Gmail
YOUR_GMAIL_APP_PASSWORD           → App Password Gmail
```

### Obtenir un App Password Gmail

1. https://myaccount.google.com/apppasswords
2. Créer "Alertmanager Kubernetes"
3. Copier le mot de passe (16 caractères)

---

## 📈 Résultats

- ✅ **Automatisation** : 100% automatisé, Git to Production
- ✅ **Déploiement** : < 5 minutes
- ✅ **Monitoring** : 24/7 en temps réel
- ✅ **Alerting** : 5 alertes configurées et testées
- ✅ **High Availability** : Réplication des pods
- ✅ **Zero Downtime** : Rolling updates

---

## 🧪 Tests

### Tester les alertes
```bash
# Lancer un pod stress CPU
kubectl apply -f monitoring/stress-test.yaml

# Vérifier le CPU
kubectl top pod cpu-stress-test

# Attendre 2 minutes → Alerte se déclenche
# Vérifier dans Prometheus → Alerts
# Vérifier email reçu

# Nettoyer
kubectl delete -f monitoring/stress-test.yaml
```

---

## 📝 Commandes utiles
```bash
# Voir tous les pods
kubectl get pods -A

# Logs d'un pod
kubectl logs <pod-name>

# Describe un pod
kubectl describe pod <pod-name>

# Redémarrer un deployment
kubectl rollout restart deployment <deployment-name>

# Voir les métriques
kubectl top pods
kubectl top nodes

# Accéder à un pod
kubectl exec -it <pod-name> -- /bin/bash
```

---

## 🤝 Contribution

Ce projet est un portfolio DevOps. N'hésitez pas à l'utiliser comme référence !

---

## 📧 Contact

- **LinkedIn** : [Votre profil]
- **GitHub** : [Votre GitHub]
- **Email** : [Votre email]

---

## 📄 Licence

MIT License - Libre d'utilisation pour apprentissage

---

## 🏆 Compétences démontrées

- Architecture Microservices
- Containerisation Docker
- Orchestration Kubernetes
- CI/CD avec Jenkins
- Infrastructure as Code
- Monitoring & Observabilité
- Alerting automatisé
- DevOps Best Practices
- Production-Ready Infrastructure

---

**⭐ Si ce projet vous a aidé, n'hésitez pas à mettre une étoile !**
