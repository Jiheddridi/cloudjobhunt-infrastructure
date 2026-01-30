terraform {
  required_version = ">= 1.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "main" {
  name     = "rg-${var.project_name}-${var.environment}"
  location = var.location
  tags = {
    Environment = var.environment
    Project     = var.project_name
    ManagedBy   = "Terraform"
  }
}

module "networking" {
  source              = "../../modules/networking"
  project_name        = var.project_name
  environment         = var.environment
  location            = var.location
  resource_group_name = azurerm_resource_group.main.name
  vnet_address_space             = "10.0.0.0/16"
  aks_subnet_address_prefix      = "10.0.1.0/24"
  database_subnet_address_prefix = "10.0.2.0/24"
  ingress_subnet_address_prefix  = "10.0.3.0/24"
}

module "monitoring" {
  source              = "../../modules/monitoring"
  project_name        = var.project_name
  environment         = var.environment
  location            = var.location
  resource_group_name = azurerm_resource_group.main.name
  sku               = "PerGB2018"
  retention_in_days = 30
}

module "acr" {
  source              = "../../modules/acr"
  project_name        = var.project_name
  environment         = var.environment
  location            = var.location
  resource_group_name = azurerm_resource_group.main.name
  sku                           = "Basic"
  admin_enabled                 = true
  public_network_access_enabled = true
  create_cicd_token             = false
}

module "aks" {
  source              = "../../modules/aks"
  project_name        = var.project_name
  environment         = var.environment
  location            = var.location
  resource_group_name = azurerm_resource_group.main.name
  aks_subnet_id  = module.networking.aks_subnet_id
  service_cidr   = "10.1.0.0/16"
  dns_service_ip = "10.1.0.10"
  kubernetes_version        = null
  automatic_channel_upgrade = "patch"
  system_node_pool_vm_size   = "Standard_D2s_v3"
  system_node_pool_min_count = 1
  system_node_pool_max_count = 3
  user_node_pool_vm_size   = "Standard_D2s_v3"
  user_node_pool_min_count = 1
  user_node_pool_max_count = 5
  acr_id                     = module.acr.acr_id
  log_analytics_workspace_id = module.monitoring.workspace_id
  depends_on = [module.networking, module.monitoring, module.acr]
}
