output "vnet_id" { value = azurerm_virtual_network.main.id }
output "aks_subnet_id" { value = azurerm_subnet.aks.id }
output "database_subnet_id" { value = azurerm_subnet.database.id }
output "nsg_id" { value = azurerm_network_security_group.main.id }
output "aks_subnet_cidr" { value = var.subnet_aks_cidr }
