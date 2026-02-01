variable "project_name" { type = string }
variable "environment" { type = string }
variable "location" { type = string }
variable "resource_group_name" { type = string }
variable "vnet_id" { type = string }
variable "database_subnet_id" { type = string }
variable "aks_subnet_cidr" { type = string }
variable "sku_name" {
  type    = string
  default = "B_Standard_B1ms"
}
variable "storage_mb" {
  type    = number
  default = 32768
}
variable "admin_username" {
  type    = string
  default = "psqladmin"
}
variable "admin_password" {
  type      = string
  sensitive = true
}
variable "database_name" {
  type    = string
  default = "cloudjobhunt"
}
