output "public_ip" {
  description = "Oeffentliche IP der VM"
  value       = azurerm_public_ip.pip.ip_address
}

output "admin_username" {
  description = "Admin Benutzername"
  value       = var.admin_username
}

output "ssh_command" {
  description = "SSH Befehl"
  value       = "ssh ${var.admin_username}@${azurerm_public_ip.pip.ip_address}"
}
