variable "project_name" { type = string }
variable "environment" { type = string }
variable "location" { type = string }
variable "resource_group_name" { type = string }
variable "vnet_address_space" {
  type    = string
  default = "10.0.0.0/16"
}
variable "subnet_aks_cidr" {
  type    = string
  default = "10.0.1.0/24"
}
variable "subnet_database_cidr" {
  type    = string
  default = "10.0.2.0/24"
}
variable "subnet_ingress_cidr" {
  type    = string
  default = "10.0.3.0/24"
}
