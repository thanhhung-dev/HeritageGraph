# ============================================
# Database Module Outputs
# ============================================

output "server_id" {
  description = "PostgreSQL Flexible Server ID"
  value       = azurerm_postgresql_flexible_server.main.id
}

output "server_name" {
  description = "PostgreSQL Flexible Server name"
  value       = azurerm_postgresql_flexible_server.main.name
}

output "server_fqdn" {
  description = "Fully qualified domain name of the server"
  value       = azurerm_postgresql_flexible_server.main.fqdn
}

output "database_name" {
  description = "Application database name"
  value       = azurerm_postgresql_flexible_server_database.main.name
}

output "connection_string" {
  description = "JDBC connection string"
  value       = "jdbc:postgresql://${azurerm_postgresql_flexible_server.main.fqdn}:5432/${var.db_name}?sslmode=require"
}

output "administrator_login" {
  description = "Administrator login"
  value       = azurerm_postgresql_flexible_server.main.administrator_login
}

output "replica_fqdn" {
  description = "Read replica FQDN"
  value       = var.enable_replica ? azurerm_postgresql_flexible_server.replica[0].fqdn : null
}
