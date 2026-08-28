# Recruitify – Deploy backend lên Azure (gói Student) bằng Terraform

Hạ tầng: 1 VM Ubuntu (Standard_B2s) trong `recruitify-dev-rg`.
VM tự cài Docker (cloud-init), sau đó Terraform upload source backend + chạy
`docker compose up -d --build` để khởi động **backend (Spring Boot)** và
**PostgreSQL** trong Docker trên cùng VM.

```
Terraform ──► Azure RG / VNet / NSG / Public IP / VM Ubuntu
                                   │ cloud-init: cài Docker
                                   ▼
        provisioners: upload web-api + .env + compose ──► docker compose up -d --build
                                   ▼
              recruitify-backend (8080)  +  recruitify-postgres (5432)
```

## Yêu cầu
- `terraform`, `az` CLI đã cài.
- Đã đăng nhập Azure: `az login` (subscription **Azure for Students**).

## Các bước

```bash
cd infrastructure/terraform

# 1. Tạo file biến từ mẫu rồi điền secrets thật
cp enviroiments/dev/terraform.tfvars.example enviroiments/dev/terraform.tfvars
# sửa db_password, jwt_secret, mail_*, imagekit_* trong file vừa tạo

# 2. Khởi tạo + xem trước
make init
make plan

# 3. Tạo hạ tầng và deploy (mất vài phút cho lần build đầu)
make apply

# 4. Lấy thông tin truy cập
make output      # backend_url, swagger_url, ssh_command
make ssh         # SSH vào VM

# Gỡ toàn bộ khi không dùng (tránh tốn credit)
make destroy
```

Sau khi `apply` xong:
- Backend: `http://<public-ip>:8080`
- Swagger: `http://<public-ip>:8080/swagger-ui`
- Health:  `http://<public-ip>:8080/actuator/health`

## Cập nhật code backend sau này
SSH vào VM rồi:
```bash
cd /opt/recruitify
# cập nhật source mới (vd: git/scp) rồi:
sudo docker compose up -d --build
```
Hoặc chạy lại `make apply` (Terraform sẽ upload source mới và build lại).

## CD tự động qua GitHub Actions
Workflow [`.github/workflows/deploy-backend.yml`](../../.github/workflows/deploy-backend.yml)
sẽ tự build + deploy backend lên VM mỗi khi push thay đổi `backend/web-api/**` lên `develop`.

Cần chạy `make apply` 1 lần trước (để có VM + compose + `.env`), rồi tạo 3 GitHub Secrets:

```bash
cd infrastructure/terraform/enviroiments/dev
gh secret set VM_HOST    --body "$(terraform output -raw vm_public_ip)"
gh secret set VM_USER    --body "azureuser"
gh secret set VM_SSH_KEY < vm_ssh_key.pem
```

Tạo thêm GitHub Environment tên `production` tại **Settings → Environments**.
Sau đó mỗi lần push backend → GitHub Actions tự SSH vào VM, upload source mới,
`docker compose up -d --build backend` và chờ container healthy. Nếu health check
thất bại, workflow khôi phục source của phiên bản trước. Có thể chạy tay qua tab
**Actions → Run workflow**.

> Jenkins (Jenkinsfile) lo CI đầy đủ và SonarQube. GitHub Actions chạy lại backend
> test như một deploy gate vì Jenkins đang ở local và có thể offline.

## Lưu ý
- `terraform.tfvars`, `*.pem`, `*.tfstate` đã bị `.gitignore` bỏ qua – không commit.
- Module `modules/database` (Azure PostgreSQL Flexible Server) hiện **không dùng**
  trong thiết lập này; chỉ giữ lại nếu sau muốn tách DB ra dịch vụ managed.
