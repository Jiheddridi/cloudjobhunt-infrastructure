output "postgres_fqdn" {
  description = "Nom de domaine complet du serveur PostgreSQL"
  value       = azurerm_postgresql_flexible_server.main.fqdn
  sensitive   = false
}

output "postgres_id" {
  description = "ID de la ressource PostgreSQL"
  value       = azurerm_postgresql_flexible_server.main.id
  sensitive   = false
}

output "database_name" {
  description = "Nom de la base de données"
  value       = azurerm_postgresql_flexible_server_database.jobhunt_db.name
  sensitive   = false
}

output "connection_string" {
  description = "Chaîne de connexion PostgreSQL"
  value       = "postgresql://${var.admin_username}:${var.admin_password}@${azurerm_postgresql_flexible_server.main.fqdn}:5432/${azurerm_postgresql_flexible_server_database.jobhunt_db.name}"
  sensitive   = true
}
