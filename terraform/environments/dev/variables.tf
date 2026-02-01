variable "project_name" { default = "cloudhunt" }
variable "environment" { default = "dev" }
variable "location" { default = "francecentral" }
variable "vnet_address_space" { default = "10.0.0.0/16" }
variable "subnet_aks_cidr" { default = "10.0.1.0/24" }
variable "subnet_database_cidr" { default = "10.0.2.0/24" }
variable "subnet_ingress_cidr" { default = "10.0.3.0/24" }
variable "db_password" {
  sensitive = true
  default = "CloudJobHunt2026!"
}
