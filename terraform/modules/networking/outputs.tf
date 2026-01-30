output "vnet_id" {
  description = "ID du Virtual Network"
  value       = azurerm_virtual_network.main.id
}

output "vnet_name" {
  description = "Nom du Virtual Network"
  value       = azurerm_virtual_network.main.name
}

output "aks_subnet_id" {
  description = "ID du subnet AKS"
  value       = azurerm_subnet.aks.id
}

output "database_subnet_id" {
  description = "ID du subnet Database"
  value       = azurerm_subnet.database.id
}

output "ingress_subnet_id" {
  description = "ID du subnet Ingress"
  value       = azurerm_subnet.ingress.id
}

output "nsg_id" {
  description = "ID du Network Security Group AKS"
  value       = azurerm_network_security_group.aks.id
}

