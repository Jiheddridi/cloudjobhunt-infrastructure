resource "azurerm_postgresql_flexible_server" "main" {
  name                   = "jobhunt-pgsql"  # ✅ Nom propre sans suffixe aléatoire
  resource_group_name    = var.resource_group_name
  location               = var.location
  version                = "14"
  
  administrator_login    = var.admin_username
  administrator_password = var.admin_password
  
  storage_mb             = 32768  # 32 GB
  sku_name               = "GP_Standard_D2s_v3"
  
  backup_retention_days        = 7
  geo_redundant_backup_enabled = false

  # 🔑 Configuration réseau CORRECTE (sans bloc "network")
  delegated_subnet_id = var.subnet_id
  private_dns_zone_id = azurerm_private_dns_zone.postgres.id

  tags = var.tags
}

# Private DNS Zone pour résolution privée
resource "azurerm_private_dns_zone" "postgres" {
  name                = "privatelink.postgres.database.azure.com"
  resource_group_name = var.resource_group_name
}

resource "azurerm_private_dns_zone_virtual_network_link" "postgres_vnet_link" {
  name                  = "jobhunt-vnet-link"
  resource_group_name   = var.resource_group_name
  private_dns_zone_name = azurerm_private_dns_zone.postgres.name
  virtual_network_id    = var.vnet_id
}

# Base de données principale
resource "azurerm_postgresql_flexible_server_database" "jobhunt_db" {
  name      = "jobhunt_db"
  server_id = azurerm_postgresql_flexible_server.main.id
  charset   = "UTF8"
  collation = "en_US.utf8"
}

# Désactiver SSL temporairement pour le développement
resource "azurerm_postgresql_flexible_server_configuration" "require_ssl" {
  name      = "require_secure_transport"
  server_id = azurerm_postgresql_flexible_server.main.id
  value     = "off"
}
