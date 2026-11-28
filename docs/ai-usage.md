# Khai báo dùng AI

README của nhóm có mục "Dùng AI vào việc gì" (2–3 dòng, bắt buộc). Ghi chi tiết vào bảng dưới đây.

> Luật của đề: dùng AI để làm bài thoải mái, nhưng **ai không giải thích được phần có tên mình thì phần đó nhận 0 điểm**. Khai thiếu không bị trừ; giấu mới bị.

| Việc | Công cụ AI | AI làm gì | Người kiểm/sửa gì | Ai phụ trách |
|---|---|---|---|---|
| Code bản chạy thử | | | | |
| Prompt / thiết kế lời gọi mô hình | | | | |
| Đào data (viết script đếm, gợi ý nhãn) | | | Kiểm tay __ dòng, khớp __ | |
| Rà câu hỏi phỏng vấn / khảo sát | | Chỉ rà câu dẫn dắt | | |
| Viết câu thử (benchmark) | | | Mỗi câu thử có `source`; câu thử AI viết được ghi rõ | |
| Sinh data `synthetic` (nếu có) | | | Seed __ · kiểm tay __ dòng | |
| Chấm cột `pass` bằng LLM (nếu có) | | | Kiểm tra thủ công __ câu thử, khớp __/__ | |
| Mô phỏng chi phí (persona, giá model, số người dùng) | Claude Code (Claude Opus 5.5) | Tìm trang giá Gemini API và số người dùng có nguồn (blog MoMo); soạn `cost/personas.yaml`; chạy `simulate --try` và đọc lỗi; soạn khung `cost/cost-estimate.md`, `spec.md` §8 | Đổi persona theo bảng Impact `spec.md` §2 cho khớp với Sơn; mở lại từng link nguồn; các tỉ lệ không có nguồn ghi "(tự ước tính)"; kiểm file bằng bộ đọc của `simulate`; số chi phí chép từ file summary, không điền tay | Nguyễn Quang Hiệp |
| Slide, văn bản | Claude Code (Claude Opus 5.5) | Dựng bộ slide 9 trang theo `slides/outline.md`; viết kịch bản video `slides/video-script.md`, kế hoạch buổi người dùng thử, bản nháp reflection | Đối chiếu mọi con số trên slide với `evidence/summary.md`, `spec.md` §2–§4, `eval/benchmark.csv`; chỗ chưa có số để `[__]`; chạy thử B01, B07 trên Web Demo trước khi viết kịch bản; reflection viết lại bằng lời của mình | Nguyễn Quang Hiệp |

**Không dùng AI để:** tạo người được phỏng vấn, trích dẫn, câu trả lời khảo sát; sửa kết quả các lượt đã chạy (`eval/run-*.csv`, `cost/simulate-*.csv`, `traces/`).
