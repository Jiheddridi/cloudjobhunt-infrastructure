output "resource_group_name" {
  description = "Nom du Resource Group"
  value       = azurerm_resource_group.main.name
}

output "vnet_id" {
  description = "ID du Virtual Network"
  value       = module.networking.vnet_id
}

output "aks_subnet_id" {
  description = "ID du subnet AKS"
  value       = module.networking.aks_subnet_id
}

output "database_subnet_id" {
  description = "ID du subnet Database"
  value       = module.networking.database_subnet_id
}

output "ingress_subnet_id" {
  description = "ID du subnet Ingress"
  value       = module.networking.ingress_subnet_id
}

output "nsg_id" {
  description = "ID du Network Security Group"
  value       = module.networking.nsg_id
}

