# Chạy HeritageGraph local bằng Docker Compose

Gói portable dùng `llama.cpp` thay cho MLX vì container Linux không truy cập được
Metal/MLX trên macOS. Ba service được chạy: `llm`, `backend`, `frontend`.
PostgreSQL không nằm trong gói vì backend MVP hiện tại chưa sử dụng database.

## 1. Chuẩn bị gói trên máy Mac đang có LoRA

Yêu cầu tạm thời khoảng 12 GB đĩa trống và internet để lấy converter:

```bash
backend/.venv/bin/python scripts/export_gguf.py
bash scripts/package_docker.sh
```

`export_gguf.py` fuse trực tiếp base + checkpoint trong `models/lora-serve`,
dequantize trước khi fuse và chỉ quantize một lần sang Q8_0. Không dùng thư mục
`models/qwen-fused` cũ vì model đó đã qua vòng requantize làm giảm chất lượng.

Kết quả là `heritagegraph-docker.tar.gz`, bao gồm code, corpus và GGUF. Model và
corpus bị Git ignore nên clone repository đơn thuần **không đủ** để chạy offline.

## 2. Chạy trên máy khác

Yêu cầu Docker Desktop/Engine có Compose v2, RAM tối thiểu 8 GB và khoảng 6 GB
đĩa trống. CPU x86_64 và ARM64 đều chạy được.

```bash
tar -xzf heritagegraph-docker.tar.gz
cd HeritageGraph
docker compose up -d
docker compose ps
```

Không cần cài Python/Node, tạo `.env`, export model hay thêm `--build`. Compose tự
build backend/frontend và tải image `llama.cpp` trong lần chạy đầu. File
`.env.docker.example` chỉ dùng khi muốn đổi cổng, địa chỉ API hoặc cấu hình GPU.

Lần đầu Docker tải image và llama.cpp nạp model nên health check có thể mất vài
phút. Khi backend báo `healthy`:

- Giao diện: <http://localhost:3000>
- Backend health: <http://localhost:8000/api/health>
- API docs: <http://localhost:8000/docs>

Test một câu không qua giao diện:

```bash
curl -X POST http://localhost:8000/api/chat \
  -H 'Content-Type: application/json' \
  -d '{"message":"Cao lầu là món gì?","use_rag":true}'
```

Xem log hoặc dừng hệ thống:

```bash
docker compose logs -f llm backend
docker compose down
```

## 3. Truy cập từ máy khác trong LAN

Sửa `.env` trước khi build, dùng IP máy chạy Docker:

```dotenv
NEXT_PUBLIC_API_URL=http://192.168.1.20:8000
```

Sau đó chạy `docker compose up --build -d`. Mở cổng 3000 và 8000 trên firewall.

## 4. Hiệu năng và kiểm định

Mặc định `LLAMA_GPU_LAYERS=0` để chạy được trên mọi CPU. Docker Desktop trên Mac
không truyền Metal vào container nên sẽ chậm hơn MLX native. Với NVIDIA Container
Toolkit, cần bổ sung quyền GPU cho service `llm` rồi tăng `LLAMA_GPU_LAYERS`.

GGUF là runtime khác với baseline MLX. Trước khi dùng số liệu trong báo cáo, chạy
lại gold set qua API Docker và ghi thành một baseline riêng; không mặc định xem
kết quả GGUF giống hoàn toàn checkpoint MLX.
