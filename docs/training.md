# Training QLoRA bằng Docker và Kaggle

Pipeline training không còn phụ thuộc MLX. Nguồn chuẩn là
`training/train_hf.py`; Docker và Kaggle chỉ là hai môi trường chạy cùng script.

## Luồng artifact

```text
data/train.jsonl + data/valid.jsonl
  -> QLoRA Transformers/PEFT
  -> models/peft-adapter
  -> gold evaluation
  -> merge FP16 + llama.cpp converter
  -> models/qwen-fused.gguf
  -> service llm trong docker-compose.yml
```

Adapter MLX cũ không tương thích với PEFT. Pipeline mới dùng thư mục
`models/peft-adapter`, vì vậy không ghi đè checkpoint MLX đang có.

## 1. Chuẩn bị dữ liệu

Trainer nhận JSONL dạng chat hiện tại:

```json
{"messages":[{"role":"system","content":"..."},{"role":"user","content":"..."},{"role":"assistant","content":"..."}]}
```

Sinh lại dữ liệu nếu cần:

```bash
backend/.venv/bin/python training/bootstrap_deep_qa.py
```

Nếu dùng teacher model, khởi động một llama.cpp server trước rồi chạy:

```bash
backend/.venv/bin/python training/bootstrap_deep_qa.py \
  --use-model --model http://localhost:8080
```

## 2. Train trong Docker

Yêu cầu máy Linux có NVIDIA driver, NVIDIA Container Toolkit và Docker Compose.
Docker Desktop trên macOS không truyền Metal/GPU Apple vào Linux container; trên
Mac chỉ nên chạy unit test, không train QLoRA.

```bash
docker compose --profile training build trainer
docker compose --profile training run --rm trainer
```

Trainer tự resume thư mục `checkpoint-N` mới nhất. Muốn bắt đầu run mới mà không
resume, nên đổi `output_dir` trong một config riêng, sau đó chạy:

```bash
docker compose --profile training run --rm trainer \
  python training/train_hf.py --config training/my_run.yaml --fresh
```

Không xóa hoặc dùng lại output của một base model khác. Optimizer state và LoRA
shape trong checkpoint gắn với đúng model/config đã tạo nó.

## 3. Train trên Kaggle

Kaggle đã chạy notebook trong container của Kaggle, vì vậy không chạy
`docker compose` bên trong notebook. Bật GPU và Internet, rồi dùng các cell:

```python
%cd /kaggle/working
!git clone https://github.com/thanhhung-dev/HeritageGraph.git
%cd HeritageGraph
!pip install -r training/requirements.txt
```

`data/` bị Git ignore. Upload `train.jsonl` và `valid.jsonl` thành một Kaggle
Dataset riêng, attach nó vào notebook, rồi copy vào working directory:

```python
!mkdir -p data
!cp /kaggle/input/heritagegraph-training-data/train.jsonl data/train.jsonl
!cp /kaggle/input/heritagegraph-training-data/valid.jsonl data/valid.jsonl
!python training/train_hf.py --config training/lora_config.yaml --fresh
```

Output nằm ở `/kaggle/working/HeritageGraph/models/peft-adapter`. Sau khi train,
phải Save Version hoặc tải artifact về; `/kaggle/working` không phải nơi lưu trữ
lâu dài giữa các session.

```python
!tar -czf /kaggle/working/peft-adapter.tar.gz -C models peft-adapter
```

Muốn resume ở session sau, attach artifact cũ như một Kaggle Dataset, copy cả
thư mục `peft-adapter` vào `models/`, rồi chạy lại không có `--fresh`.

## 4. Đánh giá và xuất GGUF

Chạy trên Linux/Kaggle đã cài training requirements, hoặc dùng chính container:

```bash
docker compose --profile training run --rm trainer bash training/eval.sh
docker compose --profile training run --rm trainer bash training/eval.sh 75
docker compose --profile training run --rm trainer bash training/fuse.sh
docker compose --profile training run --rm trainer bash training/fuse.sh 75
```

Export đọc `base_model_name_or_path` từ `adapter_config.json`, do đó không thể vô
tình merge adapter vào sai base model. Kết quả `models/qwen-fused.gguf` được dùng
trực tiếp bởi service `llm` hiện tại.

Merge model 8B FP16 cần nhiều RAM hơn lúc QLoRA. Nếu Kaggle hết RAM ở bước export,
chỉ train/evaluate adapter trên Kaggle, tải adapter về và export trên máy Linux
hoặc cloud instance có đủ RAM.

## 5. Nâng lên Qwen 3.5 8B

Khi model chính thức và phiên bản Transformers tương thích đã có, tạo config mới
thay vì sửa run 3B đang dùng:

```bash
cp training/lora_config.yaml training/qwen35_8b.yaml
```

Sửa tối thiểu:

```yaml
model_id: <hugging-face-id-chính-thức-của-Qwen-3.5-8B-Instruct>
output_dir: models/qwen35-8b-peft-adapter
batch_size: 1
gradient_accumulation_steps: 8
max_seq_length: 1536
target_modules: all-linear
```

`target_modules: all-linear` tránh hardcode tên layer của Qwen2.5. Tuy nhiên,
không thể đảm bảo trước rằng một kiến trúc tương lai chạy với phiên bản thư viện
hiện tại; cần nâng `transformers`/`peft` nếu model card chính thức yêu cầu.

Với GPU 16 GB, bắt đầu bằng batch 1, gradient checkpointing và QLoRA NF4 như
config hiện tại. Nếu OOM, giảm `max_seq_length` xuống 1024 trước; chỉ giảm
`lora_rank` khi vẫn thiếu VRAM. Luôn train ra output mới và chạy lại toàn bộ gold
evaluation trước khi thay GGUF production.
