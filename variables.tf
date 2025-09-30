variable "location" {
  description = "Azure Region"
  type        = string
  default     = "North Europe"
}

variable "resource_group_name" {
  description = "Existing Azure Resource Group"
  type        = string
  default     = "rg-lucgr-001"
}

variable "vm_name" {
  description = "Name of the VM"
  type        = string
  default     = "sec-web-vm01"
}

variable "admin_username" {
  description = "Admin user for SSH login"
  type        = string
  default     = "secadmin"
}

variable "ssh_public_key" {
  description = "Your SSH public key (ssh-ed25519 oder ssh-rsa)"
  type        = string
  sensitive   = true
}

variable "vm_size" {
  description = "Azure VM size"
  type        = string
  default     = "Standard_B2s"
}

variable "tags" {
  description = "Common tags"
  type        = map(string)
  default = {
    project = "systemsicherheit"
    owner   = "luca"
    env     = "dev"
  }
}
