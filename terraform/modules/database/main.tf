resource "azurerm_private_dns_zone" "postgres" {
  name                = "${var.project_name}-${var.environment}.postgres.database.azure.com"
  resource_group_name = var.resource_group_name
  tags = { Environment = var.environment, Project = var.project_name }
}
resource "azurerm_private_dns_zone_virtual_network_link" "postgres" {
  name                  = "vnet-link-${var.environment}"
  private_dns_zone_name = azurerm_private_dns_zone.postgres.name
  resource_group_name   = var.resource_group_name
  virtual_network_id    = var.vnet_id
  tags = { Environment = var.environment }
}
resource "azurerm_postgresql_flexible_server" "main" {
  name                = "psql-${var.project_name}-${var.environment}"
  resource_group_name = var.resource_group_name
  location            = var.location
  version             = "16"
  sku_name            = var.sku_name
  storage_mb          = var.storage_mb
  administrator_login    = var.admin_username
  administrator_password = var.admin_password
  delegated_subnet_id    = var.database_subnet_id
  private_dns_zone_id    = azurerm_private_dns_zone.postgres.id
  high_availability { mode = "Disabled" }
  maintenance_window {
    day_of_week  = 0
    start_hour   = 3
    start_minute = 0
  }
  tags = { Environment = var.environment, Project = var.project_name, ManagedBy = "Terraform" }
  depends_on = [azurerm_private_dns_zone_virtual_network_link.postgres]
}
resource "azurerm_postgresql_flexible_server_database" "main" {
  name      = var.database_name
  server_id = azurerm_postgresql_flexible_server.main.id
  charset   = "UTF8"
  collation = "en_US.utf8"
}
resource "azurerm_postgresql_flexible_server_firewall_rule" "allow_aks" {
  name             = "allow-aks-subnet"
  server_id        = azurerm_postgresql_flexible_server.main.id
  start_ip_address = cidrhost(var.aks_subnet_cidr, 0)
  end_ip_address   = cidrhost(var.aks_subnet_cidr, 255)
}
