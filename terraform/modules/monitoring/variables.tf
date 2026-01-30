variable "project_name" {
  description = "Nom du projet"
  type        = string
}

variable "environment" {
  description = "Environnement"
  type        = string
}

variable "location" {
  description = "Région Azure"
  type        = string
}

variable "resource_group_name" {
  description = "Nom du Resource Group"
  type        = string
}

variable "sku" {
  description = "SKU du Log Analytics (Free, PerGB2018)"
  type        = string
  default     = "PerGB2018"
}

variable "retention_in_days" {
  description = "Rétention des logs en jours"
  type        = number
  default     = 30
}
