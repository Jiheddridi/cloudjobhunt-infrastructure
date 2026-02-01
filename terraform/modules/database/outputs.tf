output "server_fqdn" { value = azurerm_postgresql_flexible_server.main.fqdn }
output "database_name" { value = azurerm_postgresql_flexible_server_database.main.name }
output "connection_string" {
  value     = "postgresql://${var.admin_username}:${var.admin_password}@${azurerm_postgresql_flexible_server.main.fqdn}:5432/${var.database_name}?sslmode=require"
  sensitive = true
}
