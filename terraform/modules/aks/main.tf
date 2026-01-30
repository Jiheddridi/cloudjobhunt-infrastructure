# ============================================
# AZURE KUBERNETES SERVICE (AKS) CLUSTER
# ============================================

resource "azurerm_kubernetes_cluster" "main" {
  name                = "aks-${var.project_name}-${var.environment}"
  location            = var.location
  resource_group_name = var.resource_group_name
  dns_prefix          = "aks-${var.project_name}-${var.environment}"
  
  kubernetes_version        = var.kubernetes_version
  automatic_channel_upgrade = var.automatic_channel_upgrade

  # ============================================
  # DEFAULT NODE POOL (System Pool)
  # ============================================
  default_node_pool {
    name                = "system"
    vm_size             = var.system_node_pool_vm_size
    enable_auto_scaling = true
    min_count           = var.system_node_pool_min_count
    max_count           = var.system_node_pool_max_count
    os_disk_size_gb     = 30
    vnet_subnet_id      = var.aks_subnet_id
    
    node_labels = {
      "role"        = "system"
      "environment" = var.environment
    }

    tags = {
      Role = "System"
    }
  }

  # ============================================
  # IDENTITY (Managed Identity)
  # ============================================
  identity {
    type = "SystemAssigned"
  }

  # ============================================
  # NETWORK PROFILE
  # ============================================
  network_profile {
    network_plugin    = "azure"
    network_policy    = "azure"
    load_balancer_sku = "standard"
    service_cidr      = var.service_cidr
    dns_service_ip    = var.dns_service_ip
  }

  # ============================================
  # AZURE ACTIVE DIRECTORY RBAC
  # ============================================
  azure_active_directory_role_based_access_control {
    managed            = true
    azure_rbac_enabled = true
  }

  # ============================================
  # MONITORING (OMS Agent)
  # ============================================
  oms_agent {
    log_analytics_workspace_id = var.log_analytics_workspace_id
  }

  # ============================================
  # KEY VAULT SECRETS PROVIDER
  # ============================================
  key_vault_secrets_provider {
    secret_rotation_enabled  = true
    secret_rotation_interval = "2m"
  }

  # ============================================
  # MAINTENANCE WINDOW
  # ============================================
  maintenance_window {
    allowed {
      day   = "Sunday"
      hours = [2, 3, 4]
    }
  }

  tags = {
    Environment = var.environment
    Project     = var.project_name
    ManagedBy   = "Terraform"
  }
}

# ============================================
# USER NODE POOL
# ============================================
resource "azurerm_kubernetes_cluster_node_pool" "user" {
  name                  = "user"
  kubernetes_cluster_id = azurerm_kubernetes_cluster.main.id
  vm_size               = var.user_node_pool_vm_size
  enable_auto_scaling   = true
  min_count             = var.user_node_pool_min_count
  max_count             = var.user_node_pool_max_count
  os_disk_size_gb       = 50
  vnet_subnet_id        = var.aks_subnet_id
  mode                  = "User"
  
  node_labels = {
    "role"        = "application"
    "environment" = var.environment
    "workload"    = "general"
  }

  tags = {
    Role     = "User"
    Workload = "Application"
  }
}

# ============================================
# ROLE ASSIGNMENT : ACR PULL
# ============================================
resource "azurerm_role_assignment" "acr_pull" {
  scope                = var.acr_id
  role_definition_name = "AcrPull"
  principal_id         = azurerm_kubernetes_cluster.main.kubelet_identity[0].object_id
  principal_type       = "ServicePrincipal"
}

# ============================================
# DIAGNOSTIC SETTINGS
# ============================================
resource "azurerm_monitor_diagnostic_setting" "aks" {
  name                       = "aks-diagnostics"
  target_resource_id         = azurerm_kubernetes_cluster.main.id
  log_analytics_workspace_id = var.log_analytics_workspace_id

  enabled_log {
    category = "kube-apiserver"
  }
  
  enabled_log {
    category = "kube-controller-manager"
  }
  
  enabled_log {
    category = "kube-scheduler"
  }
  
  enabled_log {
    category = "kube-audit"
  }
  
  enabled_log {
    category = "cluster-autoscaler"
  }

  metric {
    category = "AllMetrics"
    enabled  = true
  }
}
