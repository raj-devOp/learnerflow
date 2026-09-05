# Tell Terraform we're using Azure
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.0"
    }
  }
}

# Configure the Azure provider
provider "azurerm" {
  features {}
}

# Create a resource group
resource "azurerm_resource_group" "main" {
  name     = "learnerflow-rg"
  location = "ukwest"
}

# App Service Plan — the compute that hosts the app
resource "azurerm_service_plan" "main" {
  name                = "learnerflow-plan"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  os_type             = "Linux"
  sku_name            = "B1"
}

# The web app itself, running your container from GHCR
resource "azurerm_linux_web_app" "main" {
  name                = "learnerflow-app-2026"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_service_plan.main.location
  service_plan_id     = azurerm_service_plan.main.id

  site_config {
    application_stack {
      docker_image_name   = "raj-devop/learnerflow:latest"
      docker_registry_url = "https://ghcr.io"
    }
  }

  app_settings = {
    WEBSITES_PORT = "8000"
  }
}

# Print the live URL after deployment
output "app_url" {
  value = "https://${azurerm_linux_web_app.main.default_hostname}"
}
