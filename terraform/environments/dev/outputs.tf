output "aks_cluster_name" { value = module.aks.cluster_name }
output "database_server_fqdn" { value = module.database.server_fqdn }
output "database_connection_string" {
  value     = module.database.connection_string
  sensitive = true
}
