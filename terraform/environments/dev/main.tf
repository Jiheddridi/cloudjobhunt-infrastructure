terraform {
  required_providers {
    azurerm = { source = "hashicorp/azurerm", version = "~> 3.0" }
  }
}
provider "azurerm" {
  features {}
}
resource "azurerm_resource_group" "main" {
  name     = "rg-${var.project_name}-${var.environment}"
  location = var.location
  tags = { Environment = var.environment, Project = var.project_name }
}
module "networking" {
  source = "../../modules/networking"
  project_name         = var.project_name
  environment          = var.environment
  location             = var.location
  resource_group_name  = azurerm_resource_group.main.name
  vnet_address_space   = var.vnet_address_space
  subnet_aks_cidr      = var.subnet_aks_cidr
  subnet_database_cidr = var.subnet_database_cidr
  subnet_ingress_cidr  = var.subnet_ingress_cidr
}
module "acr" {
  source = "../../modules/acr"
  project_name        = var.project_name
  environment         = var.environment
  location            = var.location
  resource_group_name = azurerm_resource_group.main.name
  depends_on = [azurerm_resource_group.main]
}
module "aks" {
  source = "../../modules/aks"
  project_name             = var.project_name
  environment              = var.environment
  location                 = var.location
  resource_group_name      = azurerm_resource_group.main.name
  vnet_id                  = module.networking.vnet_id
  subnet_id                = module.networking.aks_subnet_id
  acr_id                   = module.acr.acr_id
  acr_name                 = module.acr.acr_name
  service_cidr             = "10.1.0.0/16"
  dns_service_ip           = "10.1.0.10"
  docker_bridge_cidr       = "172.17.0.1/16"
  depends_on = [module.networking, module.acr]
}
module "monitoring" {
  source = "../../modules/monitoring"
  project_name        = var.project_name
  environment         = var.environment
  location            = var.location
  resource_group_name = azurerm_resource_group.main.name
  depends_on = [azurerm_resource_group.main]
}
module "database" {
  source = "../../modules/database"
  project_name        = var.project_name
  environment         = var.environment
  location            = var.location
  resource_group_name = azurerm_resource_group.main.name
  vnet_id            = module.networking.vnet_id
  database_subnet_id = module.networking.database_subnet_id
  aks_subnet_cidr    = var.subnet_aks_cidr
  sku_name           = "B_Standard_B1ms"
  storage_mb         = 32768
  admin_username     = "psqladmin"
  admin_password     = var.db_password
  database_name      = "cloudjobhunt"
  depends_on = [module.networking, module.aks]
}
