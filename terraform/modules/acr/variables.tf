variable "project_name" {
  description = "Nom du projet"
  type        = string
}

variable "environment" {
  description = "Environnement (dev / prod)"
  type        = string
}

variable "location" {
  description = "Région Azure"
  type        = string
}

variable "resource_group_name" {
  description = "Resource Group"
  type        = string
}

variable "sku" {
  description = "SKU ACR"
  type        = string
  default     = "Basic"
}

variable "admin_enabled" {
  description = "Admin user (DEV uniquement)"
  type        = bool
  default     = true
}

variable "public_network_access_enabled" {
  description = "Accès public ACR"
  type        = bool
  default     = true
}

variable "create_cicd_token" {
  description = "Créer token CI/CD"
  type        = bool
  default     = true
}

