variable "project_name" {
  description = "Nom du projet"
  type        = string
}

variable "environment" {
  description = "Environnement (dev, staging, prod)"
  type        = string
}

variable "location" {
  description = "Région Azure"
  type        = string
}

variable "resource_group_name" {
  description = "Nom du Resource Group existant"
  type        = string
}

variable "vnet_address_space" {
  description = "CIDR du Virtual Network"
  type        = string
  default     = "10.0.0.0/16"
}

variable "aks_subnet_address_prefix" {
  description = "CIDR du subnet AKS"
  type        = string
  default     = "10.0.1.0/24"
}

variable "database_subnet_address_prefix" {
  description = "CIDR du subnet Database"
  type        = string
  default     = "10.0.2.0/24"
}

variable "ingress_subnet_address_prefix" {
  description = "CIDR du subnet Ingress"
  type        = string
  default     = "10.0.3.0/24"
}

