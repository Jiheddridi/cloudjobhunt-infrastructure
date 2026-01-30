resource "azurerm_container_registry" "main" {

  # ⚠️ Nom UNIQUE Azure (sans tirets)
  name = "acr${var.project_name}${var.environment}"

  resource_group_name = var.resource_group_name
  location            = var.location

  sku           = var.sku
  admin_enabled = var.admin_enabled

  public_network_access_enabled = var.public_network_access_enabled

  tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "Terraform"
    Service     = "ACR"
  }
}

# Permissions PULL uniquement
resource "azurerm_container_registry_scope_map" "pull_only" {
  name                    = "pull-only"
  container_registry_name = azurerm_container_registry.main.name
  resource_group_name     = var.resource_group_name

  actions = [
    "repositories/*/content/read",
    "repositories/*/metadata/read"
  ]
}

# Token CI/CD
resource "azurerm_container_registry_token" "cicd_pull" {
  count                   = var.create_cicd_token ? 1 : 0
  name                    = "cicd-pull"
  container_registry_name = azurerm_container_registry.main.name
  resource_group_name     = var.resource_group_name
  scope_map_id            = azurerm_container_registry_scope_map.pull_only.id
  enabled                 = true
}

