# Ricons — [Tên lát cắt dự kiến]

**Thành viên, lớp, track:** xem [TEAMS.md](TEAMS.md). **Điền TEAMS.md đúng format**: khi chấm và đánh giá, BTC quét file này để ghép điểm cho từng người.

*Lát cắt = phần nhỏ nhất làm xong được trong hackathon: một người dùng · một việc · một quyết định AI · một kết quả.*

---

## Nhóm làm gì, khung làm gì

| Nhóm quyết định và viết | Khung làm sẵn (không cần sửa) |
|---|---|
| Người dùng, pain, bằng chứng, impact (`evidence/`, `spec.md` §1–§2) | — |
| Hình dạng giải pháp, công cụ, prompt, luồng (`spec.md` §4, `codebase/agent.py`, `tools.py`, `ai.py`) | Ghi mọi lần gọi model / công cụ vào trace, cộng token (`codebase/tracing.py`) |
| Bộ câu thử, metric, chuẩn "đạt" (`eval/benchmark.csv`, `eval/metric_spec.yaml`, `spec.md` §7) | Kiểm đủ cột, đủ câu `kho` / `tu_choi`, đủ ≥1/3 câu từ người dùng / data thật (`run.py check`) |
| Chấm cột `pass` theo metric spec | Chạy cả bộ một lệnh, có run ID, model, token từng câu (`run.py eval`) · tính % đạt (`run.py score`) |
| Persona, số người dùng thật, giá model (`cost/personas.yaml`) | Sinh ~50 phiên, chạy thật qua bản chạy thử, tính chi phí / phiên, / task thành công, / tháng 3 kịch bản (`run.py simulate`) |

## Chạy trong 3 phút

| Việc | Windows (PowerShell) | macOS / Linux |
|---|---|---|
| Kiểm Python | `python --version` (không được thì `py --version`) | `python3 --version` |
| Chạy bản chạy thử (chế độ giả, chưa gọi model) | `python run.py` | `python3 run.py` |
| Kiểm bộ câu thử & TEAMS.md | `python run.py check` | `python3 run.py check` |
| Tạo file `.env` để nối model | `copy .env.example .env` | `cp .env.example .env` |

## Lệnh

| Lệnh | Làm gì |
|---|---|
| `python run.py` | Chạy bản chạy thử (gõ đầu vào, nhận kết quả, kèm số lần gọi model / token) |
| `python run.py check` | Kiểm `eval/benchmark.csv`, `eval/metric_spec.yaml` và `TEAMS.md` |
| `python run.py eval --try` | Thử nối model: chạy 3 câu đầu → `eval/run-try.csv` |
| `python run.py eval` | Chạy cả bộ qua `codebase/agent.py` → `eval/run-1.csv` |
| `python run.py score eval/run-1.csv` | Sau khi điền cột `pass` (1 / 0): in % đạt tổng và theo `type` |
| `python run.py simulate --try` | Thử mô phỏng chi phí 10 phiên → `cost/simulate-try.csv` |
| `python run.py simulate` | Mô phỏng chi phí khi dùng thật theo `cost/personas.yaml` (≥50 phiên) |

## Phần nào thật, phần nào giả

| Thành phần | Thật / Giả | Ghi chú |
|---|---|---|
| Lời gọi AI ở quyết định trung tâm | **Thật** (bắt buộc từ CP3) | Model: ____ |

## Dùng AI vào việc gì

2–3 dòng (bắt buộc): nhóm dùng công cụ AI nào để làm gì, người kiểm lại phần nào. Chi tiết: [docs/ai-usage.md](docs/ai-usage.md).
