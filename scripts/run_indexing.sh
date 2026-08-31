#!/usr/bin/env bash
# Xây knowledge graph + xuất artifact ra graphrag/output/.
#
# Bản cũ gọi pipeline LLM của MS GraphRAG (cần Ollama, chạy 8-12 giờ, prompt
# extract mặc định bằng tiếng Anh trên văn bản tiếng Việt, và entity do LLM sinh
# ra có thể BỊA). Corpus ở đây chỉ 23 bài nên cách đó vừa đắt vừa kém chính xác.
# Nay graph được xây deterministic trong backend/core/kg.py: mọi node đều truy
# được về một chuỗi có thật trong văn bản, build hết ~0.15 giây.
set -e
cd "$(dirname "$0")/.."

PY=backend/.venv/bin/python
[ -x "$PY" ] || PY=python3

"$PY" scripts/build_graph.py "$@"

echo ""
echo "Xem thêm:"
echo "  $PY scripts/build_graph.py --query \"lăng Minh Mạng xây năm nào\"   # truy dấu câu hỏi qua graph"
echo "  $PY scripts/build_graph.py --node \"triều Nguyễn\"                  # xem láng giềng của node"
echo "  $PY eval/eval_retrieval.py                                        # đo recall + tỉ lệ từ chối"
