variable "project_name" {
  type = string
}

variable "environment" {
  type = string
}

variable "location" {
  type = string
}

variable "resource_group_name" {
  type = string
}

variable "aks_subnet_id" {
  type = string
}

variable "service_cidr" {
  type    = string
  default = "10.1.0.0/16"
}

variable "dns_service_ip" {
  type    = string
  default = "10.1.0.10"
}

variable "kubernetes_version" {
  type    = string
  default = null
}

variable "automatic_channel_upgrade" {
  type    = string
  default = "stable"
}

variable "system_node_pool_vm_size" {
  type    = string
  default = "Standard_D2s_v3"
}

variable "system_node_pool_min_count" {
  type    = number
  default = 1
}

variable "system_node_pool_max_count" {
  type    = number
  default = 3
}

variable "user_node_pool_vm_size" {
  type    = string
  default = "Standard_D2s_v3"
}

variable "user_node_pool_min_count" {
  type    = number
  default = 1
}

variable "user_node_pool_max_count" {
  type    = number
  default = 5
}

variable "acr_id" {
  type = string
}

variable "log_analytics_workspace_id" {
  type = string
}
