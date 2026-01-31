
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
![ChatGPT Image 31 janv  2026, 21_58_01](https://github.com/user-attachments/assets/3500d5b6-9a6a-4370-bee3-24258df52372)

### Destruction (si besoin de tout supprimer)
```bash
terraform destroy
```

## 📂 Structure
```
terraform/
├── modules/           # Code réutilisable
│   └── networking/    # Module réseau
└── environments/      # Configurations par environnement
    └── dev/           # Environnement développement
```
)


## 🔐 Sécurité

- Network Security Groups configurés
- Subnets isolés par fonction
- Tags pour gestion des coûts
=======
# cloudjobhunt-infrastructure
cloudjobhunt-infrastructure
