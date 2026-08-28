# ============================================
# Database Module Variables
# ============================================

variable "name_prefix" {
  description = "Prefix for resource names"
  type        = string
}

variable "random_suffix" {
  description = "Random suffix for unique naming"
  type        = string
}

variable "resource_group_name" {
  description = "Azure Resource Group name"
  type        = string
}

variable "region" {
  description = "Azure region"
  type        = string
}

variable "network_id" {
  description = "VNet ID for private DNS zone link"
  type        = string
}

variable "delegated_subnet_id" {
  description = "Subnet ID delegated to PostgreSQL Flexible Server"
  type        = string
}

# Database configuration
variable "db_version" {
  description = "PostgreSQL version"
  type        = string
  default     = "16"
}

variable "db_tier" {
  description = "SKU name (e.g., B_Standard_B1ms, GP_Standard_D2s_v3)"
  type        = string
  default     = "B_Standard_B1ms"
}

variable "db_name" {
  description = "Application database name"
  type        = string
  default     = "recruitify"
}

variable "db_user" {
  description = "Database administrator login"
  type        = string
  default     = "recruitify"
}

variable "db_password" {
  description = "Database administrator password"
  type        = string
  sensitive   = true
}

# Storage
variable "disk_size" {
  description = "Storage size in GB"
  type        = number
  default     = 32
}

variable "disk_autoresize" {
  description = "Enable auto-grow storage"
  type        = bool
  default     = true
}

# Availability
variable "availability_type" {
  description = "Availability type: ZONAL or REGIONAL"
  type        = string
  default     = "ZONAL"
}

variable "availability_zone" {
  description = "Primary availability zone"
  type        = string
  default     = "1"
}

variable "standby_availability_zone" {
  description = "Standby availability zone for HA"
  type        = string
  default     = "2"
}

variable "deletion_protection" {
  description = "Enable deletion protection (not natively supported, use Azure locks)"
  type        = bool
  default     = true
}

# Backup
variable "backup_enabled" {
  description = "Enable backup"
  type        = bool
  default     = true
}

variable "backup_retention_days" {
  description = "Number of days to retain backups"
  type        = number
  default     = 7
}

variable "geo_redundant_backup" {
  description = "Enable geo-redundant backup"
  type        = bool
  default     = false
}

# Maintenance
variable "maintenance_window" {
  description = "Maintenance window configuration"
  type = object({
    day          = number
    hour         = number
    update_track = optional(string, "stable")
  })
  default = {
    day          = 0 # Sunday
    hour         = 3
    update_track = "stable"
  }
}

# Performance
variable "max_connections" {
  description = "Maximum number of connections"
  type        = number
  default     = 100
}

variable "log_min_duration_statement" {
  description = "Log statements taking longer than this (ms). Null to disable."
  type        = number
  default     = null
}

variable "insights_enabled" {
  description = "Enable Query Store (Query Insights)"
  type        = bool
  default     = false
}

# Replica
variable "enable_replica" {
  description = "Enable read replica"
  type        = bool
  default     = false
}

# Public access (tạm bật để migrate, tắt sau)
variable "public_access_enabled" {
  description = "Enable public network access"
  type        = bool
  default     = false
}

# Labels/Tags
variable "labels" {
  description = "Tags to apply to resources"
  type        = map(string)
  default     = {}
}
