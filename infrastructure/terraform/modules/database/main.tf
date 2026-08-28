# ============================================
# Database Module (Azure PostgreSQL Flexible Server)
# ============================================
# Creates Azure Database for PostgreSQL Flexible Server with HA configuration

# Private DNS Zone for PostgreSQL
resource "azurerm_private_dns_zone" "postgres" {
  name                = "${var.name_prefix}.postgres.database.azure.com"
  resource_group_name = var.resource_group_name

  tags = var.labels
}

# Link DNS Zone to VNet
resource "azurerm_private_dns_zone_virtual_network_link" "postgres" {
  name                  = "${var.name_prefix}-pg-dns-link"
  private_dns_zone_name = azurerm_private_dns_zone.postgres.name
  resource_group_name   = var.resource_group_name
  virtual_network_id    = var.network_id

  tags = var.labels
}

# PostgreSQL Flexible Server
resource "azurerm_postgresql_flexible_server" "main" {
  name                          = "${var.name_prefix}-postgres-${var.random_suffix}"
  resource_group_name           = var.resource_group_name
  location                      = var.region
  version                       = var.db_version
  administrator_login           = var.db_user
  administrator_password        = var.db_password
  zone                          = var.availability_zone
  sku_name                      = var.db_tier
  storage_mb                    = var.disk_size * 1024
  auto_grow_enabled             = var.disk_autoresize
  backup_retention_days         = var.backup_enabled ? var.backup_retention_days : 7
  geo_redundant_backup_enabled  = var.geo_redundant_backup
  public_network_access_enabled = var.public_access_enabled

  # Private network configuration
  delegated_subnet_id = var.public_access_enabled ? null : var.delegated_subnet_id
  private_dns_zone_id = var.public_access_enabled ? null : azurerm_private_dns_zone.postgres.id

  # High Availability
  dynamic "high_availability" {
    for_each = var.availability_type == "REGIONAL" ? [1] : []
    content {
      mode                      = "ZoneRedundant"
      standby_availability_zone = var.standby_availability_zone
    }
  }

  # Maintenance window
  maintenance_window {
    day_of_week  = var.maintenance_window.day
    start_hour   = var.maintenance_window.hour
    start_minute = 0
  }

  tags = var.labels

  depends_on = [azurerm_private_dns_zone_virtual_network_link.postgres]
}

# Application Database
resource "azurerm_postgresql_flexible_server_database" "main" {
  name      = var.db_name
  server_id = azurerm_postgresql_flexible_server.main.id
  charset   = "UTF8"
  collation = "en_US.utf8"
}

# ============================================
# Database Flags (Server Configurations)
# ============================================

resource "azurerm_postgresql_flexible_server_configuration" "max_connections" {
  name      = "max_connections"
  server_id = azurerm_postgresql_flexible_server.main.id
  value     = tostring(var.max_connections)
}

resource "azurerm_postgresql_flexible_server_configuration" "log_checkpoints" {
  name      = "log_checkpoints"
  server_id = azurerm_postgresql_flexible_server.main.id
  value     = "on"
}

resource "azurerm_postgresql_flexible_server_configuration" "log_connections" {
  name      = "log_connections"
  server_id = azurerm_postgresql_flexible_server.main.id
  value     = "on"
}

resource "azurerm_postgresql_flexible_server_configuration" "log_disconnections" {
  name      = "log_disconnections"
  server_id = azurerm_postgresql_flexible_server.main.id
  value     = "on"
}

resource "azurerm_postgresql_flexible_server_configuration" "log_min_duration" {
  count = var.log_min_duration_statement != null ? 1 : 0

  name      = "log_min_duration_statement"
  server_id = azurerm_postgresql_flexible_server.main.id
  value     = tostring(var.log_min_duration_statement)
}

# Query Insights (Query Store)
resource "azurerm_postgresql_flexible_server_configuration" "query_store" {
  count = var.insights_enabled ? 1 : 0

  name      = "pg_qs.query_capture_mode"
  server_id = azurerm_postgresql_flexible_server.main.id
  value     = "ALL"
}

# Require SSL
resource "azurerm_postgresql_flexible_server_configuration" "require_ssl" {
  name      = "require_secure_transport"
  server_id = azurerm_postgresql_flexible_server.main.id
  value     = "on"
}

# ============================================
# Read Replica (Optional)
# ============================================

resource "azurerm_postgresql_flexible_server" "replica" {
  count = var.enable_replica ? 1 : 0

  name                = "${var.name_prefix}-postgres-replica-${var.random_suffix}"
  resource_group_name = var.resource_group_name
  location            = var.region
  version             = var.db_version
  zone                = var.availability_zone
  sku_name            = var.db_tier
  storage_mb          = var.disk_size * 1024
  auto_grow_enabled   = var.disk_autoresize

  # Create as replica
  create_mode      = "Replica"
  source_server_id = azurerm_postgresql_flexible_server.main.id

  # Private network
  delegated_subnet_id = var.delegated_subnet_id
  private_dns_zone_id = azurerm_private_dns_zone.postgres.id

  tags = merge(var.labels, { role = "replica" })
}
