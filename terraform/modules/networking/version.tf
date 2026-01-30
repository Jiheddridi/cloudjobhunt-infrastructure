# ============================================
# PROVIDER AZURE – VERSION FIXE
# ============================================

terraform {
  required_version = ">= 1.5" # version moderne Terraform

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.80" # dernière branche stable 3.x
    }
  }
}

# ============================================
# PROVIDER AZURE
# ============================================
provider "azurerm" {
  features {}
}

