<<<<<<< HEAD
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
│   └── networking/    # Module réseau
└── environments/      # Configurations par environnement
    └── dev/           # Environnement développement
```

## 🔐 Sécurité

- Network Security Groups configurés
- Subnets isolés par fonction
- Tags pour gestion des coûts
=======
# cloudjobhunt-infrastructure
cloudjobhunt-infrastructure
>>>>>>> origin/main
