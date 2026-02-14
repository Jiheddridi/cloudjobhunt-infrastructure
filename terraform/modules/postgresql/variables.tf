variable "resource_group_name" {
  description = "Nom du resource group"
  type        = string
  default     = "jobhunt-dev-rg"
}

variable "location" {
  description = "Région Azure"
  type        = string
  default     = "francecentral"
}

variable "admin_username" {
  description = "Nom d'utilisateur administrateur PostgreSQL"
  type        = string
  default     = "dbadmin"
}

variable "admin_password" {
  description = "Mot de passe administrateur PostgreSQL"
  type        = string
  sensitive   = true
}

variable "vnet_id" {
  description = "ID du réseau virtuel jobhunt-vnet"
  type        = string
}

variable "subnet_id" {
  description = "ID du sous-réseau délégué à PostgreSQL"
  type        = string
}

variable "tags" {
  description = "Tags applicables aux ressources"
  type        = map(string)
  default = {
    Environment = "Development"
    Project     = "CloudJobHunt"
  }
}
