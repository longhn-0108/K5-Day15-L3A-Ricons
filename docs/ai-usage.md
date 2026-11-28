# Khai báo dùng AI

README của nhóm có mục "Dùng AI vào việc gì" (2–3 dòng, bắt buộc). Ghi chi tiết vào bảng dưới đây.

> Luật của đề: dùng AI để làm bài thoải mái, nhưng **ai không giải thích được phần có tên mình thì phần đó nhận 0 điểm**. Khai thiếu không bị trừ; giấu mới bị.

| Việc | Công cụ AI | AI làm gì | Người kiểm/sửa gì | Ai phụ trách |
|---|---|---|---|---|
| Code bản chạy thử & giao diện web | Antigravity (Coding Agent) | Dựng khung `codebase/tools.py`, `agent.py`, `ai.py` (retry/backoff) và giao diện `web_app.py` | Kiểm tay toàn bộ quy tắc lọc ngày `current_day`, cờ `essential`, hiển thị trace/token và chạy đối chiếu từng câu thử | Hoàng Nguyên Long |
| Prompt / thiết kế lời gọi mô hình | Antigravity + Gemini | Gợi ý cấu trúc `SYSTEM` prompt không phán xét và bộ lọc `FORBIDDEN_PATTERNS` | Đọc output thật qua 3 lượt chạy (`run-1` → `run-3`), bổ sung chặn xem hộ `B25` và ép nêu đủ 4 số ngân sách | Hoàng Nguyên Long |
| Đào data (viết script đếm, gợi ý nhãn) | Coding Agent | Hỗ trợ viết script `evidence/count.py` lọc bình luận thực chất và thống kê nhóm pain | Kiểm tay 30 dòng đối chiếu nhãn, khớp 28/30 (93,3%); tự rút trích dẫn nguyên văn bỏ tên | Lê Anh Sơn |
| Rà câu hỏi phỏng vấn / khảo sát | ChatGPT / Gemini | Chỉ rà câu hỏi tránh dẫn dắt theo nguyên tắc Mom Test | Trực tiếp phỏng vấn 3 người thật ngoài nhóm (`P1, P2, P3`), tự ghi chép và tổng hợp bảng Impact | Lê Anh Sơn |
| Viết câu thử (benchmark) | Coding Agent hỗ trợ soạn biến thể | Hỗ trợ nháp biến thể câu chữ cho nhóm `tu_viet` từ lưới tình huống nhóm đặt ra | Thiết kế toàn bộ lưới 25 câu, gán rõ `source` (`9/25` từ `P1–P3` & `RV`), tự tính tay đáp án `expected` | Lưu Văn Việt Đức |
| Sinh data `synthetic` (nếu có) | Python + hỗ trợ nháp mô tả | Khởi tạo khung 120 dòng giao dịch giả lập `data/transactions.csv` & `budgets.json` | Kiểm tay 100% tổng tiền lũy kế theo từng mốc ngày của cả 25 câu thử (`B01–B25`), khớp tuyệt đối với `DATA_CARD.md` | Lưu Văn Việt Đức |
| Chấm cột `pass` | Không dùng LLM tự chấm | Người chấm đối chiếu trực tiếp `output` với `pass_criterion` và 3 metric | Nguyễn Quang Hiệp chấm độc lập 5 câu mẫu trước Lượt 1, khớp 5/5 với Lưu Văn Việt Đức | Lưu Văn Việt Đức & Nguyễn Quang Hiệp |
| Mô phỏng chi phí (persona, giá model, số người dùng) | Claude Code (Claude Opus 5.5) | Tìm trang giá Gemini API và số người dùng có nguồn (blog MoMo); soạn `cost/personas.yaml`; chạy `simulate --try` và đọc lỗi; soạn khung `cost/cost-estimate.md`, `spec.md` §8 | Đổi persona theo bảng Impact `spec.md` §2 cho khớp với Sơn; mở lại từng link nguồn; các tỉ lệ không có nguồn ghi "(tự ước tính)"; kiểm file bằng bộ đọc của `simulate`; số chi phí chép từ file summary, không điền tay | Nguyễn Quang Hiệp |
| Slide, văn bản | Claude Code (Claude Opus 5.5) | Dựng bộ slide 9 trang theo `slides/outline.md`; viết kịch bản video `slides/video-script.md`, kế hoạch buổi người dùng thử, bản nháp reflection | Đối chiếu mọi con số trên slide với `evidence/summary.md`, `spec.md` §2–§4, `eval/benchmark.csv`; chỗ chưa có số để `[__]`; chạy thử B01, B07 trên Web Demo trước khi viết kịch bản; reflection viết lại bằng lời của mình | Nguyễn Quang Hiệp |

**Không dùng AI để:** tạo người được phỏng vấn, trích dẫn, câu trả lời khảo sát; sửa kết quả các lượt đã chạy (`eval/run-*.csv`, `cost/simulate-*.csv`, `traces/`).
