terraform {
  required_version = ">= 1.5"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.80"
    }
  }
}

provider "azurerm" {
  features {}
}

# RESOURCE GROUP DEV
resource "azurerm_resource_group" "main" {
  name     = "rg-cloudhunt-dev"
  location = var.location

  tags = {
    Environment = var.environment
    Project     = var.project_name
    ManagedBy   = "Terraform"
    CostCenter  = "DevOps-Training"
  }
}

# MODULE NETWORKING
module "networking" {
  source = "../../modules/networking"

  project_name        = var.project_name
  environment         = var.environment
  location            = var.location
  resource_group_name = azurerm_resource_group.main.name

  vnet_address_space             = "10.0.0.0/16"
  aks_subnet_address_prefix      = "10.0.1.0/24"
  database_subnet_address_prefix = "10.0.2.0/24"
  ingress_subnet_address_prefix  = "10.0.3.0/24"
}

