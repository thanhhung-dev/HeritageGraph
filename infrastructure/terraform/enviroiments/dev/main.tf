# ============================================
# Recruitify - Hạ tầng DEV trên Azure (gói Student)
# ============================================
# Terraform tạo toàn bộ hạ tầng từ con số 0:
#   Resource Group -> VNet/Subnet -> NSG -> Public IP -> NIC -> VM Ubuntu
# VM tự cài Docker (qua cloud-init). App + Postgres chạy bằng docker compose.

terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.0"
    }
    tls = {
      source  = "hashicorp/tls"
      version = "~> 4.0"
    }
    local = {
      source  = "hashicorp/local"
      version = "~> 2.0"
    }
  }

  required_version = ">= 1.1.0"
}

provider "azurerm" {
  features {}

  # Auth qua Azure CLI (az login). Subscription gói Student.
  subscription_id = var.subscription_id
}

# ============================================
# Variables
# ============================================
variable "subscription_id" {
  description = "Azure Subscription ID (gói Azure for Students)"
  type        = string
  default     = "70f35953-79e9-45da-bd54-9d6396d1ecd9"
}

variable "location" {
  description = "Azure region"
  type        = string
  default     = "japaneast"
}

variable "vm_size" {
  description = "Gói (SKU) của VM ARM64. japaneast chỉ còn dòng Ampere: Standard_B2pls_v2 (4GB) / Standard_B2ps_v2 (8GB)"
  type        = string
  default     = "Standard_B2ps_v2"
}

variable "admin_username" {
  description = "Tài khoản đăng nhập VM"
  type        = string
  default     = "azureuser"
}

# ============================================
# App config (secrets) - đặt giá trị trong terraform.tfvars
# ============================================
variable "db_name" {
  description = "Tên database"
  type        = string
  default     = "recruitify"
}

variable "db_username" {
  description = "User database"
  type        = string
  default     = "recruitify"
}

variable "db_password" {
  description = "Mật khẩu database"
  type        = string
  sensitive   = true
}

variable "jwt_secret" {
  description = "JWT secret key"
  type        = string
  sensitive   = true
}

variable "mail_username" {
  description = "Email gửi mail (Gmail)"
  type        = string
  default     = ""
}

variable "mail_password" {
  description = "App password của email"
  type        = string
  default     = ""
  sensitive   = true
}

variable "imagekit_url_endpoint" {
  description = "ImageKit URL endpoint"
  type        = string
  default     = ""
}

variable "imagekit_private_key" {
  description = "ImageKit private key"
  type        = string
  default     = ""
  sensitive   = true
}

variable "imagekit_public_key" {
  description = "ImageKit public key"
  type        = string
  default     = ""
}

# ============================================
# Resource Group
# ============================================
resource "azurerm_resource_group" "rg" {
  name     = "recruitify-dev-rg"
  location = var.location
}

# ============================================
# Network: VNet + Subnet
# ============================================
resource "azurerm_virtual_network" "main" {
  name                = "recruitify-vnet"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  address_space       = ["10.0.0.0/16"]
}

resource "azurerm_subnet" "app" {
  name                 = "app-subnet"
  resource_group_name  = azurerm_resource_group.rg.name
  virtual_network_name = azurerm_virtual_network.main.name
  address_prefixes     = ["10.0.1.0/24"]
}

# ============================================
# NSG: mở các port cần thiết
# ============================================
resource "azurerm_network_security_group" "main" {
  name                = "recruitify-nsg"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  # SSH
  security_rule {
    name                       = "SSH"
    priority                   = 1001
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "22"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }

  # Frontend (Next.js) + reverse proxy HTTP
  security_rule {
    name                       = "HTTP"
    priority                   = 1002
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "80"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }

  # Frontend dev port (Next.js mặc định 3000)
  security_rule {
    name                       = "Frontend"
    priority                   = 1003
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "3000"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }

  # Backend (Spring Boot)
  security_rule {
    name                       = "Backend"
    priority                   = 1004
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "8080"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }
}

resource "azurerm_subnet_network_security_group_association" "main" {
  subnet_id                 = azurerm_subnet.app.id
  network_security_group_id = azurerm_network_security_group.main.id
}

# ============================================
# Public IP + NIC
# ============================================
resource "azurerm_public_ip" "main" {
  name                = "recruitify-pip"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  allocation_method   = "Static"
  sku                 = "Standard"
}

resource "azurerm_network_interface" "main" {
  name                = "recruitify-nic"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.app.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.main.id
  }
}

# ============================================
# SSH key (Terraform tự sinh, lưu ra file local)
# ============================================
resource "tls_private_key" "ssh" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

resource "local_file" "ssh_private_key" {
  content         = tls_private_key.ssh.private_key_pem
  filename        = "${path.module}/vm_ssh_key.pem"
  file_permission = "0600"
}

# ============================================
# VM Ubuntu 24.04 (tự cài Docker qua cloud-init)
# ============================================
resource "azurerm_linux_virtual_machine" "app" {
  name                = "recruitify-vm"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  size                = var.vm_size # <-- GÓI (SKU) VM ghi ở đây
  admin_username      = var.admin_username

  network_interface_ids = [azurerm_network_interface.main.id]

  admin_ssh_key {
    username   = var.admin_username
    public_key = tls_private_key.ssh.public_key_openssh
  }

  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }

  source_image_reference {
    publisher = "Canonical"
    offer     = "ubuntu-24_04-lts"
    sku        = "server"
    version   = "latest"
  }

  # Script tự cài Docker khi VM khởi động lần đầu
  custom_data = base64encode(file("${path.module}/cloud-init.yaml"))

  # ----- Kết nối SSH để deploy -----
  connection {
    type        = "ssh"
    host        = azurerm_public_ip.main.ip_address
    user        = var.admin_username
    private_key = tls_private_key.ssh.private_key_pem
    timeout     = "5m"
  }

  # 1) Đóng gói source backend (loại bỏ build/cache) ngay trên máy chạy terraform
  provisioner "local-exec" {
    command = "tar czf ${path.module}/web-api.tgz -C ${path.module}/../../../../backend --exclude='web-api/build' --exclude='web-api/.gradle' --exclude='web-api/bin' --exclude='web-api/.idea' web-api"
  }

  # 2) Đợi cloud-init cài Docker xong rồi tạo thư mục app
  provisioner "remote-exec" {
    inline = [
      "echo 'Doi cloud-init (cai Docker) hoan tat...'",
      "sudo cloud-init status --wait || true",
      "sudo mkdir -p /opt/recruitify",
      "sudo chown -R ${var.admin_username}:${var.admin_username} /opt/recruitify",
    ]
  }

  # 3) Upload source + compose + .env
  provisioner "file" {
    source      = "${path.module}/web-api.tgz"
    destination = "/opt/recruitify/web-api.tgz"
  }

  provisioner "file" {
    source      = "${path.module}/app-compose.yml"
    destination = "/opt/recruitify/docker-compose.yml"
  }

  provisioner "file" {
    content = templatefile("${path.module}/env.tftpl", {
      db_name               = var.db_name
      db_username           = var.db_username
      db_password           = var.db_password
      jwt_secret            = var.jwt_secret
      mail_username         = var.mail_username
      mail_password         = var.mail_password
      imagekit_url_endpoint = var.imagekit_url_endpoint
      imagekit_private_key  = var.imagekit_private_key
      imagekit_public_key   = var.imagekit_public_key
    })
    destination = "/opt/recruitify/.env"
  }

  # 4) Giải nén source và build + chạy backend + postgres
  provisioner "remote-exec" {
    inline = [
      "cd /opt/recruitify",
      "tar xzf web-api.tgz",
      "rm -f web-api.tgz",
      "echo 'Build va khoi dong container (lan dau co the mat vai phut)...'",
      "sudo docker compose up -d --build",
      "sudo docker compose ps",
    ]
  }
}

# ============================================
# Outputs
# ============================================
output "vm_public_ip" {
  description = "IP public để SSH và truy cập app"
  value       = azurerm_public_ip.main.ip_address
}

output "ssh_command" {
  description = "Lệnh SSH vào VM"
  value       = "ssh -i ${path.module}/vm_ssh_key.pem ${var.admin_username}@${azurerm_public_ip.main.ip_address}"
}

output "backend_url" {
  description = "URL truy cập backend"
  value       = "http://${azurerm_public_ip.main.ip_address}:8080"
}

output "swagger_url" {
  description = "Swagger UI"
  value       = "http://${azurerm_public_ip.main.ip_address}:8080/swagger-ui"
}
