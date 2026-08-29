#!/usr/bin/env python3
"""
Tạo 3 file mẫu nhỏ để smoke-test pipeline training.
Chạy: python scripts/make_smoke_data.py
"""
import json
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"
DATA.mkdir(parents=True, exist_ok=True)

SYSTEM = (
    "Bạn là trợ lý văn hóa dân gian Việt Nam. "
    "Trích xuất entity chính xác theo 4 loại: người, địa điểm, sự kiện, thời gian. "
    "Trả lời văn phong trang trọng, giàu tính kể chuyện. "
    "Luôn trích nguồn khi dùng thông tin. Không bịa thông tin ngoài nguồn."
)

samples = [
    {
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": "Trích entity (người, địa điểm, sự kiện, thời gian) từ:\n\n\"Nghệ nhân Nguyễn Văn A (1912-1985) quê làng gốm Bát Tràng, thường trình diễn tại hội làng đầu xuân.\""},
            {"role": "assistant", "content": "{\"người\": [\"Nguyễn Văn A\"], \"địa điểm\": [\"làng gốm Bát Tràng\"], \"sự kiện\": [\"hội làng đầu xuân\"], \"thời gian\": [\"1912-1985\"]}"},
        ]
    },
    {
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": "Nguồn: \"Hội thi thổi cơm làng Đường Lâm diễn ra ngày mùng 4 tháng Giêng hằng năm, thu hút hàng nghìn du khách.\"\n\nCâu hỏi: Hội thi thổi cơm diễn ra khi nào và ở đâu?"},
            {"role": "assistant", "content": "Theo nguồn, hội thi thổi cơm làng Đường Lâm là lễ hội truyền thống được tổ chức vào ngày mùng 4 tháng Giêng hằng năm, thu hút đông đảo du khách thập phương. [Nguồn: Hội thi thổi cơm làng Đường Lâm diễn ra ngày mùng 4 tháng Giêng hằng năm]"},
        ]
    },
    {
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": "Nguồn: (không có)\n\nCâu hỏi: Lễ hội Đền Hùng có nguồn gốc từ thời nào?"},
            {"role": "assistant", "content": "Không tìm thấy thông tin này trong nguồn được cung cấp. Vui lòng cung cấp thêm tài liệu tham khảo để tôi trả lời chính xác."},
        ]
    },
    {
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": "Giải thích thuật ngữ \"tế lễ\" trong văn cảnh: \"Nghi lễ tế lễ tại đình làng được cử hành vào dịp xuân về.\""},
            {"role": "assistant", "content": "Trong văn cảnh trên, \"tế lễ\" chỉ nghi thức cúng tế trang trọng tại đình làng, thường được tổ chức vào dịp đầu năm mới để tưởng nhớ các vị thành hoàng và cầu mong mùa màng bội thu."},
        ]
    },
    {
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": "Trích entity từ:\n\n\"Làng tranh Đông Hồ thuộc huyện Thuận Thành, tỉnh Bắc Ninh, nổi tiếng với dòng tranh dân gian từ thế kỷ XVII. Hằng năm vào Tết, dân làng mở hội đua thuyền trên sông Đuống.\""},
            {"role": "assistant", "content": "{\"người\": [], \"địa điểm\": [\"Làng tranh Đông Hồ\", \"huyện Thuận Thành\", \"tỉnh Bắc Ninh\", \"sông Đuống\"], \"sự kiện\": [\"hội đua thuyền\"], \"thời gian\": [\"thế kỷ XVII\", \"Tết\"]}"},
        ]
    },
]

train_path = DATA / "train.jsonl"
valid_path = DATA / "valid.jsonl"

with train_path.open("w", encoding="utf-8") as f:
    for s in samples:
        f.write(json.dumps(s, ensure_ascii=False) + "\n")

with valid_path.open("w", encoding="utf-8") as f:
    f.write(json.dumps(samples[0], ensure_ascii=False) + "\n")
    f.write(json.dumps(samples[1], ensure_ascii=False) + "\n")

print(f"wrote {len(samples)} train, 2 valid → {DATA}")
