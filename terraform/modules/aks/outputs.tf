output "aks_id" {
  value = azurerm_kubernetes_cluster.main.id
}

output "aks_name" {
  value = azurerm_kubernetes_cluster.main.name
}

output "kube_config" {
  value     = azurerm_kubernetes_cluster.main.kube_config_raw
  sensitive = true
}

