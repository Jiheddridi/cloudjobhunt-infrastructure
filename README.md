# CloudJobHunt AI - Infrastructure as Code

## 🏗️ Architecture

Voir `docs/architecture-network.drawio`

## 🚀 Déploiement

### Prérequis
- Azure CLI installé et connecté
- Terraform >= 1.0
- Compte Azure avec crédits

### Déploiement environnement DEV
```bash
cd terraform/environments/dev
terraform init
terraform plan
terraform apply
```

### Destruction (si besoin de tout supprimer)
```bash
terraform destroy
```

## 📂 Structure
```
terraform/
├── modules/           # Code réutilisable
│   ├── acr/           # Azure Container Registry
│   ├── aks/           # Azure Kubernetes Service
│   ├── database/      # PostgreSQL Flexible
│   ├── monitoring/    # Log Analytics
│   └── networking/    # VNet, Subnets, NSG
└── environments/      # Configurations par environnement
    └── dev/           # Environnement développement

k8s/                   # Manifests Kubernetes
ansible/               # Playbooks Ansible (future utilisation)
```

## 🔐 Sécurité

- Network Security Groups configurés
- Subnets isolés par fonction
- Tags pour gestion des coûts
- Azure AD RBAC pour AKS
- Private DNS pour base de données

## 📦 Composants

| Composant | Description |
|-----------|-------------|
| **AKS** | Cluster Kubernetes avec 2 node pools |
| **ACR** | Azure Container Registry |
| **PostgreSQL** | Flexible Server avec accès privé |
| **Log Analytics** | Monitoring et Container Insights |

## 🧪 Tests

```bash
# Tester l'application locale
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000

# Tester Docker
docker build -t cloudjobhunt-backend:latest .
docker run -p 8000:8000 cloudjobhunt-backend:latest
```
